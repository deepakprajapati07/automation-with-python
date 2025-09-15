# Simple & Compound Interest Calculator with Yearly Breakdown

import math

def simple_interest(principal: float, rate: float, time: int):
    """
    Calculate Simple Interest and Total Amount with yearly breakdown.

    Args:
        principal (float): Principal amount
        rate (float): Annual interest rate in %
        time (int): Time in years

    Returns:
        si (float): Final Simple Interest
        total (float): Final Total Amount
        breakdown (list of dict): Year-wise breakdown
    """
    breakdown = []
    yearly_increment = (principal * rate) / 100   # interest earned per year
    running_interest = 0
    total = principal  # start with principal

    for year in range(1, time + 1):
        running_interest += yearly_increment
        total = principal + running_interest
        breakdown.append({
            "Year": year,
            "Interest": running_interest,
            "Total": total
        })

    # After the loop, final SI and total are just the last entries
    si = running_interest
    return si, total, breakdown


def compound_interest(principal: float, rate: float, time: int, n: int = 1):
    """
    Calculate Compound Interest and Total Amount with yearly breakdown.

    Args:
        principal (float): Principal amount
        rate (float): Annual interest rate in %
        time (int): Time in years
        n (int): Number of times interest is compounded per year (default=1)

    Returns:
        ci (float): Final Compound Interest
        total (float): Final Total Amount
        breakdown (list of dict): Year-wise breakdown
    """
    breakdown = []
    total = principal
    periodic_rate = rate / (100 * n)  # rate per compounding period

    for year in range(1, time + 1):
        # Apply compounding n times for each year
        for _ in range(n):
            total *= (1 + periodic_rate)

        ci = total - principal
        breakdown.append({
            "Year": year,
            "Interest": ci,
            "Total": total
        })

    # After loop ends, CI and Total come from last iteration
    return ci, total, breakdown

# Main Execution
if __name__ == "__main__":
    print("\nInterest Calculator with Yearly Breakdown\n")
    while True:
        try:
            principal = float(input("Enter the principal amount: ").strip())
            rate = float(input("Enter the annual interest rate (in %): ").strip())
            time = int(input("Enter the time in years: ").strip())
            interest_type = input("Choose interest type - (1) Simple Interest or (2) Compound Interest: ").strip()

            if interest_type == '1':
                si, total, breakdown = simple_interest(principal, rate, time)
                print(f"\nSimple Interest: {si:.2f}")
                print(f"Total Amount after {time} years: {total:.2f}")
                print("\nYearly Breakdown:")
                for row in breakdown:
                    print(f"Year {row['Year']}: Interest = {row['Interest']:.2f}, Total = {row['Total']:.2f}")

            elif interest_type == '2':
                n = int(input("Enter number of times interest is compounded per year (e.g., 1 for yearly, 4 for quarterly): ").strip())
                ci, total, breakdown = compound_interest(principal, rate, time, n)
                print(f"\nCompound Interest: {ci:.2f}")
                print(f"Total Amount after {time} years: {total:.2f}")
                print("\nYearly Breakdown:")
                for row in breakdown:
                    print(f"Year {row['Year']}: Interest = {row['Interest']:.2f}, Total = {row['Total']:.2f}")

            else:
                print("Invalid choice. Please enter 1 or 2.")
                continue

            break

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.\n")

"""
Summary:
This script calculates simple and compound interest with a yearly breakdown.
Key features:
- Calculates total interest and final amount for both simple and compound interest.
- Provides a detailed year-wise breakdown of interest and total amount.
Core flow:
    Input parameters → validate → calculate interest → generate breakdown → display results.
Dependencies:
- math
- typing
"""