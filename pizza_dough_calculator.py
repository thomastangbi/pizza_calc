import streamlit as st

st.set_page_config(page_title="Pizza Dough Calculator", page_icon="🍕")

st.title("🍕 Pizza Dough Calculator")

st.markdown("Calculate how much flour, water, yeast, and salt you need for your pizza night!")

number = st.number_input("Number of Doughballs", min_value=1, value=6)
size = st.number_input("Size per Doughball (grams)", min_value=50, value=275)
hydration = st.slider("Hydration (%)", min_value=50, max_value=100, value=65)

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