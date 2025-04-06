import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="BMI Calculator", layout="centered", page_icon="⚕")

st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        font-size: 12px;
        text-align: center;
        color: grey;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Your BMI Companion 💪📊</div>', unsafe_allow_html=True)

st.markdown("""
    <h2 style="text-align: center; color: #3f9eca; font-size: 30px; 
    animation: slidein 3s ease-in-out;">FitIndex: Your BMI Companion 💪📊 - Calculate your BMI instantly and get personalized tips!</h2>
    <style>
    @keyframes slidein {
        0% { transform: translateX(-100%); }
        50% { transform: translateX(0); }
        100% { transform: translateX(100%); }
    }
    </style>
""", unsafe_allow_html=True)


name = st.text_input("Enter your name")
age = st.slider("Select your age", 5, 100, 25)
gender = st.radio("Select your gender", ["Male", "Female", "Other"])
weight = st.number_input("Enter your weight (kg)", min_value=1.0)
height = st.number_input("Enter your height (meters)", min_value=0.1, format="%.2f")
height_unit = st.selectbox("Select your height unit", ["Meters", "Feet"])

if height_unit == "Feet":
    height = height * 0.3048

if st.button("Calculate BMI"):
    if weight and height:
        bmi = weight / (height ** 2)
        st.success(f"{name}, your BMI is: {bmi:.2f}")

        if bmi < 18.5:
            category = "Underweight"
            st.warning("You're underweight.")
            st.info("Tip: Increase calorie-rich foods and consult a dietitian.")
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
            st.success("You have a normal weight.")
            st.info("Tip: Maintain your diet and stay active.")
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            st.info("You're overweight.")
            st.info("Tip: Add cardio, eat more fiber, and cut sugar.")
        else:
            category = "Obese"
            st.error("You're in the obese category.")
            st.info("Tip: Seek professional medical advice for a plan.")

        min_ideal = 18.5 * height**2
        max_ideal = 24.9 * height**2
        st.write(f"Ideal weight for your height: *{min_ideal:.1f} kg - {max_ideal:.1f} kg*")

        if 'bmi_data' not in st.session_state:
            st.session_state.bmi_data = []

        if name:
            st.session_state.bmi_data.append({
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Weight (kg)": weight,
                "Height (m)": height,
                "BMI": round(bmi, 2),
                "Category": category
            })

        if st.session_state.bmi_data:
            st.subheader("BMI History")
            df = pd.DataFrame(st.session_state.bmi_data)
            st.dataframe(df, use_container_width=True)

        st.subheader("Your BMI on Category Bar")

        fig, ax = plt.subplots(figsize=(8, 1))
        categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
        colors = ['yellow', 'green', 'orange', 'red']
        limits = [0, 18.5, 24.9, 29.9, 40]

        for i in range(4):
            ax.barh(0, limits[i+1] - limits[i], left=limits[i], color=colors[i])

        ax.axvline(bmi, color='blue', linewidth=2, label=f'Your BMI: {bmi:.2f}')
        ax.set_xlim(10, 40)
        ax.get_yaxis().set_visible(False)
        ax.set_xlabel('BMI')
        ax.legend()
        st.pyplot(fig)

st.markdown('<div class="footer">Designed with care by Saira | Streamlit BMI Calculator</div>', unsafe_allow_html=True)
