# Count no of days between two dates
from datetime import datetime
from typing import Optional

# Count Days
def count_days(date1: datetime, use_today: bool, date2: Optional[datetime] = None) -> int:
    """Count the number of days between two dates."""
    if date2 is None or use_today:
        date2 = datetime.today()
    return abs((date2 - date1).days)

# Parse Date
def parse_date(date_str: str) -> datetime:
    """Parse a date string safely into a datetime object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

# Main Execution
if __name__ == "__main__":
    print("\nDays Counter Between Two Dates\n")

    while True:
        try:
            # First date input
            date1_str = input("Enter the first date (YYYY-MM-DD): ").strip()
            date1 = parse_date(date1_str)

            # Ask if today should be used
            use_today_str = input("Use today's date as the second date? (yes/no): ").strip().lower()

            date2 = None
            use_today = use_today_str in ["yes", "y"]

            if not use_today:
                date2_str = input("Enter the second date (YYYY-MM-DD): ").strip()
                date2 = parse_date(date2_str)

            # Perform calculation
            days_count = count_days(date1, use_today, date2)
            print(f"\nNumber of days between {date1.date()} and {(date2 or datetime.today()).date()}: {days_count} days\n")
            break

        except ValueError as e:
            print(e)
            print("Let's try again...\n")


"""
    # Days Counter Program

    - Implemented functions for counting days and parsing dates to enhance modularity.
    - Added error handling for invalid date formats to improve user experience.
    - Included option to use today's date for flexibility.
    
    Core flow:
        User inputs → validated & parsed → optional use of today’s date → compute difference → print result.
 
"""