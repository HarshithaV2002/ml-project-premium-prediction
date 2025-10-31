import streamlit as st
from matplotlib import pyplot as plt
from prediction_helper import predict

# ================== PAGE SETUP ==================
st.set_page_config(page_title="Health Insurance Cost Predictor", layout="wide")

# ================== CUSTOM CSS ==================
st.markdown("""
    <style>
    body, .main, .block-container {
        background: linear-gradient(135deg, #fff5e6, #fff);
    }

    h1 {
        color: #6a0dad !important;
        font-weight: bold !important;
        text-align: left !important;
        margin-bottom: 25px !important;
    }

    /* Make form labels black */
    label, div[data-baseweb="select"] * {
        color: black !important;
    }

    /* Input and select styling */
    div[data-baseweb="input"] input, div[data-baseweb="select"] > div {
        color: black !important;
        background-color: white !important;
        border: 1px solid #6a0dad !important;
        border-radius: 8px !important;
        height: 40px !important;
    }

    /* Stronger selector for button */
    div.stButton > button[kind="primary"], div.stButton > button:first-child {
        background: #8a2be2 !important;   /* Bright purple */
        color: white !important;
        border: 2px solid #8a2be2 !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-size: 16px !important;
        height: 45px !important;
        font-weight: bold !important;
        transition: all 0.3s ease-in-out !important;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stButton > button:first-child:hover {
        background: #6a0dad !important;   /* Deep purple on hover */
        border-color: #6a0dad !important;
        transform: scale(1.03);
        color: white !important;
    }

    /* Optional: Remove Streamlit theme override */
    [data-testid="stAppViewContainer"] button {
        background: #8a2be2 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ================== LAYOUT ==================
col1, col2 = st.columns([2, 1.2])

# ================== LEFT SIDE FORM ==================
with col1:
    st.markdown("<h1>🏥 Health Insurance Cost Predictor</h1>", unsafe_allow_html=True)

    with st.form("prediction_form"):
        categorical_options = {
            'Gender': ['Male', 'Female'],
            'Stress Level': ['Low', 'Medium', 'High'],
            'Physical Level': ['Low', 'Medium', 'High'],
            'Marital Status': ['Unmarried', 'Married'],
            'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
            'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
            'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
            'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
            'Medical History': [
                'No Disease', 'Diabetes', 'High blood pressure',
                'Diabetes & High blood pressure', 'Thyroid', 'Heart disease',
                'High blood pressure & Heart disease', 'Diabetes & Thyroid',
                'Diabetes & Heart disease'
            ],
            'Insurance Plan': ['Bronze', 'Silver', 'Gold']
        }

        # Input rows
        row1 = st.columns(3)
        row2 = st.columns(3)
        row3 = st.columns(3)
        row4 = st.columns(3)
        row5 = st.columns(3)

        with row1[0]:
            age = st.number_input('Age', 18, 100, step=1)
        with row1[1]:
            dependants = st.number_input('Number of Dependants', 0, 20, step=1)
        with row1[2]:
            income = st.number_input('Income in Lakhs', 0, 200, step=1)

        with row2[0]:
            gender = st.selectbox('Gender', categorical_options['Gender'])
        with row2[1]:
            marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
        with row2[2]:
            bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])

        with row3[0]:
            smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
        with row3[1]:
            region = st.selectbox('Region', categorical_options['Region'])
        with row3[2]:
            medical_history = st.selectbox('Medical History', categorical_options['Medical History'])

        with row4[0]:
            insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
        with row4[1]:
            employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])
        with row4[2]:
            physical_level = st.selectbox('Physical Level', categorical_options['Physical Level'])

        with row5[0]:
            stress_level = st.selectbox('Stress Level', categorical_options['Stress Level'])

        submitted = st.form_submit_button("Predict")

        if submitted:
            input_dict = {
                'Age': age,
                'Number of Dependants': dependants,
                'Income in Lakhs': income,
                'Physical Level': physical_level,
                'Stress Level': stress_level,
                'Insurance Plan': insurance_plan,
                'Employment Status': employment_status,
                'Gender': gender,
                'Marital Status': marital_status,
                'BMI Category': bmi_category,
                'Smoking Status': smoking_status,
                'Region': region,
                'Medical History': medical_history
            }
            prediction = predict(input_dict)
            st.session_state['prediction'] = prediction

    if 'prediction' in st.session_state:
        st.markdown(
            f"""
            <div style="
                background-color: #f3e5ff;
                border: 2px solid #6a0dad;
                color: black;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                font-weight: 600;
                font-size: 18px;
                margin-top: 15px;">
                Predicted Health Insurance Cost: ₹{st.session_state['prediction']}
            </div>
            """,
            unsafe_allow_html=True
        )

# ================== RIGHT SIDE DONUT CHART ==================
with col2:
    labels = ['Bronze', 'Silver', 'Gold']
    sizes = [37.2, 36.4, 26.4]
    colors = ['#e0b3ff', '#b366ff', '#8000ff']

    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%',
        startangle=90, colors=colors, wedgeprops=dict(width=0.3)
    )

    for text in texts + autotexts:
        text.set_color('black')

    ax.axis('equal')
    st.pyplot(fig)
