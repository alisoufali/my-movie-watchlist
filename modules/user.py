import datetime
import sqlite3

import pytz

from modules.database import Database
from modules.utilities import Utilities


class UserUtilities:

    @staticmethod
    def view_movies_from_movies(cursor: sqlite3.Cursor = None,
                                timezone: pytz.BaseTzInfo = None,
                                header: str = None, indent: int = 4) -> None:
        if cursor.arraysize > 0:
            indentation = " " * indent
            print(f"\n{indentation}-- {header} --\n")
            for movie in cursor:
                title = movie["title"]
                release_date = datetime.datetime.fromtimestamp(
                    movie["release_timestamp"], timezone
                )
                release_date_string = release_date.strftime("%b %d %Y")
                output_string = \
                    f"{indentation}{title}:    {release_date_string}"
                print(output_string)

    @staticmethod
    def view_watched_movies_from_watched(cursor: sqlite3.Cursor = None,
                                         username: str = None,
                                         indent: int = 4) -> None:
        if cursor.arraysize > 0:
            indentation = " " * indent
            print(f"\n{indentation}-- {username}'s Watched Movies --\n")
            for movie in cursor:
                title = movie["title"]
                output_string = f"{indentation}{title}"
                print(output_string)


class UserFunctions:

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
        UserUtilities.view_movies_from_movies(
            cursor=cursor, timezone=timezone, header=header, indent=indent
        )

    @classmethod
    def view_all_movies(cls, timezone: pytz.BaseTzInfo = None,
                        indent: int = 4) -> None:
        cursor = Database.select_movies_from_movies(
            upcomming=False, order=True,
            order_by="title", ascending=True
        )
        header = "All Movies"
        UserUtilities.view_movies_from_movies(
            cursor=cursor, timezone=timezone, header=header, indent=indent
        )

    @classmethod
    def view_watched_movies(cls, username: str = None,
                            indent: int = 4) -> None:
        cursor = Database.select_movies_from_watched(
            username=username, order=True, ascending=True
        )
        UserUtilities.view_watched_movies_from_watched(
            cursor=cursor, username=username, indent=indent
        )

    @classmethod
    def watch_movie(cls, username: str = None, title: str = None):
        all_movies_in_movies = Database.select_movies_from_movies(
            upcomming=False, order=False
        ).fetchall()
        found_movie_in_movies = False
        for movie in all_movies_in_movies:
            if movie["title"] == title:
                found_movie_in_movies = True
                break
        else:
            print("\nMovie not found in movies table.\n"
                  "Please add it there first.")
        if found_movie_in_movies:
            Database.insert_watched_movie_to_watched(
                username=username, title=title
            )
