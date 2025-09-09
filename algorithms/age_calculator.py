# Age Calculator -> calculate age based on birthdate
from datetime import datetime
from typing import Tuple
from dateutil.relativedelta import relativedelta
from utils.date_parser import parse_date

def calculate_age(birthdate: datetime) -> Tuple[int, int, int]:
    """Calculate age in years, months, and days from the birthdate to today."""
    today = datetime.today()
    diff = relativedelta(today, birthdate)
    return diff.years, diff.months, diff.days

# Main Execution
if __name__ == "__main__":
    print("\nAge Calculator Based on Birthdate\n")

    while True:
        try:
            # Birthdate input
            birthdate_str = input("Enter your birthdate (YYYY-MM-DD): ").strip()
            birthdate = parse_date(birthdate_str)

            # Perform calculation
            years, months, days = calculate_age(birthdate)
            print(f"\nYou are {years} years, {months} months, and {days} days old.\n")
            break

        except ValueError as e:
            print(e)
            print("Let's try again...\n")