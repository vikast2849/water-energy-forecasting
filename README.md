# Population-Driven Forecasting: A Machine Learning Framework for Urban & Rural Water & Energy Demand

**Department of Computer Science & Engineering**  
**S.J.M. Institute of Technology (SJMIT), Chitradurga**  
*Academic Year 2026 - 2027*

---

## 📌 Project Overview
Rapid urbanization and population dynamics create severe strains on municipal resources. Existing systems treat urban and rural areas uniformly, resulting in water wastage in cities and severe shortages and power cuts in agrarian regions.

This project delivers a **population-driven forecasting website and machine learning framework** that models both **Water Demand (MLD)** and **Energy Demand (MWh)** across urban and rural sectors.

---

## 🧠 Machine Learning Algorithms Implemented

In accordance with the project specification (Chapters 1–5), the system implements three core algorithms:

1. **Support Vector Machine (SVM / SVR):**
   - Non-linear Radial Basis Function (RBF) kernel mapping high-dimensional demographic and climate variables.
   - Ideal for continuous urban water and electricity demand forecasting.
   - **Performance:** Water $R^2 = 99.86\%$, Energy $R^2 = 93.06\%$, 5-Fold CV $R^2 = 99.79\%$.

2. **K-Nearest Neighbors (KNN Regressor & Classifier):**
   - Distance-weighted neighbor aggregation ($k=5$).
   - Captures localized community consumption behaviors in rural taluks and agricultural clusters.
   - **Performance:** Water $R^2 = 98.84\%$, Energy $R^2 = 98.85\%$, 5-Fold CV $R^2 = 98.89\%$.

3. **Logistic Regression:**
   - Calibrated sigmoid probability classifier ($P(\text{Scarcity}) = \frac{1}{1 + e^{-z}}$).
   - Classifies resource scarcity risk (Normal vs. High Scarcity Risk) with transparent odds ratios and feature importance coefficients.
   - **Performance:** Accuracy $= 91.35\%$, Precision $= 0.974$, Recall $= 0.925$, F1 $= 0.949$.

> **All models comfortably exceed the non-functional requirement of $>85\%$ accuracy.**

---

## 🌐 Web Application Features

1. **Executive Dashboard (`/`):**
   - High-level KPIs (Average Water MLD, Energy MWh, Disparity Ratio, Scarcity alerts).
   - Multi-year trajectory graphs (2019–2035) with historical trends and ML forecasts.
   - Tri-model architecture snapshot.

2. **Interactive Live Prediction Studio (`/predict`):**
   - Dynamic form for localized demographic, climate, and infrastructure inputs.
   - 1-Click regional presets: *Chitradurga Urban Core*, *Challakere Rural Agrarian*, *Hiriyur Agro-Cluster*, and *Bengaluru Peri-Urban*.
   - Side-by-side comparative breakdown of **SVM**, **KNN**, and **Logistic Regression** forecasts.
   - Automated actionable policy recommendations for municipal utility boards.

3. **Urban vs. Rural Disparity Framework (`/comparative`):**
   - Multi-dimensional disparity radar chart.
   - Seasonal consumption breakdown (Summer vs Monsoon vs Winter LPCD).
   - Comprehensive taluk comparison table covering 11 Karnataka regions.

4. **3-Model Benchmarks & Explainability (`/models`):**
   - Grouped $R^2$ variance, MAE, and RMSE comparison charts.
   - Confusion matrices for all 3 classifiers.
   - Logistic Regression feature weights & odds ratio table.
   - Architectural comparison matrix.

5. **"What-If" Climate & Demographic Simulator (`/simulation`):**
   - Real-time reactive sliders for Population Growth %, Global Warming Temp Anomaly, and Rainfall Deficit.
   - Instant live stress testing across all 3 models.

6. **Dataset Management & CSV Upload (`/dataset`):**
   - Interactive paginated table of 924+ empirical records.
   - Filter by Region Name and Context (Urban/Rural).
   - 1-Click CSV dataset upload with automated retraining of SVM, KNN, and Logistic Regression models.

7. **Academic Project Report (`/report`):**
   - Formal documentation formatted for the final year project viva and institutional submission.
   - 1-Click "Print / Save as PDF" button.

---

## 🚀 How to Run the Website

### Prerequisites
- Python 3.9+ (Installed: Python 3.14)
- Packages: `Flask`, `scikit-learn`, `pandas`, `numpy`, `joblib`, `matplotlib`

### Step 1: Navigate to the Project Directory
```powershell
cd C:\Users\vinod\.gemini\antigravity\scratch\water-energy-forecasting
```

### Step 2: Run the Application
```powershell
python app.py
```

### Step 3: Open in Browser
Open your web browser and navigate to:
```


```

---

## 🧪 Running Automated Tests
To run the automated verification test suite:
```powershell
python test_pipeline.py
```

---

## 📁 Project Structure
```
water-energy-forecasting/
│
├── app.py                      # Flask application and REST API endpoints
├── train.py                    # Model training and cross-validation pipeline
├── test_pipeline.py            # Automated test suite (5/5 unit tests)
├── README.md                   # Complete documentation
│
├── data/
│   ├── generate_dataset.py     # Script to generate realistic urban/rural dataset
│   └── water_energy_demand.csv # 924 multi-year records across 11 regions
│
├── ml/
│   ├── preprocessor.py         # StandardScaler, feature extraction & imputation
│   ├── models.py               # SVM (SVR/SVC), KNN, Logistic Regression engines
│   └── analytics.py            # Disparity analysis, trendlines & simulation engine
│
├── saved_models/
│   ├── svm_water.joblib        # Trained SVR model for water demand
│   ├── svm_energy.joblib       # Trained SVR model for energy demand
│   ├── svm_clf.joblib          # Trained SVC model for scarcity risk
│   ├── knn_water.joblib        # Trained KNN Regressor for water demand
│   ├── knn_energy.joblib       # Trained KNN Regressor for energy demand
│   ├── knn_clf.joblib          # Trained KNN Classifier for scarcity risk
│   ├── logistic_clf.joblib     # Trained Logistic Regression classifier
│   ├── linear_water.joblib     # Linear baseline model for water
│   ├── linear_energy.joblib    # Linear baseline model for energy
│   ├── scaler.joblib           # Preprocessor StandardScaler
│   └── metrics.json            # Model metrics, R2, MAE, RMSE, Confusion Matrices
│
├── static/
│   ├── css/
│   │   └── style.css           # Modern glassmorphism UI & responsive styles
│   └── js/
│       ├── main.js             # Form presets, sliders, and upload handler
│       └── charts.js           # Chart.js visualization routines
│
└── templates/
    ├── base.html               # Base layout with sidebar & status pills
    ├── dashboard.html          # Executive analytics dashboard
    ├── predict.html            # Live forecasting studio
    ├── comparative.html        # Urban vs Rural disparity framework
    ├── models.html             # 3-model benchmark & explainability
    ├── simulation.html         # Climate & growth stress test simulator
    ├── dataset.html            # Dataset explorer & upload portal
    └── report.html             # Academic project report (Print/PDF)
```
