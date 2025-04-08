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
        "yeast_ratio": 0.002
    },
    "Biga": {
        "function": calculate_biga,  # This one returns a dict with Day 1 & Day 2
        "hydration": 65,
        "salt_ratio": 0.025,
        "yeast_ratio": 0.00065
    }
}

YEAST_TYPES = {
    "Dry": {
        "factor": 1
    },
    "Fresh": {
        "factor": 3
    }
}

dough_type = st.radio("Select dough type:", options=list(DOUGH_TYPES.keys()), index=None)

if dough_type:
    selected_config = DOUGH_TYPES[dough_type]

    st.markdown("---")
    st.subheader("Dough Parameters")

    number = st.number_input("Number of doughballs", min_value=1, value=6, step=1)
    size = st.number_input("Size per doughball (grams)", min_value=100, value=275, step=5)
    hydration = st.slider("Hydration (%)", min_value=50, max_value=100, value=65, step=1)

    # Default ratios from selected dough type
    salt_ratio = selected_config["salt_ratio"]
    yeast_ratio = selected_config["yeast_ratio"]

    use_custom = st.checkbox("⚙️ Advanced Options - Manually set salt and yeast ratios")

    if use_custom:
        yeast_type = st.radio("Yeast type", options=YEAST_TYPES, horizontal=True)
        selected_yeast = YEAST_TYPES[yeast_type]
        yeast_ratio = st.slider(f"{yeast_type} Yeast ratio (%)", min_value=0.0, max_value=0.5, value=yeast_ratio * 100 * selected_yeast["factor"], step=0.01) / 100
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
