from pathlib import Path
from typing import Optional

from modules.config import Config
from modules.menu import Menu


class Main:

    @classmethod
    def main(cls, config_path: Optional[Path] = None):

        Config.load_configs(config_path=config_path)

        menu = Menu(indent=2)

        print(menu)
        pass


if __name__ == "__main__":
    Main.main()
