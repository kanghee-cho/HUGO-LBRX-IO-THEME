class AzureDevOpsError(Exception):
    """Base exception for all Azure DevOps API errors."""


class NotFoundError(AzureDevOpsError):
    """Raised when a requested resource does not exist (HTTP 404)."""


class AuthenticationError(AzureDevOpsError):
    """Raised when the PAT is invalid or lacks required permissions (HTTP 401/403)."""
