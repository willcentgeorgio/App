# App
import sys

def get_valid_input(prompt, type_func, validation_func=None, error_message="Invalid input. Please try again."):
    """Helper function to get validated user input."""
    while True:
        try:
            value = type_func(input(prompt))
            if validation_func and not validation_func(value):
                print(error_message)
            else:
                return value
        except ValueError:
            print(error_message)

def calculate_nutritional_needs():
    """Calculates and displays a user's daily nutritional needs."""
    print("--- Daily Nutritional Needs Calculator ---")

    # 1. User Inputs
    # Using helper function for robust input
    weight_kg = get_valid_input(
        "Enter your weight in kilograms (e.g., 70): ",
        float,
        lambda x: x > 0,
        "Weight must be a positive number."
    )
    height_cm = get_valid_input(
        "Enter your height in centimeters (e.g., 175): ",
        float,
        lambda x: x > 0,
        "Height must be a positive number."
    )
    age = get_valid_input(
        "Enter your age in years (e.g., 30): ",
        int,
        lambda x: 10 <= x <= 100,
        "Age must be between 10 and 100."
    )
    gender = get_valid_input(
        "Enter your gender (male/female): ",
        str,
        lambda x: x.lower() in ['male', 'female'],
        "Gender must be 'male' or 'female'."
    ).lower()

    print("\nSelect your physical activity level:")
    print("  1. Sedentary (little to no exercise)")
    print("  2. Light (light exercise/sports 1-3 days/week)")
    print("  3. Moderate (moderate exercise/sports 3-5 days/week)")
    print("  4. Active (hard exercise/sports 6-7 days/week)")
    print("  5. Very Active (very hard exercise/physical job)")

    activity_choice = get_valid_input(
        "Enter the number corresponding to your activity level: ",
        int,
        lambda x: 1 <= x <= 5,
        "Please enter a number between 1 and 5."
    )

    activity_multipliers = {
        1: 1.2,   # Sedentary
        2: 1.375, # Light
        3: 1.55,  # Moderate
        4: 1.725, # Active
        5: 1.9    # Very Active
    }
    activity_level_multiplier = activity_multipliers[activity_choice]

    # 3. Core Calculations - Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
    if gender == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:  # female
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Total Daily Energy Expenditure (TDEE)
    tdee = bmr * activity_level_multiplier

    # 2. Goal Selection
    print("\nSelect your fitness goal:")
    print("  1. Build Muscle Mass (Caloric Surplus)")
    print("  2. Maintain Muscle Mass (Maintenance Calories)")
    print("  3. Lose Body Fat (Caloric Deficit)")

    goal_choice = get_valid_input(
        "Enter the number corresponding to your goal: ",
        int,
        lambda x: 1 <= x <= 3,
        "Please enter a number between 1 and 3."
    )

    target_calories = tdee
    goal_description = "Maintenance"

    if goal_choice == 1:
        target_calories += 400  # Average surplus of +300 to +500
        goal_description = "Muscle Building"
    elif goal_choice == 3:
        target_calories -= 400  # Average deficit of -300 to -500
        goal_description = "Fat Loss"

    # Ensure target calories do not go below a healthy minimum (e.g., 1200 for women, 1500 for men)
    min_calories = 1500 if gender == 'male' else 1200
    if target_calories < min_calories:
        print(f"\nWarning: Calculated target calories ({int(target_calories)}) are below recommended minimum of {min_calories}. Adjusting to {min_calories}.")
        target_calories = min_calories

    # 4. Macro & Micro Breakdown
    # Protein: 1.8g per kg of body weight (average of 1.6-2.2g)
    protein_grams = round(1.8 * weight_kg, 2)
    protein_calories = protein_grams * 4

    # Fats: 25-30% of total target calories (using 28% as an average)
    fat_percentage = 0.28
    fat_calories = target_calories * fat_percentage
    fat_grams = round(fat_calories / 9, 2)

    # Carbohydrates: Remaining calories
    remaining_calories_for_carbs = target_calories - protein_calories - fat_calories
    # Ensure carbs are not negative if target calories are very low
    if remaining_calories_for_carbs < 0:
        remaining_calories_for_carbs = 0
    carb_grams = round(remaining_calories_for_carbs / 4, 2)

    # Fiber: General guideline (e.g., 14g per 1000 calories)
    fiber_grams = round((target_calories / 1000) * 14, 2)

    # 5. Output formatting
    print("\n" + "="*40)
    print("           NUTRITIONAL SUMMARY")
    print("="*40)
    print(f"Gender: {gender.capitalize()}")
    print(f"Age: {age} years")
    print(f"Weight: {weight_kg:.1f} kg")
    print(f"Height: {height_cm:.1f} cm")
    print(f"Goal: {goal_description}")
    print("-"*40)
    print(f"Basal Metabolic Rate (BMR):   {int(bmr)} calories")
    print(f"Total Daily Energy Expenditure (TDEE): {int(tdee)} calories")
    print(f"Target Daily Calories:        {int(target_calories)} calories")
    print("-"*40)
    print("Daily Macronutrient Breakdown:")
    print(f"  Protein:     {protein_grams:.1f} grams ({int(protein_calories)} calories)")
    print(f"  Fats:        {fat_grams:.1f} grams ({int(fat_calories)} calories)")
    print(f"  Carbohydrates: {carb_grams:.1f} grams ({int(remaining_calories_for_carbs)} calories)")
    print(f"  Fiber:       {fiber_grams:.1f} grams (general guideline)")
    print("="*40)
    print("Note: These are estimated values. Individual needs may vary.")
    print("Consult a healthcare professional or registered dietitian for personalized advice.")

# Run the calculator
calculate_nutritional_needs()
