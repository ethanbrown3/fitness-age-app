import streamlit as st

def score(value, min_val, max_val):
    return max(0, min(100, (value - min_val) / (max_val - min_val) * 100))

st.title("Fitness-Based Biological Age Calculator")

sex = st.selectbox("Sex", ["male", "female"])
hrv = st.slider("HRV (ms)", 20, 120, 87)
rhr = st.slider("RHR (bpm)", 30, 100, 52)
body_fat = st.slider("Body Fat (%)", 5.0, 40.0, 12.0)
height = st.slider("Height (inches)", 48, 84, 72)
weight = st.slider("Weight (lbs)", 80, 300, 194)
vo2 = st.slider("VO2 Max", 20.0, 70.0, 50.0)

# Calculate BMI
height_m = height * 0.0254
weight_kg = weight * 0.453592
bmi = weight_kg / (height_m ** 2)

# Adjusted scoring
hrv_score = score(hrv, 10 if sex == "female" else 20, 90 if sex == "female" else 100)
rhr_score = score(105 - rhr if sex == "female" else 100 - rhr, 0, 60)
bf_score = score(30 - body_fat if sex == "female" else 25 - body_fat, 0, 12 if sex == "female" else 15)
bmi_score = max(0, 100 - abs(bmi - 22) * 5)
vo2_score = score(vo2 - 25 if sex == "female" else vo2 - 30, 0, 25)

fitness_score = sum([hrv_score, rhr_score, bf_score, bmi_score, vo2_score]) / 5
relative_age = 80 - (fitness_score / 100 * 60)

st.subheader(f"🏋️‍♂️ Fitness Score: {fitness_score:.1f}")
st.subheader(f"🧬 Biological Age: {relative_age:.1f} years")