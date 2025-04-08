import streamlit as st
from PIL import Image

st.set_page_config(page_title="Pizza Dough Calculator", page_icon="🍕", layout="centered")

# Load and display logo
logo = Image.open("logo.png")
st.image(logo, use_container_width=True)

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

number = st.number_input("Number of Doughballs", min_value=1, value=6, step=1)
size = st.number_input("Size per Doughball (grams)", min_value=50, value=275, step=1)
hydration = st.slider("Hydration (%)", min_value=50, max_value=100, value=65, step=1)
salt_ratio = 0.0275
yeast_ratio = 0.0023

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
        "salt_ratio": 0.0275,
        "yeast_ratio": 0.0023
    },
    "Biga": {
        "function": calculate_biga,  # This one returns a dict with Day 1 & Day 2
        "hydration": 65,
        "salt_ratio": 0.0275,
        "yeast_ratio": 0.0023
    }
}

dough_type = st.selectbox("Choose dough type", list(DOUGH_TYPES.keys()))

if st.button("Calculate"):
    selected = DOUGH_TYPES[dough_type]
    func = selected["function"]

    result = func(number, size, hydration, salt_ratio, yeast_ratio)

    # Handle Biga (multi-day structure)
    if isinstance(result, dict) and "Day 1 - Biga" in result:
        for day, components in result.items():
            st.subheader(day)
            for k, v in components.items():
                st.write(f"**{k}:** {v} g")
    else:
        # Handle standard return tuple: (flour, water, salt, yeast)
        flour, water, salt, yeast = result
        st.success("Your ingredients:")
        st.write(f"**Flour:** {flour} g")
        st.write(f"**Water:** {water} g")
        st.write(f"**Salt:** {salt} g")
        st.write(f"**Dry Yeast:** {yeast} g")