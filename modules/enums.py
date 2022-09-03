from enum import Enum
from typing import List


class MenuFunctionalities(Enum):

    ADD_USER = 1
    ADD_MOVIE = 2
    WATCH_A_MOVIE = 3
    VIEW_ALL_USERS = 4
    VIEW_ALL_MOVIES = 5
    VIEW_UPCOMMING_MOVIES = 6
    VIEW_WATCHED_MOVIES = 7
    SEARCH_MOVIE = 8
    EXIT = 9

    @classmethod
    def get_sorted_functionalities(cls) -> List:
        functionalities = list(cls)
        functionalities.sort(key=(lambda functionality: functionality.value))
        return functionalities
