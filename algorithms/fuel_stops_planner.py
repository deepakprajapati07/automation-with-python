# Fuel Stops Planner

import math
from typing import Dict, List

def plan_fuel_stops(distance: float, mileage: float, tank_capacity: float, fuel_price: float) -> Dict:
    """
    Calculate fuel stops for a long trip.

    Args:
        distance (float): Total trip distance in km.
        mileage (float): Vehicle mileage in km per liter.
        tank_capacity (float): Fuel tank capacity in liters.
        fuel_price (float): Price per liter of fuel.

    Returns:
        dict: fuel_needed (L), total_cost (currency), refuels (count), stop_points (km marks).
    """

    # --- 1. Validations ---
    if distance <= 0 or mileage <= 0 or tank_capacity <= 0 or fuel_price < 0:
        raise ValueError("Inputs must be positive numbers.")

    # --- 2. Core calculations ---
    max_range = mileage * tank_capacity
    fuel_needed = distance / mileage
    total_cost = fuel_needed * fuel_price

    # --- 3. Refuels and stop points ---
    if distance <= max_range:
        refuels = 0
        stop_points: List[float] = []
    else:
        refuels = math.ceil(distance / max_range) - 1
        stop_points = [min(i * max_range, distance) for i in range(1, refuels + 1)]

    # --- 4. Structured output ---
    return {
        "fuel_needed": round(fuel_needed, 2),
        "total_cost": round(total_cost, 2),
        "refuels": refuels,
        "stop_points": stop_points
    }

# Main Execution
if __name__ == "__main__":
    trip_info = plan_fuel_stops(
        distance=3500, 
        mileage=25, 
        tank_capacity=50, 
        fuel_price=100
    )
    print(trip_info)
    
"""
    Summary:
    This script calculates the fuel requirements and refueling stops for a long-distance trip.
    Key features:
    - Calculates total fuel needed and cost based on distance, mileage, tank capacity, and fuel price.
    - Determines the number of refueling stops and their locations along the route.
    Core flow:
        Input parameters → validate → calculate fuel needs and stops → output results.
    Dependencies:
    - math
    - typing
     Core flow:   
        Input parameters → validate → calculate fuel needs and stops → output results.
    Dependencies:
    - math
    - typing
"""