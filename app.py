import streamlit as st
import json
from collections import defaultdict

# Load recipes
def load_recipes():
    with open("recipes.json", "r") as f:
        return json.load(f)

# Load planner
def load_planner():
    with open("planner.json", "r") as f:
        return json.load(f)

# Save planner
def save_planner(planner):
    with open("planner.json", "w") as f:
        json.dump(planner, f, indent=2)

# Aggregate ingredients
def generate_shopping_list(planner, recipes):
    shopping_list = defaultdict(list)
    recipe_dict = {r["name"]: r["ingredients"] for r in recipes}
    for day, dish in planner.items():
        if dish and dish in recipe_dict:
            for ingredient in recipe_dict[dish]:
                shopping_list[ingredient["item"]].append(ingredient["quantity"])
    return shopping_list

# App layout
st.title("🍽️ Weekly Dinner Planner")

recipes = load_recipes()
planner = load_planner()
recipe_names = [r["name"] for r in recipes]

st.header("📅 Plan Your Week")

for day in planner:
    # search_term = st.text_input(f"Search recipe for {day}", "")
    # filtered_recipes = [r for r in recipe_names if search_term.lower() in r.lower()]
    planner[day] = st.selectbox(f"{day}", [""] + recipe_names)

if st.button("Save Plan"):
    save_planner(planner)
    st.success("Planner saved!")

st.header("🛒 Shopping List")
shopping_list = generate_shopping_list(planner, recipes)
for item, quantities in shopping_list.items():
    st.write(f"- {item}: {', '.join(quantities)}")
