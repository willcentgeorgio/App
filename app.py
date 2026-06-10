import streamlit as st

st.set_page_config(page_title="Nutritional Needs Calculator", page_icon="🍎")

st.title("🍎 Daily Nutritional Needs Calculator")
st.write("Enter your details below to calculate your custom daily targets.")

# 1. User Inputs via Streamlit Widgets (Validation is handled automatically)
weight_kg = st.number_input("Enter your weight in kilograms (e.g., 70):", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
height_cm = st.number_input("Enter your height in centimeters (e.g., 175):", min_value=50.0, max_value=250.0, value=175.0, step=0.1)
age = st.number_input("Enter your age in years (e.g., 30):", min_value=10, max_value=100, value=30, step=1)
gender_input = st.radio("Enter your gender:", ['Male', 'Female'])
gender = gender_input.lower()

# Activity level mapping matching your dictionary logic
activity_options = {
    "Sedentary (little to no exercise)": 1.2,
    "Light (light exercise/sports 1-3 days/week)": 1.375,
    "Moderate (moderate exercise/sports 3-5 days/week)": 1.55,
    "Active (hard exercise/sports 6-7 days/week)": 1.725,
    "Very Active (very hard exercise/physical job)": 1.9
}
activity_choice = st.selectbox("Select your physical activity level:", list(activity_options.keys()))
activity_level_multiplier = activity_options[activity_choice]

# 3. Core Calculations - Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
if gender == 'male':
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
else:  # female
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

# Total Daily Energy Expenditure (TDEE)
tdee = bmr * activity_level_multiplier

# 2. Goal Selection mapping matching your original options
goal_options = {
    "Build Muscle Mass (Caloric Surplus)": 1,
    "Maintain Muscle Mass (Maintenance Calories)": 2,
    "Lose Body Fat (Caloric Deficit)": 3
}
goal_choice_text = st.selectbox("Select your fitness goal:", list(goal_options.keys()))
goal_choice = goal_options[goal_choice_text]

target_calories = tdee
goal_description = "Maintenance"

if goal_choice == 1:
    target_calories += 400  # Average surplus of +300 to +500
    goal_description = "Muscle Building"
elif goal_choice == 3:
    target_calories -= 400  # Average deficit of -300 to -500
    goal_description = "Fat Loss"

# Ensure target calories do not go below a healthy minimum
min_calories = 1500 if gender == 'male' else 1200
if target_calories < min_calories:
    st.warning(f"Warning: Calculated target calories ({int(target_calories)}) are below recommended minimum of {min_calories}. Adjusting to {min_calories}.")
    target_calories = min_calories

# 4. Macro & Micro Breakdown (Your original logic)
protein_grams = round(1.8 * weight_kg, 2)
protein_calories = protein_grams * 4

fat_percentage = 0.28
fat_calories = target_calories * fat_percentage
fat_grams = round(fat_calories / 9, 2)

remaining_calories_for_carbs = target_calories - protein_calories - fat_calories
if remaining_calories_for_carbs < 0:
    remaining_calories_for_carbs = 0
carb_grams = round(remaining_calories_for_carbs / 4, 2)

fiber_grams = round((target_calories / 1000) * 14, 2)

# 5. Output Web Formatting
st.markdown("---")
st.header("🎯 NUTRITIONAL SUMMARY")

# Display your profile info
st.markdown(f"**Gender:** {gender.capitalize()} | **Age:** {age} years | **Weight:** {weight_kg:.1f} kg | **Height:** {height_cm:.1f} cm")
st.markdown(f"**Goal:** {goal_description}")
st.markdown("---")

# Key metrics shown side-by-side
col1, col2, col3 = st.columns(3)
col1.metric("BMR (Calories)", f"{int(bmr)}")
col2.metric("TDEE (Calories)", f"{int(tdee)}")
col3.metric("Target Daily Calories", f"{int(target_calories)}")

st.markdown("---")
st.subheader("Daily Macronutrient Breakdown:")

# Display macros beautifully with bullet points or custom text blocks
st.write(f"🧬 **Protein:** {protein_grams:.1f} grams ({int(protein_calories)} calories)")
st.write(f"🥑 **Fats:** {fat_grams:.1f} grams ({int(fat_calories)} calories)")
st.write(f"🍞 **Carbohydrates:** {carb_grams:.1f} grams ({int(remaining_calories_for_carbs)} calories)")
st.write(f"🥗 **Fiber:** {fiber_grams:.1f} grams (general guideline)")

st.markdown("---")
st.caption("Note: These are estimated values. Individual needs may vary. Consult a healthcare professional or registered dietitian for personalized advice.")
