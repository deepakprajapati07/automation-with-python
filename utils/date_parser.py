from datetime import datetime

# Parse Date
def parse_date(date_str: str) -> datetime:
    """Parse a date string safely into a datetime object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")