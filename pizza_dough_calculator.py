import streamlit as st
from PIL import Image

st.set_page_config(page_title="Pizza Dough Calculator", page_icon="🍕", layout="centered")

# Load and display logo
logo = Image.open("logo.png")
# st.image(logo, use_container_width=True)

st.title("Pizza Dough Calculator")
st.markdown("Easily calculate how much flour, water, salt, and yeast you need.")

st.markdown("""
<style>
    /* Center everything nicely and keep the aesthetic clean */
    .main {
        font-family: 'Georgia', serif;
        color: #111;
    }

    h1, h2, h3 {
        color: #000;
        font-weight: 700;
    }

    /* Style the button like it's from a vintage bakery */
    .stButton > button {
        background-color: #000000;
        color: white;
        border: none;
        padding: 0.5em 1.5em;
        font-size: 16px;
        font-weight: bold;
        border-radius: 0;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #333;
    }

    /* Optional: hide Streamlit’s default menu and footer */
    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Initialize variablers
number = 0
size = 0
hydration = 0
salt_ratio = 0.0275
yeast_ratio = 0.0023
selected_config = 0

#
def calculate_yeast_percentage(duration_hours, yeast_type="fresh"):
    base_ratio = 0.25 / (duration_hours ** 0.5)
    if yeast_type == "dry":
        return round(base_ratio * 0.33, 4)
    return round(base_ratio, 4)

# Define dough type calculations 
def calculate_neapolitan(number, size, hydration, salt_ratio, yeast_ratio):
    total_weight = number * size
    hydration_ratio = hydration / 100

    flour = total_weight / (1 + hydration_ratio + salt_ratio + yeast_ratio)
    water = flour * hydration_ratio
    salt = flour * salt_ratio
    yeast = flour * yeast_ratio

    return round(flour), round(water), round(salt, 2), round(yeast, 2)    

def calculate_biga(number, size, hydration, salt_ratio, yeast_ratio):
    # Total dough weight
    total_weight = number * size
    hydration_ratio = hydration / 100

    flour = total_weight / (1 + hydration_ratio + salt_ratio + yeast_ratio)
    water = flour * hydration_ratio
    salt = flour * salt_ratio

    # Biga hydration is typically lower (~50%)
    biga_hydration = 0.5
    yeast_ratio_day1 = 0.002
    yeast_ratio_day2 = 0.0005

    # Let's say 40% of the flour goes into the biga
    flour_biga = flour
    water_biga = flour_biga * biga_hydration
    yeast_biga = flour_biga * yeast_ratio_day1

    # Remaining flour for day 2
    water_day2 = water - water_biga
    salt_day2 = salt
    yeast_day2 = flour * yeast_ratio_day2

    return {
        "Day 1 - Biga": {
            "Flour": round(flour_biga),
            "Water": round(water_biga),
            "Yeast": round(yeast_biga, 2)
        },
        "Day 2 - Final Dough": {
            "Water": round(water_day2),
            "Salt": round(salt_day2, 2),
            "Yeast": round(yeast_day2, 2)
        }
    }

DOUGH_TYPES = {
    "Neapolitan": {
        "function": calculate_neapolitan,
        "hydration": 50,
        "salt_ratio": 0.025,
        "yeast_ratio": 0.002,
        "yeast_factor": {
            "Dry": 1,
            "Fresh": 3
        },
        "fermentation": 48
    },
    "Biga": {
        "function": calculate_biga,  # This one returns a dict with Day 1 & Day 2
        "hydration": 65,
        "salt_ratio": 0.025,
        "yeast_ratio": 0.00065,
        "yeast_factor": {
            "Dry": 1,
            "Fresh": 3
        }
    }
}

dough_type = st.radio("Select dough type:", options=list(DOUGH_TYPES.keys()), index=None)

if dough_type:
    selected_config = DOUGH_TYPES[dough_type]
    yeast_types = selected_config["yeast_factor"]


    st.markdown("---")
    st.subheader("Dough Parameters")

    number = st.number_input("Number of doughballs", min_value=1, value=6, step=1)
    size = st.number_input("Size per doughball (grams)", min_value=100, value=275, step=5)
    hydration = st.slider("Hydration (%)", min_value=50, max_value=100, value=65, step=1)

    # Default ratios from selected dough type
    salt_ratio = selected_config["salt_ratio"]
    yeast_ratio = selected_config["yeast_ratio"]

    use_custom = st.checkbox("⚙️ Advanced Options")

    if use_custom:

        if selected_config["fermentation"]:
            fermentation_duration = st.slider("Fermentation (Hours)", min_value=8, max_value=96, value=selected_config["fermentation"], step=8)
        else:
            fermentation_duration = 1

        yeast_type = st.radio("Yeast type", options=yeast_types, horizontal=True)
        if yeast_type == "Fresh":
            yeast_factor = yeast_types["Fresh"]
        else:
            yeast_factor = yeast_types["Dry"]

        yeast_ratio = st.slider(f"{yeast_type} Yeast ratio (%)", min_value=0.0, max_value=0.5, value=yeast_ratio * 100 * yeast_factor, step=0.01) / 100
        salt_ratio = st.slider("Salt ratio (%)", min_value=1.0, max_value=3.5, value=salt_ratio * 100, step=0.1) / 100

    if st.button("Calculate"):
        func = selected_config["function"]

        if func == calculate_neapolitan:
            flour, water, salt, yeast = func(number, size, hydration, salt_ratio, yeast_ratio)
            st.success("Your ingredients:")
            st.write(f"**Flour:** {flour} g")
            st.write(f"**Water:** {water} g")
            st.write(f"**Salt:** {salt} g")
            st.write(f"**Dry Yeast:** {yeast} g")
        elif func == calculate_biga:
            result = func(number, size, hydration, salt_ratio, yeast_ratio)
            for day, components in result.items():
                st.subheader(day)
                for k, v in components.items():
                    st.write(f"**{k}:** {v} g")
