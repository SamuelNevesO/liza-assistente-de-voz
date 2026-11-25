from __future__ import annotations

import logging

from src.ui.app import LizaApp


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    app = LizaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
