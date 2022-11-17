import sys
from typing import Sequence

from erdb.main.app import App


def entrypoint(argv: Sequence[str] | None = None) -> int:
    app = App(sys.argv[1:] if argv is None else argv)
    return app.run()