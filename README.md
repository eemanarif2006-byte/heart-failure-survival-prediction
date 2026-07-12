# ❤️ Heart Failure Survival Prediction using Machine Learning

An AI-powered web application that predicts the survival outcome of patients with heart failure using supervised machine learning. This project demonstrates the complete machine learning workflow, from data preprocessing and model training to deployment through an interactive Streamlit application.

---

## 📖 Overview

Heart failure is a serious medical condition where early risk assessment can support clinical decision-making. This project uses a Random Forest Classifier trained on real clinical records to predict whether a patient is likely to survive or experience a death event based on clinical and laboratory measurements.

The application provides an intuitive interface where users can enter patient information and receive an instant AI-powered prediction along with prediction confidence.

> **Disclaimer:** This project is developed for educational purposes only and should not be used for medical diagnosis or treatment.

---

## ✨ Features

- 📊 Exploratory Data Analysis (EDA)
- 🧹 Data preprocessing and feature selection
- 🤖 Multiple Machine Learning models
  - Decision Tree Classifier
  - Random Forest Classifier
- 📈 Model performance evaluation
- ❤️ Prediction confidence for both survival and death risk
- 🌐 Interactive Streamlit web application
- 🎨 Modern glassmorphism-inspired user interface
- 💾 Trained model saved using Pickle for deployment

---

## 📂 Dataset

The project uses the **Heart Failure Clinical Records Dataset**, containing clinical information collected from patients with heart failure.

### Dataset Information

- **Instances:** 299
- **Features:** 12 clinical attributes
- **Target Variable:** `DEATH_EVENT`

### Input Features

| Feature | Description |
|---------|-------------|
| Age | Patient age |
| Anaemia | Presence of anaemia |
| Creatinine Phosphokinase | Level of CPK enzyme |
| Diabetes | Diabetes status |
| Ejection Fraction | Percentage of blood leaving the heart each beat |
| High Blood Pressure | Hypertension status |
| Platelets | Platelet count |
| Serum Creatinine | Kidney function indicator |
| Serum Sodium | Sodium level in blood |
| Sex | Male/Female |
| Smoking | Smoking status |
| Follow-up Time | Follow-up period in days |

### Target

- **0** → Patient survived
- **1** → Death event occurred

---

## 🧠 Machine Learning Workflow

The notebook follows a complete supervised learning pipeline:

1. Import required libraries
2. Load dataset
3. Exploratory Data Analysis
4. Data inspection
5. Feature selection
6. Train-Test Split
7. Model training
8. Model evaluation
9. Model comparison
10. Save the best model
11. Deploy using Streamlit

---

## 🤖 Models Used

### Decision Tree Classifier

Used as the baseline classification model.

### Random Forest Classifier

The Random Forest model achieved the best performance and was selected for deployment.

---

## 📊 Model Performance

| Model | Accuracy |
|--------|---------:|
| Decision Tree | 73% |
| Random Forest | **83%** |

The Random Forest classifier demonstrated better generalization and was chosen as the final model.

---

## 🖥️ Streamlit Application

The deployed application allows users to:

- Enter patient clinical information
- Generate instant predictions
- View prediction confidence
- Experience a clean and responsive interface

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Pickle
- Streamlit
- Matplotlib

---

## 📁 Project Structure

```
Heart-Failure-Survival-Prediction/

│── app.py
│── heart_model.pkl
│── heart_failure_clinical_records_dataset.csv
│── Heart_Failure_Prediction.ipynb
│── requirements.txt
│── README.md
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Heart-Failure-Survival-Prediction.git
```

Move into the project directory:

```bash
cd Heart-Failure-Survival-Prediction
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

## 📸 Application Preview

Add screenshots of your Streamlit application here.

Example:

```
images/
├── home.png
├── prediction.png
├── result.png
```

---

## 🎯 Future Improvements

- Hyperparameter tuning
- Additional classification models
- Feature importance visualization
- SHAP explainability
- Docker deployment
- Cloud deployment
- Enhanced medical dashboard

---

## 📚 Learning Outcomes

This project demonstrates practical knowledge of:

- Supervised Machine Learning
- Classification Algorithms
- Random Forest
- Data Exploration
- Model Evaluation
- Model Deployment
- Streamlit Application Development
- Git & GitHub

---

## 👨‍💻 Author

**Eeman Arif**

BS Artificial Intelligence Student

Developed as part of the **DecodeLabs Artificial Intelligence Industrial Training Program**.

---

## ⭐ Acknowledgements

- DecodeLabs
- Scikit-learn Documentation
- Streamlit
- Heart Failure Clinical Records Dataset
