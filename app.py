import os
import sys
import json
import pandas as pd
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session

# Add base directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.models import ModelTrainer, DemandPredictor
from ml.analytics import DemandAnalytics

app = Flask(__name__)
app.config["SECRET_KEY"] = "sjmit-cs-project-2026-secret-secure-key"
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "data")

DATA_PATH = os.path.join(BASE_DIR, "data", "water_energy_demand.csv")
MODELS_DIR = os.path.join(BASE_DIR, "saved_models")

# In-memory user database with pre-configured demo users
USERS_DB = {
    "officer@sjmit.ac.in": {"name": "Dr. Rajesh Kumar", "password": "password123", "role": "Municipal Utility Officer"},
    "researcher@sjmit.ac.in": {"name": "Final Year CS&E Scholar", "password": "password123", "role": "CS&E Project Scholar"},
    "admin@sjmit.ac.in": {"name": "System Administrator", "password": "admin", "role": "System Admin"}
}

# Access Control Decorator (Fulfills Section 5.9 Security Requirements)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login_page", message="Authentication Required: Please sign in or use 1-Click Demo Login to access this module."))
        return f(*args, **kwargs)
    return decorated_function

# Initialize models and analytics
predictor = DemandPredictor(models_dir=MODELS_DIR)
analytics = DemandAnalytics(data_path=DATA_PATH)

@app.context_processor
def inject_global_vars():
    return {
        "project_title": "Population-Driven Forecasting: A Machine Learning Framework for Urban & Rural Water & Energy Demand",
        "college_dept": "Dept. of CS&E, SJMIT, Chitradurga",
        "academic_year": "2026-2027",
        "current_user": session.get("user")
    }

# -----------------------------------------------------------------------------
# WEB PAGE ROUTES
# -----------------------------------------------------------------------------

@app.route("/")
def root():
    # If not logged in, gate access directly to Login Page
    if not session.get("user"):
        return redirect(url_for("login_page"))
    return redirect(url_for("home"))

@app.route("/home")
@login_required
def home():
    kpis = analytics.get_summary_kpis()
    metrics = predictor.metrics
    return render_template("home.html", kpis=kpis, metrics=metrics)

@app.route("/dashboard")
@login_required
def dashboard():
    kpis = analytics.get_summary_kpis()
    trends = analytics.get_time_series_trends()
    metrics = predictor.metrics
    return render_template("dashboard.html", kpis=kpis, trends=trends, metrics=metrics)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    error = None
    message = request.args.get("message")
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        # Check existing or demo user
        if username in USERS_DB:
            if USERS_DB[username]["password"] == password:
                session["user"] = {
                    "email": username,
                    "name": USERS_DB[username]["name"],
                    "role": USERS_DB[username]["role"]
                }
                return redirect(url_for("home"))
            else:
                error = "Invalid password. Please verify credentials."
        else:
            # Allow flexible sign-in for evaluation / quick testing
            if len(password) >= 3:
                name_part = username.split("@")[0].replace(".", " ").title()
                session["user"] = {
                    "email": username,
                    "name": name_part or "Authorized Reviewer",
                    "role": "CS&E Project Reviewer"
                }
                return redirect(url_for("home"))
            else:
                error = "User not recognized. Use quick demo buttons or register."

    return render_template("login.html", error=error, message=message)

@app.route("/register", methods=["GET", "POST"])
def register_page():
    error = None
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        role = request.form.get("role", "CS&E Project Scholar")
        password = request.form.get("password", "").strip()

        if not fullname or not email or not password:
            error = "Please fill in all required registration fields."
        else:
            USERS_DB[email] = {
                "name": fullname,
                "password": password,
                "role": role
            }
            session["user"] = {
                "email": email,
                "name": fullname,
                "role": role
            }
            return redirect(url_for("dashboard"))

    return render_template("register.html", error=error)

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password_page():
    error = None
    success = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        otp_code = request.form.get("otp_code", "").strip()
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not email or not new_password or not confirm_password:
            error = "Please fill out all required fields."
        elif new_password != confirm_password:
            error = "New passwords do not match. Please verify."
        elif len(new_password) < 4:
            error = "Password must be at least 4 characters long."
        else:
            if email in USERS_DB:
                USERS_DB[email]["password"] = new_password
            else:
                name_part = email.split("@")[0].replace(".", " ").title()
                USERS_DB[email] = {
                    "name": name_part or "Authorized User",
                    "password": new_password,
                    "role": "CS&E Project Scholar"
                }
            success = f"Password for {email} has been successfully reset! You can now sign in with your new credentials."

    return render_template("forgot_password.html", error=error, success=success)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page", message="You have been safely signed out. Please authenticate to continue."))

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict_page():
    result = None
    default_inputs = {
        "Region_Name": "Chitradurga Urban",
        "Region_Type": "Urban",
        "Population": 225000,
        "Population_Density": 3950,
        "Household_Size": 4.0,
        "Avg_Temperature_C": 36.5,
        "Rainfall_mm": 15.0,
        "Industrial_Index": 68.0,
        "Agricultural_Index": 10.0,
        "Water_Piped_Coverage_Pct": 92.0,
        "Electrification_Pct": 99.0,
        "Season": "Summer"
    }

    if request.method == "POST":
        user_inputs = {
            "Region_Name": request.form.get("Region_Name", "Custom Region"),
            "Region_Type": request.form.get("Region_Type", "Urban"),
            "Population": float(request.form.get("Population", 100000)),
            "Population_Density": float(request.form.get("Population_Density", 2000)),
            "Household_Size": float(request.form.get("Household_Size", 4.0)),
            "Avg_Temperature_C": float(request.form.get("Avg_Temperature_C", 30.0)),
            "Rainfall_mm": float(request.form.get("Rainfall_mm", 50.0)),
            "Industrial_Index": float(request.form.get("Industrial_Index", 50.0)),
            "Agricultural_Index": float(request.form.get("Agricultural_Index", 50.0)),
            "Water_Piped_Coverage_Pct": float(request.form.get("Water_Piped_Coverage_Pct", 80.0)),
            "Electrification_Pct": float(request.form.get("Electrification_Pct", 95.0)),
            "Season": request.form.get("Season", "Summer")
        }
        result = predictor.predict_single(user_inputs)
        default_inputs = user_inputs

    return render_template("predict.html", result=result, form_data=default_inputs)

@app.route("/comparative")
@login_required
def comparative():
    kpis = analytics.get_summary_kpis()
    comparison_data = analytics.get_urban_rural_comparison()
    regional_breakdown = analytics.get_regional_breakdown()
    return render_template("comparative.html", kpis=kpis, comp=comparison_data, regions=regional_breakdown)

@app.route("/map")
@login_required
def map_view():
    kpis = analytics.get_summary_kpis()
    return render_template("map.html", kpis=kpis)

@app.route("/models")
@login_required
def models_view():
    metrics = predictor.metrics
    return render_template("models.html", metrics=metrics)

@app.route("/simulation")
@login_required
def simulation():
    return render_template("simulation.html")

@app.route("/dataset")
@login_required
def dataset_view():
    page = int(request.args.get("page", 1))
    per_page = 20
    region_filter = request.args.get("region", "")
    type_filter = request.args.get("type", "")

    df = pd.read_csv(DATA_PATH)
    if region_filter:
        df = df[df["Region_Name"].str.contains(region_filter, case=False, na=False)]
    if type_filter:
        df = df[df["Region_Type"].str.lower() == type_filter.lower()]

    total_items = len(df)
    total_pages = max(1, (total_items + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_data = df.iloc[start_idx:end_idx].to_dict(orient="records")

    return render_template("dataset.html", 
                           records=page_data, 
                           page=page, 
                           total_pages=total_pages, 
                           total_items=total_items,
                           region_filter=region_filter,
                           type_filter=type_filter)

@app.route("/report")
@login_required
def report_view():
    kpis = analytics.get_summary_kpis()
    metrics = predictor.metrics
    trends = analytics.get_time_series_trends()
    return render_template("report.html", kpis=kpis, metrics=metrics, trends=trends)

# -----------------------------------------------------------------------------
# RESTFUL API ENDPOINTS
# -----------------------------------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json(force=True)
        res = predictor.predict_single(data)
        return jsonify({"status": "success", "data": res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    try:
        data = request.get_json(force=True)
        pop_growth = float(data.get("pop_growth_pct", 0.0))
        temp_anomaly = float(data.get("temp_anomaly", 0.0))
        rain_factor = float(data.get("rain_factor", 1.0))
        ind_change = float(data.get("ind_change", 0.0))
        agr_change = float(data.get("agr_change", 0.0))
        reg_type = data.get("region_type", "Urban")

        if reg_type.lower() == "urban":
            base_input = {
                "Region_Name": "Simulated Urban Megacity",
                "Region_Type": "Urban",
                "Population": 300000 * (1.0 + pop_growth / 100.0),
                "Population_Density": 4200 * (1.0 + pop_growth / 100.0),
                "Household_Size": 4.1,
                "Avg_Temperature_C": 32.0 + temp_anomaly,
                "Rainfall_mm": max(0.0, 50.0 * rain_factor),
                "Industrial_Index": max(0.0, min(100.0, 70.0 + ind_change)),
                "Agricultural_Index": max(0.0, min(100.0, 10.0 + agr_change)),
                "Water_Piped_Coverage_Pct": 94.0,
                "Electrification_Pct": 99.0,
                "Season": "Summer"
            }
        else:
            base_input = {
                "Region_Name": "Simulated Rural Taluk",
                "Region_Type": "Rural",
                "Population": 80000 * (1.0 + pop_growth / 100.0),
                "Population_Density": 210 * (1.0 + pop_growth / 100.0),
                "Household_Size": 5.2,
                "Avg_Temperature_C": 33.0 + temp_anomaly,
                "Rainfall_mm": max(0.0, 35.0 * rain_factor),
                "Industrial_Index": max(0.0, min(100.0, 15.0 + ind_change)),
                "Agricultural_Index": max(0.0, min(100.0, 85.0 + agr_change)),
                "Water_Piped_Coverage_Pct": 48.0,
                "Electrification_Pct": 88.0,
                "Season": "Summer"
            }

        sim_res = predictor.predict_single(base_input)
        return jsonify({"status": "success", "simulation_inputs": base_input, "results": sim_res}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/analytics/summary", methods=["GET"])
def api_summary():
    return jsonify({
        "kpis": analytics.get_summary_kpis(),
        "trends": analytics.get_time_series_trends(),
        "metrics": predictor.metrics
    })

@app.route("/api/analytics/correlation", methods=["GET"])
def api_correlation():
    return jsonify(analytics.get_correlation_matrix())

@app.route("/api/download/dataset", methods=["GET"])
def download_dataset():
    if os.path.exists(DATA_PATH):
        return send_file(DATA_PATH, as_attachment=True, download_name="water_energy_demand_data.csv")
    return "Dataset file not found", 404

@app.route("/api/upload", methods=["POST"])
def upload_dataset():
    global predictor, analytics
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"status": "error", "message": "Only CSV files are supported"}), 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], "water_energy_demand.csv")
    file.save(save_path)

    try:
        trainer = ModelTrainer(data_path=save_path, models_dir=MODELS_DIR)
        metrics = trainer.train_and_evaluate()
        predictor = DemandPredictor(models_dir=MODELS_DIR)
        analytics = DemandAnalytics(data_path=save_path)
        return jsonify({
            "status": "success", 
            "message": "Dataset uploaded and models retrained successfully!",
            "metrics": metrics
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Training failed: {str(e)}"}), 500

@app.route("/api/retrain", methods=["POST"])
def retrain_models():
    global predictor, analytics
    try:
        trainer = ModelTrainer(data_path=DATA_PATH, models_dir=MODELS_DIR)
        metrics = trainer.train_and_evaluate()
        predictor = DemandPredictor(models_dir=MODELS_DIR)
        analytics = DemandAnalytics(data_path=DATA_PATH)
        return jsonify({"status": "success", "message": "Models retrained successfully", "metrics": metrics}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
