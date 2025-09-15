"""
EMI Calculator with Amortization Schedule

This program calculates monthly EMI and generates the amortization schedule
for two types of loans:
1. Reducing Balance (Interest calculated on remaining balance)
2. Flat Rate (Interest calculated on original principal)

The last month EMI is adjusted to ensure total EMI = principal + interest.
"""

# Reducing Balance EMI Functions
def reducing_balance_emi(principal: float, annual_rate: float, tenure_years: int) -> float:
    """
    Calculate EMI for Reducing Balance loan
    """
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    pow_val = (1 + monthly_rate) ** tenure_months
    emi = (principal * monthly_rate * pow_val) / (pow_val - 1)
    return emi 

# Reducing Balance Schedule
def reducing_balance_schedule(principal: float, annual_rate: float, tenure_years: int):
    """
    Generate month-wise amortization schedule for Reducing Balance loan
    Adjust last month EMI to match total principal + interest
    """
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    emi = reducing_balance_emi(principal, annual_rate, tenure_years)

    balance = principal
    schedule = []

    total_principal_paid = 0.0
    total_interest_paid = 0.0

    for month in range(1, tenure_months + 1):
        interest_component = balance * monthly_rate
        principal_component = emi - interest_component

        # Round only for display
        display_interest = round(interest_component, 2)
        display_principal = round(principal_component, 2)
        display_emi = round(display_principal + display_interest, 2)

        # Adjust last month to pay exact principal + interest
        if month == tenure_months:
            display_principal = balance
            display_emi = display_principal + display_interest
            balance = 0.0
        else:
            balance -= principal_component

        schedule.append({
            "Month": month,
            "EMI": display_emi,
            "Interest": display_interest,
            "Principal": display_principal,
            "Balance": round(balance, 2)
        })

        total_principal_paid += display_principal
        total_interest_paid += display_interest

    return schedule


# Flat Rate EMI Functions
def flat_rate_emi(principal: float, annual_rate: float, tenure_years: int) -> float:
    """
    Calculate EMI for Flat Rate loan
    """
    total_interest = principal * annual_rate / 100 * tenure_years
    total_repayment = principal + total_interest
    emi = total_repayment / (tenure_years * 12)
    return emi

# Flat Rate Schedule
def flat_rate_schedule(principal: float, annual_rate: float, tenure_years: int):
    """
    Generate month-wise amortization schedule for Flat Rate loan
    Adjust last month EMI to match total principal + total interest exactly
    """
    months = tenure_years * 12
    total_interest = principal * annual_rate / 100 * tenure_years
    monthly_principal = principal / months
    monthly_interest = total_interest / months

    balance = principal
    schedule = []

    for month in range(1, months + 1):
        if month == months:
            display_principal = balance  # pay off remaining principal exactly
            # Calculate remaining interest to match total_interest
            sum_interest_so_far = sum(entry['Interest'] for entry in schedule)
            display_interest = total_interest - sum_interest_so_far
            display_emi = display_principal + display_interest
            balance = 0.0
        else:
            display_principal = monthly_principal
            display_interest = monthly_interest
            display_emi = display_principal + display_interest
            balance -= display_principal

        # Round only for display
        schedule.append({
            "Month": month,
            "EMI": round(display_emi, 2),
            "Interest": round(display_interest, 2),
            "Principal": round(display_principal, 2),
            "Balance": round(balance, 2)
        })

    return schedule

# Reducing Balance & Flat Rate EMI Comparison
def compare_loans(principal: float, annual_rate: float, tenure_years: int) -> dict:
    """
    Compare Reducing Balance and Flat Rate loans side-by-side.
    
    Returns a dictionary containing:
    - Month-wise schedules for both loans
    - Totals for EMI, interest, and principal
    - Interest saved by using Reducing Balance
    """
    # Generate schedules
    rb_schedule = reducing_balance_schedule(principal, annual_rate, tenure_years)
    fr_schedule = flat_rate_schedule(principal, annual_rate, tenure_years)

    # Calculate totals
    rb_total_emi = sum(entry['EMI'] for entry in rb_schedule)
    rb_total_interest = sum(entry['Interest'] for entry in rb_schedule)
    fr_total_emi = sum(entry['EMI'] for entry in fr_schedule)
    fr_total_interest = sum(entry['Interest'] for entry in fr_schedule)

    interest_saved = fr_total_interest - rb_total_interest

    # Return all data in structured format
    return {
        "principal": principal,
        "reducing_balance": {
            "schedule": rb_schedule,
            "total_emi": rb_total_emi,
            "total_interest": rb_total_interest,
            "total_principal": principal
        },
        "flat_rate": {
            "schedule": fr_schedule,
            "total_emi": fr_total_emi,
            "total_interest": fr_total_interest,
            "total_principal": principal
        },
        "interest_saved": interest_saved
    }


# Helper Function to print the comparison data
def print_loan_comparison(data: dict):
    """
    Print a clean, month-wise comparison table for Reducing Balance and Flat Rate loans.
    Expects the dictionary returned by compare_loans().
    """
    rb_schedule = data["reducing_balance"]["schedule"]
    fr_schedule = data["flat_rate"]["schedule"]

    # Header
    print("\nMonth-wise EMI Comparison (Reducing Balance vs Flat Rate):")
    print(f"{'Month':<6}{'RB EMI':<10}{'RB Interest':<12}{'RB Principal':<12}"
          f"{'FR EMI':<10}{'FR Interest':<12}{'FR Principal':<12}")

    # Month-wise data
    for m in range(len(rb_schedule)):
        rb = rb_schedule[m]
        fr = fr_schedule[m]
        print(f"{m+1:<6}{rb['EMI']:<10.2f}{rb['Interest']:<12.2f}{rb['Principal']:<12.2f}"
              f"{fr['EMI']:<10.2f}{fr['Interest']:<12.2f}{fr['Principal']:<12.2f}")

    # Totals
    rb_total_emi = data["reducing_balance"]["total_emi"]
    rb_total_interest = data["reducing_balance"]["total_interest"]
    fr_total_emi = data["flat_rate"]["total_emi"]
    fr_total_interest = data["flat_rate"]["total_interest"]
    principal = data["principal"]

    print("\nTOTALS:")
    print(f"{'Type':<15}{'Total EMI':<12}{'Total Interest':<15}{'Total Principal':<15}")
    print(f"{'Reducing Balance':<15}{rb_total_emi:<12.2f}{rb_total_interest:<15.2f}{principal:<15.2f}")
    print(f"{'Flat Rate':<15}{fr_total_emi:<12.2f}{fr_total_interest:<15.2f}{principal:<15.2f}")

    # Interest saved
    print("\nInterest saved with Reducing Balance:", round(data["interest_saved"], 2))



# Main Execution
if __name__ == "__main__":
    print("\nEMI Calculator with Amortization Schedule\n")

    while True:
        try:
            loan_type = input("Choose loan type - (1) Reducing Balance or (2) Flat Rate: ").strip()
            if loan_type not in ['1', '2']:
                print("Invalid choice. Please enter 1 or 2.")
                continue

            principal = float(input("Enter the loan amount (principal): ").strip())
            annual_rate = float(input("Enter the annual interest rate (in %): ").strip())
            tenure_years = int(input("Enter the tenure (in years): ").strip())

            # Select loan type
            if loan_type == '1':
                schedule = reducing_balance_schedule(principal, annual_rate, tenure_years)
                loan_name = "Reducing Balance"
            else:
                schedule = flat_rate_schedule(principal, annual_rate, tenure_years)
                loan_name = "Flat Rate"

            # Display amortization schedule
            print(f"\nLoan Type: {loan_name}")
            print(f"Monthly EMI (approx): ₹{round(schedule[0]['EMI'], 2):,.2f}\n")
            print(f"{'Month':<6}{'EMI':<12}{'Interest':<12}{'Principal':<12}{'Balance':<12}")

            total_emi = 0.0
            total_principal = 0.0
            total_interest = 0.0

            for entry in schedule:
                print(f"{entry['Month']:<6}{entry['EMI']:<12.2f}{entry['Interest']:<12.2f}"
                      f"{entry['Principal']:<12.2f}{entry['Balance']:<12.2f}")
                total_emi += entry['EMI']
                total_principal += entry['Principal']
                total_interest += entry['Interest']

            # Totals
            print("-" * 54)
            print(f"{'Total':<6}{total_emi:<12.2f}{total_interest:<12.2f}{total_principal:<12.2f}{'-':<12}")
            
            # Get comparison data
            # data = compare_loans(principal, annual_rate, tenure_years)

            # Print the comparison table
            # print_loan_comparison(data)

            break

        except ValueError:
            print("Invalid input. Please enter numeric values.\n")


"""
    Summary:
    This script calculates the monthly EMI and generates an amortization schedule for both Reducing Balance and Flat Rate loans.
    Key features:
    - Supports different loan types with distinct interest calculation methods.
    - Provides detailed month-wise breakdown of EMI, interest, principal, and remaining balance.
    - Calculates total payment summaries, including interest saved with Reducing Balance loans.
    - User-friendly input prompts and error handling for a smooth experience.
    Core flow:
        Input loan details → calculate EMI → generate amortization schedule → display results.
"""