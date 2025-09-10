# BMI Calculator

INCH_TO_METER = 0.0254  # Conversion factor from inches to meters

# BMI Heath Categories
bmi_categories = {
    "Underweight": (0, 18.4),
    "Normal weight": (18.5, 24.9),
    "Overweight": (25, 29.9),
    "Obesity": (30, float('inf'))
}

def calculate_bmi(weight_kg: float, height_feet: int = None, height_inches: int = None, height_cm: int = None) -> float:
    """Calculate Body Mass Index (BMI) given weight in kilograms and height in feet and inches."""
    if height_cm is not None:
        height_m = height_cm / 100
    else:
        height_m = (height_feet * 12 + height_inches) * INCH_TO_METER

    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi: float) -> str:
    """Determine the BMI category based on the BMI value."""
    for category, (low, high) in bmi_categories.items():
        if low <= bmi <= high:
            return category
    return "Unknown"

# Main Execution
if __name__ == "__main__":
    print("\nBMI Calculator\n")

    while True:
        try:
            # Weight input
            weight_str = input("Enter your weight in kilograms (e.g., 70.5): ").strip()
            weight_kg = float(weight_str)

            # Height input
            height_unit = input("Do you want to enter height in (1) feet and inches or (2) centimeters? Enter 1 or 2: ").strip()
            if height_unit == '1':
                height_in_cm = False
                feet_str = input("Enter your height - feet part (e.g., 5): ").strip()
                inches_str = input("Enter your height - inches part (e.g., 10): ").strip()
                height_feet = int(feet_str)
                height_inches = int(inches_str)
                height_cm = None
            elif height_unit == '2':
                height_in_cm = True
                cm_str = input("Enter your height in centimeters (e.g., 175): ").strip()
                height_cm = int(cm_str)
                height_feet = None
                height_inches = None
            else:
                raise ValueError("Invalid choice for height unit. Please enter 1 or 2.")

            # Perform calculation
            bmi = calculate_bmi(weight_kg, height_feet, height_inches, height_cm)
            print(f"\nYour BMI is: {bmi}\n")
            category = get_bmi_category(bmi)
            print(f"You are classified as: {category}\n")
            break

        except ValueError as e:
            print(e)
            print("Let's try again...\n")