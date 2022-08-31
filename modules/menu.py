from typing import List

from modules.enums import MenuFunctionalities


class Menu:

    WELCOME_MESSAGE = "Welcome to my movie watchlist application!"

    def __init__(self, indent: int = 2):
        print(f"{self.WELCOME_MESSAGE}\n")
        self.message = self.__create_menu_message(indent=indent)

    def __create_menu_items(self, indent: int = 2) -> List[str]:

        indentation = " " * indent

        menu_sorted_functionalities = \
            MenuFunctionalities.get_sorted_functionalities()

        menu_items = [None] * len(menu_sorted_functionalities)
        for index, functionality in enumerate(menu_sorted_functionalities):
            menu_items[index] = (f"{indentation}{functionality.value}) "
                                 f"{functionality.name}")

        return menu_items

    def __create_menu_message(self, indent: int = 2) -> str:

        menu_items = self.__create_menu_items(indent=indent)
        menu_items_string = "\n".join(menu_items)

        menu_message = \
            (
                "Please select one of the following options:"
                "\n"
                f"{menu_items_string}"
                "\n"
                "Your selection: "
            )

        return menu_message

    def __str__(self):
        return self.message
