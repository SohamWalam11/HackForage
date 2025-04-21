import streamlit as st
import os
import matplotlib.pyplot as plt
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Sustainable Energy Tracker", layout="centered")

# --- Load Custom CSS ---
css_path = "style.css"  # Make sure this path is correct if it's in the same folder as the app
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("CSS file not found. Make sure the path is correct.")

# --- Session State for Navigation ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- Navbar HTML ---
st.markdown("""
    <div class="navbar">
        <a href="/?page=home">Home</a>
        <a href="/?page=tracker">Tracker</a>
        <a href="/?page=about">About</a>
    </div>
""", unsafe_allow_html=True)

# --- Get Page from Query ---
query_params = st.query_params
if 'page' in query_params:
    st.session_state.page = query_params['page']

# --- Tracker Page ---
def tracker_page():
    st.title("📊 Energy Tracker")

    username = st.text_input("Enter your name:")

    st.header("🏠 Household Appliances")
    home_appliances = {
        "Refrigerator": 20,
        "Air Conditioner": 30,
        "Clothes Dryer": 25,
        "Washing Machine": 15,
        "Dishwasher": 10,
        "Microwave": 5,
        "Water Heater": 18
    }
    selected_home_appliances = st.multiselect("Select Household Appliances", list(home_appliances.keys()))
    home_expenses = {
        appliance: st.number_input(f"{appliance} (₹/month)", min_value=0.0, step=100.0)
        for appliance in selected_home_appliances
    }

    st.header("💻 Electronics")
    electronics = {
        "Laptop": 8,
        "TV": 12,
        "Gaming Console": 10,
        "Desktop Computer": 15,
        "Smartphone": 5,
        "Printer": 2,
        "Router": 3
    }
    selected_electronics = st.multiselect("Select Electronics", list(electronics.keys()))
    electronic_expenses = {
        electronic: st.number_input(f"{electronic} (₹/month)", min_value=0.0, step=100.0)
        for electronic in selected_electronics
    }

    st.header("🚗 Vehicle Fuel Expenses")
    selected_fuels = st.multiselect("Select the fuel types you use:", ["Petrol", "Diesel", "CNG", "LPG"])
    fuel_emission_factors = {
        'Petrol': 2.31 / 10,
        'Diesel': 2.68 / 10,
        'CNG': 1.90 / 10,
        'LPG': 1.51 / 10
    }
    fuel_costs = {
        fuel: st.number_input(f"{fuel} (₹/month)", min_value=0.0, step=100.0)
        for fuel in selected_fuels
    }

    # --- Sustainability Factor (Green Offset Percentage) Slider ---
    sustainability_factor = st.slider(
        "Select your Sustainability Factor (%)", 
        min_value=0, max_value=100, step=1, value=10
    )

    # --- Calculations ---
    home_appliance_emissions = sum(home_expenses[appliance] * home_appliances[appliance] / 1000 for appliance in selected_home_appliances)
    electronic_emissions = sum(electronic_expenses[el] * electronics[el] / 1000 for el in selected_electronics)
    vehicle_emissions = sum(fuel_costs[fuel] * fuel_emission_factors[fuel] for fuel in selected_fuels)

    total_co2 = home_appliance_emissions + electronic_emissions + vehicle_emissions
    green_offset = total_co2 * (sustainability_factor / 100)  # Adjusted green offset based on slider

    # --- Display Results ---
    if username and (any(home_expenses.values()) or any(electronic_expenses.values()) or selected_fuels):
        st.success(f"🌍 Total Estimated CO₂ Emission: {total_co2:.2f} kg/month")
        st.success(f"⚡ Estimated Green Offset: {green_offset:.2f} kg")

        # Pie Chart
        labels = ['Net CO₂ Emission', 'Sustainable Contribution']
        values = [total_co2 - green_offset, green_offset]
        colors = ['#ff4b4b', '#00cc66']
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        st.pyplot(fig)

        # Save to CSV
        data = {
            "Username": [username],
            "Home Appliances (₹)": [sum(home_expenses.values())],
            "Electronics (₹)": [sum(electronic_expenses.values())],
            "Selected Fuels": [", ".join(selected_fuels)],
            **{f"{fuel} (₹)": [fuel_costs.get(fuel, 0)] for fuel in selected_fuels},
            "CO₂ Emission (kg)": [total_co2],
            "Green Offset (kg)": [green_offset]
        }
        df = pd.DataFrame(data)
        file_path = "energy_contributions.csv"
        df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
        st.info("✅ Data saved successfully!")

# --- About Page ---
def about_page():
    st.title("🔍 About Sustainable Energy Tracker")

    st.header("What is Sustainable Energy Tracker?")
    st.markdown("""
    Sustainable Energy Tracker is a tool designed to help individuals and households track their energy consumption and CO₂ emissions. 
    The app allows you to input various factors that contribute to your energy usage, including household appliances, electronics, and vehicles. 
    Based on your inputs, the app calculates your estimated CO₂ emissions and suggests ways to offset those emissions to contribute to a greener future.
    """)

    st.header("How It Works")
    st.markdown("""
    1. **Input Data**: Enter details about your household appliances, electronics, and fuel usage.
    2. **Track Emissions**: The app calculates your energy consumption and CO₂ emissions based on your inputs.
    3. **Offset Emissions**: The app suggests a green offset, a sustainable measure to reduce your carbon footprint.
    4. **Visualize**: View your results through visualizations like pie charts and detailed data summaries.
    """)

    st.header("Why It Matters")
    st.markdown("""
    As the world grapples with climate change, reducing our carbon footprint has never been more important. 
    By tracking energy consumption and understanding our individual emissions, we can make more sustainable choices in our everyday lives.
    Our goal is to make the process of reducing emissions easier, one household at a time.

    Take control of your energy usage, track your emissions, and make a positive impact on the environment today!
    """)

    st.header("Our Mission")
    st.markdown("""
    Our mission is simple: 
    - **Empower individuals** to track and reduce their carbon footprint.
    - **Raise awareness** about the impact of energy consumption on the environment.
    - **Promote sustainable living** through actionable insights and tips.

    Join us in making the planet a greener place for future generations. Together, we can make a difference!
    """)

    st.header("Contact Us")
    st.markdown("""
    If you have any questions, feedback, or suggestions, feel free to reach out to us:

    - **Email**: support@sustainabletracker.com
    - **Website**: [www.sustainabletracker.com](http://www.sustainabletracker.com)
    - **Social Media**: @SustainableTracker
    """)

    st.info("Thank you for using the Sustainable Energy Tracker!")

# --- Page Routing ---
if st.session_state.page == "home":
    # Home Page Content
    st.title("Welcome to Sustainable Energy Tracker!")
    st.header("Track your energy usage and make the planet a greener place.")
    st.markdown("""
    This app helps you monitor your household energy consumption, calculate your CO₂ emissions, and track the steps you can take to reduce your carbon footprint.
    """)
    st.markdown("""
    - **Track Appliances**: Calculate energy consumption based on household appliances and electronics.
    - **Offset Emissions**: See how much CO₂ you could offset by reducing energy consumption or switching to renewable energy.
    - **Easy to Use**: Simple interface to input data and track your progress.
    """)

elif st.session_state.page == "tracker":
    # Tracker Page Content
    tracker_page()  # Call the function you already defined for the tracker page

elif st.session_state.page == "about":
    # About Page Content
    about_page()  # Call the function for the about page

else:
    # Default to Home Page if page is not recognized
    st.title("Welcome to Sustainable Energy Tracker!")
    st.header("Track your energy usage and make the planet a greener place.")
    st.markdown("""
    This app helps you monitor your household energy consumption, calculate your CO₂ emissions, and track the steps you can take to reduce your carbon footprint.
    """)
    st.markdown("""
    - **Track Appliances**: Calculate energy consumption based on household appliances and electronics.
    - **Offset Emissions**: See how much CO₂ you could offset by reducing energy consumption or switching to renewable energy.
    - **Easy to Use**: Simple interface to input data and track your progress.
    """)
