# Persisting the Azure DevOps PAT on macOS

## Purpose

Store the Azure DevOps Personal Access Token (PAT) in macOS Keychain and load it
into the `AZDO_PAT_LBRX` environment variable whenever an interactive zsh session
starts. The MCP server receives this value through its configuration.

Persistence does not make a PAT permanent: Azure DevOps expiration, revocation,
and organization policies still apply. This setup does not automatically renew
the token.

## 1. Store the PAT in Keychain

Create or regenerate a PAT in Azure DevOps with only the permissions required
for your work. Copy the token into Keychain rather than into a repository file,
chat message, or shell command.

1. Open **Keychain Access** using Spotlight.
2. Select the **login** keychain.
3. Search for `AZDO_PAT_LBRX`.
4. If the item already exists, open it, update its password with the PAT, and
   save the change.
5. If it does not exist, choose **File > New Password Item** and enter:

   | Field | Value |
   |---|---|
   | Keychain Item Name | `AZDO_PAT_LBRX` |
   | Account Name | The output of `whoami` in Terminal |
   | Password | The actual Azure DevOps PAT |

Run this command to identify the account name:

```zsh
whoami
```

The item name and account must match the lookup command below. Allow Keychain
access when prompted, after confirming that the request is expected.

## 2. Configure the Persistent Environment Variable

Open your zsh startup configuration:

```zsh
nano ~/.zshrc
```

If `ZDOTDIR` is configured, edit the `.zshrc` inside that directory instead.

Add the following block once. If the existing lookup line is already present,
replace that line with this block rather than adding a second definition:

```zsh
if AZDO_PAT_LBRX="$(security find-generic-password -a "$USER" -s "AZDO_PAT_LBRX" -w)"; then
  export AZDO_PAT_LBRX
else
  unset AZDO_PAT_LBRX
  print -u2 -- "Failed to load AZDO_PAT_LBRX from macOS Keychain."
fi
```

In nano, press **Control+O**, then **Enter** to save, and **Control+X** to exit.

This block:

- Reads the PAT from Keychain without printing it.
- Exports the value to processes started from that shell.
- Reports a lookup failure explicitly and removes any stale value.
- Stores only the lookup command in the startup file, not the token itself.

The existing one-line version performs the same lookup on success:

```zsh
export AZDO_PAT_LBRX="$(security find-generic-password -a "$USER" -s "AZDO_PAT_LBRX" -w)"
```

The block is preferred because `export` can mask the lookup command's failure
status in the one-line version.

### Plaintext Alternative: Put the Value Directly in the Startup File

If you deliberately choose not to use Keychain, replace the Keychain lookup
with this line in the same startup file:

```zsh
export AZDO_PAT_LBRX='YOUR_ACTUAL_PAT'
```

Replace `YOUR_ACTUAL_PAT` in the editor with the actual token. Do not run a
command containing your real PAT in Terminal, where it may enter shell history.
Use only one method; do not keep both definitions.

**This alternative stores the PAT in plaintext.** Anyone or any backup or
dotfile-sync service with access to the file may obtain it. Never commit the
startup file or token. Keychain is the recommended option.

## 3. Load and Verify the Value

Open a new Terminal window, or apply the startup configuration to the current
shell:

```zsh
source ~/.zshrc
```

If you use `ZDOTDIR`, source the startup file from that directory instead.

Check whether the variable is populated without exposing the token:

```zsh
if [[ -n "$AZDO_PAT_LBRX" ]]; then
  echo "AZDO_PAT_LBRX is loaded."
else
  echo "AZDO_PAT_LBRX is missing." >&2
fi
```

This verifies only that a value is loaded. It does not verify that the PAT is
valid, unexpired, or authorized for an Azure DevOps operation.

Do not use `echo "$AZDO_PAT_LBRX"`, `printenv AZDO_PAT_LBRX`, or shell tracing
(`set -x`) when loading or diagnosing the token.

## 4. Make the Value Available to the MCP Server

Keep the environment-variable reference in the repository's
[MCP configuration](../.mcp.json):

```json
{
  "env": {
    "AZDO_PAT": "${AZDO_PAT_LBRX}"
  }
}
```

This is an excerpt, not a replacement for the complete configuration. It maps
the local `AZDO_PAT_LBRX` variable to the MCP server's `AZDO_PAT` variable.
Environment substitution depends on the MCP client; this example assumes the
client supports `${AZDO_PAT_LBRX}` references.

1. Fully quit VS Code with **Command+Q**, closing all running instances.
2. In the terminal where verification succeeded, navigate to the repository.
3. Launch VS Code:

   ```zsh
   code .
   ```

4. Restart or reconnect the Azure DevOps MCP server using your client's controls.
5. Perform a read-only operation, such as listing projects, to verify
   authentication without changing remote data.

If `code` is unavailable, open the VS Code Command Palette and run
**Shell Command: Install 'code' command in PATH**, then retry.

Applications inherit their environment when they start. Updating the variable
in Terminal does not update an already-running VS Code or MCP server.
Launching VS Code from the Dock is not guaranteed to inherit your terminal's
environment; use the terminal launch procedure for predictable behavior.

## 5. Update an Expired or Rotated PAT

1. Create or regenerate the PAT in Azure DevOps.
2. Update the password of the existing Keychain item named `AZDO_PAT_LBRX`.
   Keep its account name unchanged.
3. Open a new terminal or reload the startup configuration.
4. Verify that the variable is loaded without printing it.
5. Fully quit VS Code, launch it from that terminal, and reconnect the MCP server.
6. Verify authentication with a read-only operation.
7. If you created a separate replacement token, revoke the old token after
   confirming that the replacement works.

The startup configuration and MCP placeholder do not need to change when using
Keychain. If you chose the plaintext alternative, update the value in the
startup file instead.

## Troubleshooting

| Symptom | Action |
|---|---|
| Keychain reports that the item cannot be found | Confirm the item name is `AZDO_PAT_LBRX` and its account matches `$USER`. |
| Keychain denies access | Unlock the login keychain and review the access prompt or the item's access controls. |
| The value is missing after reopening Terminal | Confirm that Terminal uses zsh, that the correct startup file was edited, and that no later setting overwrites or unsets the variable. |
| Terminal has the value, but MCP does not | Fully quit VS Code, launch it from the verified terminal, and reconnect MCP. Confirm that the client supports the configured environment substitution. |
| MCP returns `401 Unauthorized` | Confirm that the new token was loaded into the MCP process and that it is valid, unexpired, and belongs to the intended organization. |
| MCP returns `403 Forbidden` | Check the PAT scopes and the user's permissions for the requested resource. |

## Security Checklist

- Prefer Keychain over plaintext token storage.
- Never paste the real token into repository files, documentation, screenshots,
  chat messages, logs, or command arguments.
- Do not print the token while troubleshooting or share a full environment dump.
- Grant only the PAT permissions required for the intended operations.
- Rotate tokens before expiry and revoke any token that may have been exposed.
- Remember that exporting a token makes it available to child processes of that
  shell; Keychain protects storage, not the environment of running processes.
