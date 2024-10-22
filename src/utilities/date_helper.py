from datetime import datetime, timezone, timedelta

class Date:
    def __init__(self, unix_timestamp: int = None):
        if unix_timestamp is not None:
            self.unix_timestamp = unix_timestamp
        else:
            # Default to current Unix timestamp
            self.unix_timestamp = int(datetime.now(timezone.utc).timestamp())

    def is_valid(self) -> bool:
        """Check if the stored Unix timestamp is valid (non-negative)."""
        return self.unix_timestamp >= 0

    def to_formatted_date(self) -> str:
        """Convert Unix timestamp to formatted date string (MM-DD-YYYY)."""
        dt = datetime.fromtimestamp(self.unix_timestamp, timezone.utc)
        return dt.strftime("%m-%d-%Y")

    def add_time(self, seconds: int = 0, minutes: int = 0, hours: int = 0):
        """Add specified time to the Unix timestamp."""
        total_seconds = seconds + (minutes * 60) + (hours * 3600)
        self.unix_timestamp += total_seconds

    def get_unix_timestamp(self) -> int:
        """Return the current Unix timestamp."""
        return self.unix_timestamp

