# Health Insurance Cost Predictor

## Introduction

The Health Insurance Cost Predictor is a Machine Learning web application that predicts an individual's insurance premium cost based on personal, medical, and lifestyle factors.
This project combines data preprocessing, feature engineering, and XGBoost regression modeling to deliver accurate and interpretable cost predictions.
The frontend is built using Streamlit, providing a clean, interactive user interface where users can input their details and instantly get a predicted insurance cost.

## Features 
- **Predicts personalized health insurance costs.**
- **Modern Streamlit web UI with a purple-themed design.**
- **Input features include:**
     - **Demographic: Age, Gender, Marital Status, Dependents, Region**
     - **Lifestyle: Income, Stress Level, Physical Activity Level, Smoking Status**
     - **Medical: BMI Category, Medical History, Insurance Plan, Employment Status**
-  **Donut chart visualization showing insurance plan distribution (Bronze, Silver, Gold).**
-  **Trained using multiple regression models and tuned with RandomizedSearchCV for best accuracy.**


## Project Structure
- **frontend – Contains the Streamlit application code and UI components.**
- **artifacts/ – Stores the trained machine learning model and scaler objects saved using Joblib.**
   - **prediction_model.joblib – Trained XGBoostRegressor model used for predictions.**
   - **scaler_model.joblib – MinMaxScaler object used for feature scaling during preprocessing.**
- **requirements.txt – Lists all the required Python packages to run the project.**
- **README.md – Provides an overview, setup instructions, and details about the project.**

## Machine Learning Workflow
1. Data Cleaning
- **Handled missing values and outliers.**
- **Normalized numerical features using MinMaxScaler.**
2. Feature Engineering
- **Created normalized_risk_score (based on Medical History) to represent disease severity.**
- **Created lifestyle_risk_score (based on Physical & Stress Level) to capture lifestyle influence.**
- **Applied Label Encoding and One-Hot Encoding for categorical features.**
3. Feature Selection
- **Used Variance Inflation Factor (VIF) to identify and remove multicollinear features.**
4. Model Training & Evaluation
- **Split the dataset using train_test_split.**
- **Trained and evaluated the using Linearn Regression , Ridge Regression and XGBRegressor**
5. Hyperparameter Tuning
- **Used RandomizedSearchCV on XGBRegressor() to identify the best combination of parameters like:n_estimators, max_depth, learning_rate**
- **Saved the final optimized model  for deployment.**

## Model Explanation
Final Model: XGBRegressor() (Tuned using RandomizedSearchCV)
- **XGBoost (Extreme Gradient Boosting) is an advanced ensemble algorithm that combines multiple decision trees to improve accuracy.**
- **It handles both categorical and numerical data efficiently, preventing overfitting via regularization parameters.**
- **Chosen as the final model because it outperformed Linear and Ridge Regression with ~98% score on test data.**




## Demo video
https://drive.google.com/file/d/1L7sy2HRW5xTpUVu-00zw2ZRahVqXZOfG/view?usp=drive_link

### *Click the link above to watch the demo video!*


## Tech Stack
- **Frontend: Streamlit**
- **Backend / Model Handling: Python**
- **Machine Learning Libraries: Scikit-learn, XGBoost**
- **Data Processing: Pandas, NumPy**
- **Model Serialization: Joblib**
- **Visualization: Matplotlib, Seaborn**



## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HarshithaV2002/ml-project-premium-prediction.git
   cd ml-project-premium-prediction
   ```

1. **Install dependencies:**:   
   ```commandline
    pip install -r requirements.txt
   ```
1. **Run the Streamlit app:**:   
   ```commandline
    streamlit run frontend/main.py

   ```


## Live Demo
You can access the deployed application here:
[**Premium Prediction App – Live on Streamlit**](https://ml-project-healthcare-insurance-premium-prediction.streamlit.app/)


## Future Improvements

- **Integrate database to save user predictions.**
- **Add more medical & lifestyle parameters for improved accuracy.**
- **Enable API-based prediction service for wider use.**


## Conclusion
This project demonstrates how Machine Learning and feature engineering can be applied to predict insurance premiums with high accuracy.
The final tuned XGBRegressor model provides interpretable, data-driven cost predictions — all wrapped in an elegant Streamlit interface.
