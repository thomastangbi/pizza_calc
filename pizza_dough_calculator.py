import streamlit as st
from PIL import Image

st.set_page_config(page_title="Pizza Dough Calculator", page_icon="🍕", layout="centered")

# Load and display logo
logo = Image.open("logo.png")
st.image(logo, use_container_width=True)

st.title("Pizza Dough Calculator")
st.markdown("Quickly calculate how much flour, water, salt, and yeast you need.")

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

if st.button("Calculate"):
    total_weight = number * size
    hydration_ratio = hydration / 100
    salt_ratio = 0.0275
    yeast_ratio = 0.00229

    flour = total_weight / (1 + hydration_ratio + salt_ratio + yeast_ratio)
    water = flour * hydration_ratio
    salt = flour * salt_ratio
    yeast = flour * yeast_ratio

    st.success("Here's what you need:")
    st.write(f"**Flour:** {round(flour)} g")
    st.write(f"**Water:** {round(water)} g")
    st.write(f"**Salt:** {round(salt, 2)} g")
    st.write(f"**Dry Yeast:** {round(yeast, 2)} g")