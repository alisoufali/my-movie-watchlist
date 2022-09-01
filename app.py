from pathlib import Path
from typing import Optional

from modules.config import Config
from modules.menu import Menu
from modules.enums import MenuFunctionalities


class Main:

    @classmethod
    def main(cls, config_path: Optional[Path] = None):

        Config.load_configs(config_path=config_path)

        menu = Menu(indent=2)

        while (user_input := int(input(menu))) != \
                MenuFunctionalities.EXIT.value:
            if user_input == \
                    MenuFunctionalities.ADD_MOVIE.value:
                pass
            elif user_input == \
                    MenuFunctionalities.VIEW_UPCOMMING_MOVIES.value:
                pass
            elif user_input == \
                    MenuFunctionalities.VIEW_ALL_MOVIES.value:
                pass
            elif user_input == \
                    MenuFunctionalities.WATCH_A_MOVIE.value:
                pass
            elif user_input == \
                    MenuFunctionalities.VIEW_WATCHED_MOVIES.value:
                pass
            else:
                print("Invalid input please try again.")


if __name__ == "__main__":
    Main.main()
