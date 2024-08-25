from datetime import datetime
import pytz

class Time:

    def __init__(self):
        # Create a UTC timezone object
        utc_tz = pytz.UTC

        # Generate a datetime object with microseconds precision
        self.now = datetime.now(utc_tz)
        self.microsecond_timestamp = self.now.timestamp()

        print(f"time: {self.microsecond_timestamp}")

    def __str__(self):
        return f"{self.microsecond_timestamp}"