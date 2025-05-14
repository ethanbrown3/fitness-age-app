import streamlit as st
from enum import Enum, auto


def score(value, min_val, max_val):
    return max(0, min(100, (value - min_val) / (max_val - min_val) * 100))


# Enums and constants for the Fitness-Based Biological Age Calculator
# All constants are either part of an enum, a mapping, or documented below.

class Sex(Enum):
    MALE = "male"
    FEMALE = "female"
# Sex: Biological sex, used for sex-specific scoring constants

class Metric(Enum):
    HRV_MIN = auto()      # Minimum HRV for scoring
    HRV_MAX = auto()      # Maximum HRV for scoring
    RHR_BASE = auto()     # Base value for RHR scoring
    BF_BASE = auto()      # Base value for Body Fat scoring
    BF_MIN = auto()       # Minimum value for Body Fat scoring
    VO2_OFFSET = auto()   # Offset for VO2 Max scoring

class SliderParam(Enum):
    HRV = "hrv"           # Heart Rate Variability
    RHR = "rhr"           # Resting Heart Rate
    BODY_FAT = "body_fat" # Body Fat Percentage
    HEIGHT = "height"     # Height in inches
    WEIGHT = "weight"     # Weight in pounds
    VO2 = "vo2"           # VO2 Max


# Sex-specific scoring constants for each metric
SCORING_CONSTANTS = {
    Sex.MALE: {
        Metric.HRV_MIN: 20,      # ms
        Metric.HRV_MAX: 100,     # ms
        Metric.RHR_BASE: 100,    # bpm
        Metric.BF_BASE: 25,      # %
        Metric.BF_MIN: 15,       # %
        Metric.VO2_OFFSET: 30,   # ml/kg/min
    },
    Sex.FEMALE: {
        Metric.HRV_MIN: 10,      # ms
        Metric.HRV_MAX: 90,      # ms
        Metric.RHR_BASE: 105,    # bpm
        Metric.BF_BASE: 30,      # %
        Metric.BF_MIN: 12,       # %
        Metric.VO2_OFFSET: 25,   # ml/kg/min
    },
}

# Slider min, max, and default values for each metric
SLIDER_CONSTANTS = {
    SliderParam.HRV: {"min": 20, "max": 120, "default": 87},           # ms
    SliderParam.RHR: {"min": 30, "max": 100, "default": 52},           # bpm
    SliderParam.BODY_FAT: {"min": 5.0, "max": 40.0, "default": 12.0},  # %
    SliderParam.HEIGHT: {"min": 48, "max": 84, "default": 72},         # inches
    SliderParam.WEIGHT: {"min": 80, "max": 300, "default": 194},       # lbs
    SliderParam.VO2: {"min": 20.0, "max": 70.0, "default": 50.0},      # ml/kg/min
}

# BMI calculation constants
BMI_IDEAL = 22  # Ideal BMI for scoring
BMI_PENALTY = 5 # Penalty per point away from ideal

# Unit conversion constants
INCHES_TO_METERS = 0.0254   # 1 inch = 0.0254 meters
POUNDS_TO_KG = 0.453592     # 1 pound = 0.453592 kilograms

st.title("Fitness-Based Biological Age Calculator")

sex = st.selectbox("Sex", list(
    Sex), format_func=lambda x: x.value.capitalize())
hrv = st.slider("HRV (ms)", SLIDER_CONSTANTS[SliderParam.HRV]["min"],
                SLIDER_CONSTANTS[SliderParam.HRV]["max"], SLIDER_CONSTANTS[SliderParam.HRV]["default"])
rhr = st.slider("RHR (bpm)", SLIDER_CONSTANTS[SliderParam.RHR]["min"],
                SLIDER_CONSTANTS[SliderParam.RHR]["max"], SLIDER_CONSTANTS[SliderParam.RHR]["default"])
body_fat = st.slider("Body Fat (%)", SLIDER_CONSTANTS[SliderParam.BODY_FAT]["min"],
                     SLIDER_CONSTANTS[SliderParam.BODY_FAT]["max"], SLIDER_CONSTANTS[SliderParam.BODY_FAT]["default"])
height = st.slider("Height (inches)", SLIDER_CONSTANTS[SliderParam.HEIGHT]["min"],
                   SLIDER_CONSTANTS[SliderParam.HEIGHT]["max"], SLIDER_CONSTANTS[SliderParam.HEIGHT]["default"])
weight = st.slider("Weight (lbs)", SLIDER_CONSTANTS[SliderParam.WEIGHT]["min"],
                   SLIDER_CONSTANTS[SliderParam.WEIGHT]["max"], SLIDER_CONSTANTS[SliderParam.WEIGHT]["default"])
vo2 = st.slider("VO2 Max", SLIDER_CONSTANTS[SliderParam.VO2]["min"],
                SLIDER_CONSTANTS[SliderParam.VO2]["max"], SLIDER_CONSTANTS[SliderParam.VO2]["default"])

# Calculate BMI
height_m = height * INCHES_TO_METERS
weight_kg = weight * POUNDS_TO_KG
bmi = weight_kg / (height_m ** 2)

# Adjusted scoring
hrv_score = score(
    hrv, SCORING_CONSTANTS[sex][Metric.HRV_MIN], SCORING_CONSTANTS[sex][Metric.HRV_MAX])
rhr_score = score(SCORING_CONSTANTS[sex][Metric.RHR_BASE] - rhr, 0, 60)
bf_score = score(SCORING_CONSTANTS[sex][Metric.BF_BASE] -
                 body_fat, 0, SCORING_CONSTANTS[sex][Metric.BF_MIN])
bmi_score = max(0, 100 - abs(bmi - BMI_IDEAL) * BMI_PENALTY)
vo2_score = score(vo2 - SCORING_CONSTANTS[sex][Metric.VO2_OFFSET], 0, 25)

fitness_score = sum([hrv_score, rhr_score, bf_score, bmi_score, vo2_score]) / 5

# Relative age calculation constants
AGE_BASE = 80   # Base age for calculation
AGE_RANGE = 60  # Range reduced by fitness score

relative_age = AGE_BASE - (fitness_score / 100 * AGE_RANGE)

st.subheader(f"🏋️‍♂️ Fitness Score: {fitness_score:.1f}")
st.subheader(f"🧬 Biological Age: {relative_age:.1f} years")
