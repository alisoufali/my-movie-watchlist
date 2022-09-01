import datetime
import sqlite3

import pytz

from modules.database import Database
from modules.utilities import Utilities


class UserUtilities:

    @staticmethod
    def view_movies_in_cursor(cursor: sqlite3.Cursor = None,
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
        Database.insert_movie(
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
        cursor = Database.select_movies(
            upcomming=True, today_timestamp=today_timestamp,
            order=True, order_by="date", ascending=True
        )
        header = "Upcomming Movies"
        UserUtilities.view_movies_in_cursor(
            cursor=cursor, timezone=timezone, header=header, indent=indent
        )

    @classmethod
    def view_all_movies(cls, timezone: pytz.BaseTzInfo = None, indent: int = 4) -> None:
        cursor = Database.select_movies(
            upcomming=False, order=True,
            order_by="title", ascending=True
        )
        header = "All Movies"
        UserUtilities.view_movies_in_cursor(
            cursor=cursor, timezone=timezone, header=header, indent=indent
        )

    @classmethod
    def watch_movie(cls, title: str = None):
        Database.update_movie_watched(title=title, is_watched=True)

    @classmethod
    def view_watched_movies(cls, timezone: pytz.BaseTzInfo = None,
                            indent: int = 4) -> None:
        cursor = Database.select_movies(
            filter_watch=True, watched=True, order=True,
            order_by="date", ascending=True
        )
        header = "Watched Movies"
        UserUtilities.view_movies_in_cursor(
            cursor=cursor, timezone=timezone, header=header, indent=indent
        )
