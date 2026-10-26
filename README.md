# Population-Driven Forecasting: A Machine Learning Framework for Urban & Rural Water & Energy Demand

[![Live Demo](https://img.shields.io/badge/Live%20Demo-water.vikasst.shop-0284c7?style=for-the-badge&logo=googlechrome&logoColor=white)](https://water.vikasst.shop)
[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-emerald?style=for-the-badge&logo=flask&logoColor=white)](https://palletsprojects.com/p/flask/)
[![Scikit-Learn](https://img.shields.io/badge/ML-scikit--learn%201.8-orange?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

**Department of Computer Science & Engineering**  
**S.J.M. Institute of Technology (SJMIT), Chitradurga**  
*Academic Year 2026 - 2027*

🌐 **Production Link:** [https://water.vikasst.shop](https://water.vikasst.shop)

---

## 📌 Project Overview
Rapid urbanization and population dynamics create severe strains on municipal utility systems. Traditional municipal resource planning frequently treats urban and rural sectors homogeneously, yielding treated water shortages and power load-shedding in agrarian zones alongside over-consumption in metropolitan centers.

This project delivers a **production-grade machine learning framework and cloud web application** to forecast:
- **Water Demand (Million Litres per Day - MLD)**
- **Energy Demand (Megawatt-Hours per Day - MWh)**
- **Resource Scarcity Risk Classification (Normal vs. High Scarcity Risk)**

Models are trained on empirical demographic, climatic, and infrastructure metrics across 11 Karnataka district regions.

---

## ⚡ Tech Stack
- **Backend Framework:** Python 3.13, Flask 3.1
- **Machine Learning & Analytics:** scikit-learn 1.8, NumPy 2.5, Pandas 2.3, Joblib 1.6
- **Production WSGI Server:** Gunicorn 23.0
- **Frontend:** Responsive HTML5, Glassmorphism CSS3, Chart.js 4.4, Leaflet.js, Three.js, Font Awesome 6
- **Hosting & Infrastructure:** Render Web Service (Linux)
- **Domain & SSL:** Custom Domain `water.vikasst.shop` (https://water.vikasst.shop) with automated TLS/HTTPS encryption

---

## 🧠 Machine Learning Algorithms
1. **Support Vector Machine (SVM / SVR / SVC):**
   - Non-linear Radial Basis Function (RBF) kernel mapping complex interactions between demographic density and seasonal thermal stress.
   - **Performance:** Water $R^2 = 99.86\%$, Energy $R^2 = 93.06\%$, 5-Fold Cross-Validation $R^2 = 99.79\%$.
2. **K-Nearest Neighbors (KNN Regressor & Classifier):**
   - Distance-weighted neighbor aggregation ($k=5$) capturing localized cluster consumption behaviors.
   - **Performance:** Water $R^2 = 98.84\%$, Energy $R^2 = 98.85\%$, 5-Fold Cross-Validation $R^2 = 98.89\%$.
3. **Logistic Regression & Linear Baseline:**
   - Interpretable log-odds classification for drought and scarcity risk alerting with feature importance ranking.
   - **Performance:** Accuracy $= 91.35\%$, Precision $= 0.974$, Recall $= 0.925$, F1 $= 0.949$.

---

## 🌐 Web Application Features
- **Executive Dashboard (`/dashboard`, `/home`):** Real-time KPIs, historical trends (2019–2025), and forward projections (2026–2035).
- **Interactive Forecasting Studio (`/predict`):** Localized parameter inputs, 1-click regional presets, consensus averaging, and actionable municipal policy recommendations.
- **Urban vs. Rural Disparity Framework (`/comparative`):** Comparative analytics, disparity ratios, and seasonal consumption radar breakdowns.
- **Geospatial Resource Map (`/map`):** Interactive GIS mapping of regional demand clusters and infrastructure coverage.
- **3-Model Benchmarks & Explainability (`/models`):** Grouped $R^2$, MAE, RMSE metrics, confusion matrices, and feature coefficients.
- **Demographic & Climate Stress Simulator (`/simulation`):** What-if stress testing with dynamic sliders for temperature anomalies, rainfall variation, and population shifts.
- **Dataset Management & Retraining (`/dataset`):** Paginated explorer of empirical records with CSV upload and automated retraining pipeline.
- **Health Check Endpoint (`/health`):** Lightweight automated uptime monitoring endpoint.

---

## 📸 Screenshots
*(Add application interface screenshots below)*

| Executive Dashboard | Forecasting Studio |
| :---: | :---: |
| ![Dashboard Screenshot](static/img/dashboard_preview.png) | ![Predict Screenshot](static/img/predict_preview.png) |

---

## 💻 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/vikast2849/water-energy-forecasting.git
cd water-energy-forecasting
```

### 2. Create and Activate Virtual Environment
**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**On Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` to set your secret key or custom demo passwords.

### 5. Run the Application
**Development Server:**
```bash
python app.py
```
**Production Server (Gunicorn):**
```bash
gunicorn app:app --workers 2 --timeout 120
```
Access the application at `http://127.0.0.1:5000`.

---

## 🧪 Automated Testing
Run the complete unit and integration test suite:
```bash
python test_pipeline.py
```

---

## 📁 Project Structure
```
water-energy-forecasting/
├── app.py                      # Flask web application & REST API routes
├── Procfile                    # Render/Heroku process declaration
├── render.yaml                 # Render infrastructure-as-code specification
├── requirements.txt            # Pinned production dependencies
├── .python-version             # Python version pin (3.13.0)
├── .env.example                # Example environment variables template
├── .gitignore                  # Git ignore rules
├── run.py                      # Production startup helper
├── train.py                    # Standalone model training pipeline
├── test_pipeline.py            # Automated test suite
├── README.md                   # Complete documentation
│
├── data/
│   ├── generate_dataset.py     # Synthetic data generator for Karnataka regions
│   └── water_energy_demand.csv # 924 historical records
│
├── ml/
│   ├── preprocessor.py         # Feature engineering & StandardScaler
│   ├── models.py               # SVR/SVC, KNN, Logistic Regression predictors
│   └── analytics.py            # Statistical KPIs, trends, and disparity analysis
│
├── saved_models/
│   ├── *.joblib                # Serialized scikit-learn models & scaler
│   └── metrics.json            # Model evaluation metrics cache
│
├── static/
│   ├── css/style.css           # Glassmorphism dark mode stylesheet
│   └── js/                     # Client-side visualization routines (Chart.js)
│
└── templates/
    ├── base.html               # Master layout template
    ├── login.html              # Authentication portal
    ├── dashboard.html          # Executive analytics dashboard
    ├── predict.html            # Scenario forecasting studio
    ├── comparative.html        # Urban vs Rural analytics
    ├── map.html                # GIS resource mapping
    ├── models.html             # Machine learning evaluation
    ├── simulation.html         # Climate/demographic simulator
    ├── dataset.html            # Paginated dataset viewer
    └── report.html             # Institutional project report
```

---

## 🚀 Cloud Deployment (Render.com)

1. Connect the GitHub repository `vikast2849/water-energy-forecasting` to [Render](https://dashboard.render.com).
2. Configure Web Service:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --workers 2 --timeout 120`
3. Add environment variables:
   - `PYTHON_VERSION`: `3.13.0`
   - `SECRET_KEY`: *(Generate a random 32-byte string)*
4. Map custom domain `water.vikasst.shop` (https://water.vikasst.shop) and configure DNS records as specified in the project deployment guide.
