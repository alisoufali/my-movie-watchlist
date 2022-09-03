import sqlite3
from typing import Union

from pypika import Column, Order, Parameter, Query, Table, JoinType
from pypika.functions import Lower

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
        cls.__create_users_table()
        cls.__create_movies_table()
        cls.__create_watch_list_table()

    @classmethod
    def __create_users_table(cls) -> None:
        table = Table("users")
        columns = [
            Column(column_name="id", column_type="INTEGER"),
            Column(column_name="username", column_type="TEXT")
        ]
        query = Query.create_table(table=table).if_not_exists().\
            columns(*columns).primary_key("id").unique("username")
        with cls.__connection:
            cls.__connection.execute(query.get_sql())

    @classmethod
    def __create_movies_table(cls) -> None:
        table = Table(name="movies")
        columns = [
            Column(column_name="id", column_type="INTEGER"),
            Column(column_name="title", column_type="TEXT"),
            Column(column_name="release_timestamp", column_type="REAL"),
        ]
        query = Query.create_table(table).if_not_exists().\
            columns(*columns).primary_key("id").\
            unique("title", "release_timestamp")
        with cls.__connection:
            cls.__connection.execute(query.get_sql())

    @classmethod
    def __create_watch_list_table(cls) -> None:
        table = Table("watch_list")
        columns = [
            Column(column_name="user_id", column_type="INTEGER"),
            Column(column_name="movie_id", column_type="INTEGER")
        ]
        query = Query.create_table(table=table).if_not_exists().\
            columns(*columns).\
            unique("user_id", "movie_id")
        # There is a bug in pypika to have more than one foreign keys
        # We bypass this bug as the following
        query_string = query.get_sql()
        query_string = query_string[:-1] +\
            ', FOREIGN KEY ("user_id") REFERENCES "users" ("id")' +\
            ', FOREIGN KEY ("movie_id") REFERENCES "movies" ("id")' +\
            ')'
        with cls.__connection:
            cls.__connection.execute(query_string)

    @classmethod
    def get_user_id_by_username(cls, username: str = None) -> Union[int, None]:
        table = Table(name="users")
        query = Query.from_(table=table).select(table.id).\
            where(table.username == Parameter("?"))
        parameters = (username, )

        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql(), parameters)
        selected_users = cursor.fetchall()

        if len(selected_users) == 0:
            print(f"{username} not found in database.")
            user_id = None
        else:
            user_id = selected_users[0]["id"]

        return user_id

    @classmethod
    def get_movie_id_by_title(cls, title: str = None) -> Union[int, None]:
        table = Table("movies")
        query = Query.from_(table=table).select(table.id).\
            where(table.title == Parameter("?"))
        parameters = (title, )

        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql(), parameters)
        selected_movies = cursor.fetchall()

        if len(selected_movies) == 0:
            print(f"{title} not found in database.")
            movie_id = None
        else:
            movie_id = selected_movies[0]["id"]

        return movie_id

    @classmethod
    def insert_user_to_users(cls, username: str = None) -> None:
        table = Table("users")

        check_query = Query.from_(table=table).select("*").\
            where(table.username == Parameter("?"))
        check_parameters = (username, )
        check_cursor = cls.__connection.cursor()
        check_cursor.execute(check_query.get_sql(), check_parameters)
        check_cursor_data = check_cursor.fetchall()
        if len(check_cursor_data) > 0:
            print(f"{username} has already been added to users table!")
            return None

        query = Query.into(table=table).columns("username").\
            insert(Parameter("?"))
        parameters = (username, )
        with cls.__connection:
            cls.__connection.execute(query.get_sql(), parameters)

    @classmethod
    def insert_movie_to_movies(cls, title: str = None,
                               release_date_timestamp: float = None) -> None:
        table = Table(name="movies")

        check_query = Query.from_(table=table).select("*").\
            where(table.title == Parameter("?"))
        check_parameters = (title, )
        check_cursor = cls.__connection.cursor()
        check_cursor.execute(check_query.get_sql(), check_parameters)
        check_cursor_data = check_cursor.fetchall()
        if len(check_cursor_data) > 0:
            for movie in check_cursor_data:
                timestamp_error = \
                    abs(movie["release_timestamp"] - release_date_timestamp)
                if timestamp_error < 0.1:
                    print(f"{title} has already been added to movies table!")
                    return None

        query = Query.into(table=table).\
            columns("title", "release_timestamp").\
            insert(Parameter("?"), Parameter("?"))
        parameters = (title, release_date_timestamp)
        with cls.__connection:
            cls.__connection.execute(query.get_sql(), parameters)

    @classmethod
    def insert_watched_movie_to_watch_list(cls, username: str = None,
                                           title: str = None) -> None:
        user_id = cls.get_user_id_by_username(username=username)
        movie_id = cls.get_movie_id_by_title(title=title)

        if user_id is None or movie_id is None:
            return None

        table = Table(name="watch_list")

        check_query = Query.from_(table=table).select("*").\
            where((table.user_id == Parameter("?")) &
                  (table.movie_id == Parameter("?")))
        check_parameters = (user_id, movie_id)

        check_cursor = cls.__connection.cursor()
        check_cursor.execute(check_query.get_sql(), check_parameters)
        check_cursor_data = check_cursor.fetchall()
        if len(check_cursor_data) > 0:
            print(f"{username} has already watched {title}!")
            return None

        query = Query.into(table=table).\
            columns("user_id", "movie_id").\
            insert(Parameter("?"), Parameter("?"))
        parameters = (user_id, movie_id)

        with cls.__connection:
            cls.__connection.execute(query.get_sql(), parameters)

    @classmethod
    def select_users_from_users(cls, order: bool = False,
                                order_by: str = "username",
                                ascending: bool = True) -> sqlite3.Cursor:
        table = Table("users")
        query = Query.from_(table=table).select("*")

        if order:
            if order_by == "username":
                orderby_column = table.username
            elif order_by == "id":
                orderby_column = table.id
            if ascending:
                order_pattern = Order.asc
            else:
                order_pattern = Order.desc
            query = query.orderby(orderby_column, order=order_pattern)

        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql())
        return cursor

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
            elif order_by == "id":
                orderby_column = table.id
            if ascending:
                order_pattern = Order.asc
            else:
                order_pattern = Order.desc
            query = query.orderby(orderby_column, order=order_pattern)

        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql(), parameters)
        return cursor

    @classmethod
    def select_user_watched_movies(cls, username: str = None,
                                   order: bool = False,
                                   order_by: str = "date",
                                   ascending: bool = True
                                   ) -> sqlite3.Cursor:
        users_table = Table("users")
        movies_table = Table("movies")
        watch_list_table = Table("watch_list")

        query = Query.from_(table=movies_table).\
            select(movies_table.id, movies_table.title,
                   movies_table.release_timestamp).\
            join(watch_list_table, JoinType.inner).\
            on(watch_list_table.movie_id == movies_table.id).\
            join(users_table, JoinType.inner).\
            on(watch_list_table.user_id == users_table.id).\
            where(users_table.username == Parameter("?"))
        parameters = (username, )

        if order:
            if order_by == "title":
                orderby_column = movies_table.title
            elif order_by == "date":
                orderby_column = movies_table.release_timestamp

            if ascending:
                order_pattern = Order.asc
            else:
                order_pattern = Order.desc
            query = query.orderby(orderby_column, order=order_pattern)

        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql(), parameters)
        return cursor

    @classmethod
    def select_searched_movies(cls, search_term: str = None,
                               order: bool = False,
                               order_by: str = "title",
                               ascending: bool = True
                               ) -> sqlite3.Cursor:
        table = Table("movies")

        query = Query.from_(table=table).select("*").\
            where(Lower(table.title).like(Parameter("?")))
        parameters = (f"%{search_term.lower()}%", )

        if order:
            if order_by == "title":
                orderby_column = table.title
            elif order_by == "date":
                orderby_column = table.release_timestamp

            if ascending:
                order_pattern = Order.asc
            else:
                order_pattern = Order.desc
            query = query.orderby(orderby_column, order=order_pattern)

        cursor = cls.__connection.cursor()
        cursor.execute(query.get_sql(), parameters)
        return cursor
