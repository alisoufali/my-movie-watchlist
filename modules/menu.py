import datetime
import sqlite3
from typing import List

import pytz

from modules.database import Database
from modules.enums import MenuFunctionalities
from modules.utilities import Utilities


class MenuUtilities:

    @staticmethod
    def view_movies(cursor: sqlite3.Cursor = None,
                    timezone: pytz.BaseTzInfo = None,
                    header: str = None, indent: int = 4) -> None:
        cursor_data = cursor.fetchall()
        if len(cursor_data) > 0:
            indentation = " " * indent
            print(f"\n{indentation}-- {header} --\n")
            for movie in cursor_data:
                id_ = movie["id"]
                title = movie["title"]
                release_date = datetime.datetime.fromtimestamp(
                    movie["release_timestamp"], timezone
                )
                release_date_string = release_date.strftime("%b %d %Y")
                output_string = \
                    f"{indentation}{id_}:  {title},    {release_date_string}"
                print(output_string)

    @staticmethod
    def view_users(cursor: sqlite3.Cursor = None, header: str = None,
                   indent: int = 4) -> None:
        cursor_data = cursor.fetchall()
        if len(cursor_data) > 0:
            indentation = " " * indent
            print(f"\n{indentation}-- {header} --\n")
            for user in cursor_data:
                id_ = user["id"]
                username = user["username"]
                output_string = \
                    f"{indentation}{id_}:  {username}"
                print(output_string)


class MenuFunctions:

    @classmethod
    def add_user(cls, username: str = None):
        Database.insert_user_to_users(username=username)

    @classmethod
    def add_movie(cls, title: str = None, release_date_string: str = None,
                  timezone: pytz.BaseTzInfo = None) -> None:
        release_date_local = \
            datetime.datetime.strptime(release_date_string, "%d-%m-%Y")
        release_date_utc = Utilities.convert_date_time_local_to_utc(
            local_dt=release_date_local, timezone=timezone
        )
        release_date_timestamp = release_date_utc.timestamp()
        Database.insert_movie_to_movies(
            title=title,
            release_date_timestamp=release_date_timestamp
        )

    @classmethod
    def watch_movie(cls, username: str = None, title: str = None):
        Database.insert_watched_movie_to_watch_list(
            username=username, title=title
        )

    @classmethod
    def view_all_users(cls, indent: int = 4) -> None:
        cursor = Database.select_users_from_users()
        header = "Users"
        MenuUtilities.view_users(
            cursor=cursor, header=header,
            indent=indent
        )

    @classmethod
    def view_upcomming_movies(cls, timezone: pytz.BaseTzInfo = None,
                              indent: int = 4) -> None:
        today_date_local = datetime.datetime.today()
        today_date = Utilities.convert_date_time_local_to_utc(
            local_dt=today_date_local, timezone=timezone
        )
        today_timestamp = today_date.timestamp()
        cursor = Database.select_movies_from_movies(
            upcomming=True, today_timestamp=today_timestamp,
            order=True, order_by="date", ascending=True
        )
        header = "Upcomming Movies"
        MenuUtilities.view_movies(
            cursor=cursor, timezone=timezone,
            header=header, indent=indent
        )

    @classmethod
    def view_all_movies(cls, timezone: pytz.BaseTzInfo = None,
                        indent: int = 4) -> None:
        cursor = Database.select_movies_from_movies(
            upcomming=False, order=True,
            order_by="title", ascending=True
        )
        header = "All Movies"
        MenuUtilities.view_movies(
            cursor=cursor, timezone=timezone,
            header=header, indent=indent
        )

    @classmethod
    def view_watched_movies(cls, username: str = None,
                            timezone: pytz.BaseTzInfo = None,
                            indent: int = 4) -> None:
        cursor = Database.select_user_watched_movies(
            username=username, order=True, order_by="title",
            ascending=True
        )
        header = f"{username}'s Watched Movies"
        MenuUtilities.view_movies(
            cursor=cursor, timezone=timezone,
            header=header, indent=indent
        )


class Menu:

    WELCOME_MESSAGE = "Welcome to my movie watchlist application!"

    def __init__(self, indent: int = 2):
        print(f"{self.WELCOME_MESSAGE}")
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
                "\nPlease select one of the following options:"
                "\n"
                f"{menu_items_string}"
                "\n"
                "Your selection: "
            )

        return menu_message

    def __str__(self):
        return self.message
