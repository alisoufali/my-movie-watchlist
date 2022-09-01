import sqlite3

from pypika import Column, Parameter, Query, Table, Order

from modules.config import Config


class Database:

    __connection = None

    @classmethod
    def connect_to_database(cls) -> None:
        cls.__connection = sqlite3.connect(database=Config.DATABASE_PATH)
        cls.__connection.row_factory = sqlite3.Row
        cls.__create_tables()

    @classmethod
    def __create_tables(cls) -> None:
        cls.__create_movies_table()
        cls.__create_watched_table()

    @classmethod
    def __create_movies_table(cls) -> None:
        table = Table(name="movies")
        columns = [
            Column(column_name="title", column_type="TEXT"),
            Column(column_name="release_timestamp", column_type="REAL"),
        ]
        query = Query.create_table(table).\
            if_not_exists().columns(*columns)
        with cls.__connection:
            cls.__connection.execute(query.get_sql())

    @classmethod
    def __create_watched_table(cls) -> None:
        table = Table("watched")
        columns = [
            Column(column_name="watcher_name", column_type="TEXT"),
            Column(column_name="title", column_type="TEXT")
        ]
        query = Query.create_table(table=table).\
            if_not_exists().columns(*columns)
        with cls.__connection:
            cls.__connection.execute(query.get_sql())

    @classmethod
    def insert_movie(cls, title: str = None,
                     release_date_timestamp: float = None) -> None:
        table = Table(name="movies")
        query = Query.into(table=table).\
            columns("title", "release_timestamp").\
            insert(Parameter("?"), Parameter("?"))
        parameters = (title, release_date_timestamp)
        with cls.__connection:
            cls.__connection.execute(query.get_sql(), parameters)

    @classmethod
    def select_movies_from_movies(cls, upcomming: bool = False,
                                  today_timestamp: float = None,
                                  order: bool = False,
                                  order_by: str = "date",
                                  ascending: bool = True) -> sqlite3.Cursor:

        table = Table(name="movies")

        if upcomming:
            query = Query.from_(table=table).select("*").\
                where(table.release_timestamp > Parameter("?"))
            parameters = (today_timestamp, )
        else:
            query = Query.from_(table=table).select("*")
            parameters = tuple()

        if order:
            if order_by == "date":
                orderby_column = table.release_timestamp
            elif order_by == "title":
                orderby_column = table.title
            if ascending:
                order_pattern = Order.asc
            else:
                order_pattern = Order.desc
            query = query.orderby(orderby_column, order=order_pattern)

        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql(), parameters)
        return cursor

    @classmethod
    def update_movie_watched(cls, title: str = None,
                             is_watched: int = None) -> None:
        table = Table(name="movies")
        query = Query.update(table=table).set(
            table.watched, int(is_watched)).where(
            table.title == title)
        with cls.__connection:
            cls.__connection.execute(query.get_sql())

    @classmethod
    def select_movies_from_watched(cls, username: str = None,
                                   order: bool = False,
                                   ascending: bool = True) -> sqlite3.Cursor:
        table = Table("watched")
        query = Query.from_(table=table).select(table.title).\
            where(table.watcher_name == Parameter("?"))
        if order:
            orderby_column = table.title
            if ascending:
                order_pattern = Order.asc
            else:
                order_pattern = Order.desc
            query = query.orderby(orderby_column, order=order_pattern)
        parameters = (username, )
        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql(), parameters)
        return cursor
