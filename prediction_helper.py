import pandas as pd
from joblib import load

model = load("artifacts/prediction_model.joblib")
scaler_mo = load("artifacts/scaler_model.joblib")


def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    # Split the medical history into potential two parts and convert to lowercase
    diseases = "&".join(medical_history).lower().split(" & ")

    # Calculate the total risk score by summing the risk scores for each part
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)  # Default to 0 if disease not found

    max_score = 14 # risk score for heart disease (8) + second max risk score (6) for diabetes or high blood pressure
    min_score = 0  # Since the minimum score is always 0

    # Normalize the total risk score
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)

    return normalized_risk_score



def calculate_lifestyle_risk(physical_activity, stress_level):
    """
    Calculates a lifestyle risk score based on physical activity and stress level.
    Works for string, list, or pandas Series inputs.
    """
    pa_score = {'High': 0, 'Medium': 1, 'Low': 4}
    stress_score = {'High': 4, 'Medium': 1, 'Low': 0}

    # 🔹 Normalize input types to pandas Series
    if isinstance(physical_activity, list):
        physical_activity = pd.Series(physical_activity)
    elif isinstance(physical_activity, str):
        physical_activity = pd.Series([physical_activity])

    if isinstance(stress_level, list):
        stress_level = pd.Series(stress_level)
    elif isinstance(stress_level, str):
        stress_level = pd.Series([stress_level])

    # 🔹 Map to numeric values
    pa_values = physical_activity.map(pa_score)
    stress_values = stress_level.map(stress_score)

    result = pa_values + stress_values
    return result.iloc[0] if len(result) == 1 else result


def preprocess_input(input_dict):
    expected_columns = [
        'age','number_of_dependants','income_lakhs','insurance_plan','normalized_risk_score','life_style_risk_score',
        'gender_Male','region_Northwest','region_Southeast','region_Southwest','marital_status_Unmarried',
       'bmi_category_Obesity','bmi_category_Overweight','bmi_category_Underweight','smoking_status_Occasional',
        'smoking_status_Regular','employment_status_Salaried','employment_status_Self-Employed'
    ]
    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    for key, value in input_dict.items():
        if key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'Marital Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'BMI Category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1
        elif key == 'Smoking Status':
            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1
            elif value == 'Regular':
                df['smoking_status_Regular'] = 1
        elif key == 'Employment Status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance Plan':  # Correct key usage with case sensitivity
            df['insurance_plan'] = insurance_plan_encoding.get(value, 1)
        elif key == 'Age':  # Correct key usage with case sensitivity
            df['age'] = value
        elif key == 'Number of Dependants':  # Correct key usage with case sensitivity
            df['number_of_dependants'] = value
        elif key == 'Income in Lakhs':  # Correct key usage with case sensitivity
            df['income_lakhs'] = value
    df['normalized_risk_score'] = calculate_normalized_risk(input_dict['Medical History'])
    df['life_style_risk_score'] = calculate_lifestyle_risk(input_dict['Physical Level'], input_dict['Stress Level'])
    df = handle_scaling(df,scaler_mo)
    return df

def handle_scaling(df, scaler_mo=None):
    # scale age and income_lakhs column
    scaler_object = scaler_mo
    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    df['income_level'] = None # since scaler object expects income_level supply it. This will have no impact on anything
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    df.drop('income_level', axis='columns', inplace=True)

    return df










def predict(input_dict):
   input_df = preprocess_input(input_dict)
   prediction = model.predict(input_df)

   return int(prediction[0])