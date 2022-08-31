from enum import Enum
from typing import List


class MenuFunctionalities(Enum):

    ADD_MOVIE = 1
    VIEW_UPCOMMING_MOVIES = 2
    VIEW_ALL_MOVIES = 3
    WATCH_A_MOVIE = 4
    VIEW_WATCHED_MOVIES = 5
    EXIT = 6

    @classmethod
    def get_sorted_functionalities(cls) -> List:
        functionalities = list(cls)
        functionalities.sort(key=(lambda functionality: functionality.value))
        return functionalities
