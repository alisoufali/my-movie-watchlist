import datetime

import pytz


class Utilities:

    @staticmethod
    def convert_date_time_local_to_utc(
        local_dt: datetime.datetime = None,
        timezone: pytz.BaseTzInfo = None
    ):
        utc_dt = timezone.localize(local_dt).astimezone(pytz.utc)
        return utc_dt
