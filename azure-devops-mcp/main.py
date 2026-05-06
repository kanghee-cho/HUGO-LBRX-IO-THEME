import logging
import sys

from config import Settings


def run() -> None:
    settings = Settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stderr,
    )

    transport = "streamable-http" if "--http" in sys.argv else "stdio"

    from server import mcp
    mcp.run(transport=transport)


if __name__ == "__main__":
    run()
