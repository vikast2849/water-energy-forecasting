import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from ml.preprocessor import DemandPreprocessor

class ModelTrainer:
    def __init__(self, data_path: str, models_dir: str):
        self.data_path = data_path
        self.models_dir = models_dir
        self.preprocessor = DemandPreprocessor()
        self.models = {}
        self.metrics = {}

    def train_and_evaluate(self):
        df = pd.read_csv(self.data_path)
        
        # Preprocessing
        X_scaled, engineered_df = self.preprocessor.fit_transform(df)
        y_water = df["Water_Demand_MLD"].values
        y_energy = df["Energy_Demand_MWh"].values
        y_scarcity = df["Scarcity_Risk"].values

        # Split train/test (80/20)
        indices = np.arange(len(df))
        train_idx, test_idx = train_test_split(indices, test_size=0.2, random_state=42, stratify=y_scarcity)

        X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
        y_w_train, y_w_test = y_water[train_idx], y_water[test_idx]
        y_e_train, y_e_test = y_energy[train_idx], y_energy[test_idx]
        y_s_train, y_s_test = y_scarcity[train_idx], y_scarcity[test_idx]

        # 5-Fold Cross Validation Setup (per Chapter 5.11)
        kf = KFold(n_splits=5, shuffle=True, random_state=42)

        # ---------------------------------------------------------------------
        # MODEL 1: SUPPORT VECTOR MACHINE (SVM / SVR / SVC)
        # ---------------------------------------------------------------------
        svm_water = SVR(kernel='rbf', C=100.0, epsilon=0.1, gamma='scale')
        svm_water.fit(X_train, y_w_train)
        pred_w_svm = svm_water.predict(X_test)
        cv_w_svm = cross_val_score(svm_water, X_scaled, y_water, cv=kf, scoring='r2').mean()

        svm_energy = SVR(kernel='rbf', C=150.0, epsilon=0.1, gamma='scale')
        svm_energy.fit(X_train, y_e_train)
        pred_e_svm = svm_energy.predict(X_test)
        cv_e_svm = cross_val_score(svm_energy, X_scaled, y_energy, cv=kf, scoring='r2').mean()

        svm_clf = SVC(kernel='rbf', C=10.0, probability=True, random_state=42)
        svm_clf.fit(X_train, y_s_train)
        pred_s_svm = svm_clf.predict(X_test)
        cv_s_svm = cross_val_score(svm_clf, X_scaled, y_scarcity, cv=kf, scoring='accuracy').mean()

        # ---------------------------------------------------------------------
        # MODEL 2: K-NEAREST NEIGHBORS (KNN)
        # ---------------------------------------------------------------------
        knn_water = KNeighborsRegressor(n_neighbors=5, weights='distance', algorithm='auto')
        knn_water.fit(X_train, y_w_train)
        pred_w_knn = knn_water.predict(X_test)
        cv_w_knn = cross_val_score(knn_water, X_scaled, y_water, cv=kf, scoring='r2').mean()

        knn_energy = KNeighborsRegressor(n_neighbors=5, weights='distance', algorithm='auto')
        knn_energy.fit(X_train, y_e_train)
        pred_e_knn = knn_energy.predict(X_test)
        cv_e_knn = cross_val_score(knn_energy, X_scaled, y_energy, cv=kf, scoring='r2').mean()

        knn_clf = KNeighborsClassifier(n_neighbors=5, weights='distance')
        knn_clf.fit(X_train, y_s_train)
        pred_s_knn = knn_clf.predict(X_test)
        cv_s_knn = cross_val_score(knn_clf, X_scaled, y_scarcity, cv=kf, scoring='accuracy').mean()

        # ---------------------------------------------------------------------
        # MODEL 3: LOGISTIC REGRESSION (AND LINEAR BASELINE FOR RESOURCE DEMAND)
        # ---------------------------------------------------------------------
        log_clf = LogisticRegression(max_iter=1000, C=1.0, random_state=42, class_weight='balanced')
        log_clf.fit(X_train, y_s_train)
        pred_s_log = log_clf.predict(X_test)
        pred_s_log_prob = log_clf.predict_proba(X_test)[:, 1]
        cv_s_log = cross_val_score(log_clf, X_scaled, y_scarcity, cv=kf, scoring='accuracy').mean()

        linear_water = Ridge(alpha=1.0)
        linear_water.fit(X_train, y_w_train)
        pred_w_lin = linear_water.predict(X_test)
        cv_w_lin = cross_val_score(linear_water, X_scaled, y_water, cv=kf, scoring='r2').mean()

        linear_energy = Ridge(alpha=1.0)
        linear_energy.fit(X_train, y_e_train)
        pred_e_lin = linear_energy.predict(X_test)
        cv_e_lin = cross_val_score(linear_energy, X_scaled, y_energy, cv=kf, scoring='r2').mean()

        # ---------------------------------------------------------------------
        # COMPUTE EVALUATION METRICS
        # ---------------------------------------------------------------------
        def reg_metrics(y_true, y_pred, cv_r2):
            return {
                "MAE": round(float(mean_absolute_error(y_true, y_pred)), 3),
                "RMSE": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 3),
                "R2_Score": round(float(r2_score(y_true, y_pred)), 4),
                "R2_Pct": round(float(r2_score(y_true, y_pred) * 100), 2),
                "CV_5Fold_R2": round(float(cv_r2 * 100), 2)
            }

        def clf_metrics(y_true, y_pred, cv_acc):
            cm = confusion_matrix(y_true, y_pred).tolist()
            return {
                "Accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
                "Accuracy_Pct": round(float(accuracy_score(y_true, y_pred) * 100), 2),
                "Precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 3),
                "Recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 3),
                "F1_Score": round(float(f1_score(y_true, y_pred, zero_division=0)), 3),
                "CV_5Fold_Accuracy": round(float(cv_acc * 100), 2),
                "Confusion_Matrix": cm
            }

        self.metrics = {
            "Water_Demand": {
                "SVM": reg_metrics(y_w_test, pred_w_svm, cv_w_svm),
                "KNN": reg_metrics(y_w_test, pred_w_knn, cv_w_knn),
                "Linear_Regression": reg_metrics(y_w_test, pred_w_lin, cv_w_lin)
            },
            "Energy_Demand": {
                "SVM": reg_metrics(y_e_test, pred_e_svm, cv_e_svm),
                "KNN": reg_metrics(y_e_test, pred_e_knn, cv_e_knn),
                "Linear_Regression": reg_metrics(y_e_test, pred_e_lin, cv_e_lin)
            },
            "Scarcity_Classification": {
                "Logistic_Regression": clf_metrics(y_s_test, pred_s_log, cv_s_log),
                "SVM_Classifier": clf_metrics(y_s_test, pred_s_svm, cv_s_svm),
                "KNN_Classifier": clf_metrics(y_s_test, pred_s_knn, cv_s_knn)
            },
            "Feature_Coefficients_Logistic": {
                feat: round(float(coef), 4)
                for feat, coef in zip(self.preprocessor.feature_names, log_clf.coef_[0])
            },
            "Dataset_Summary": {
                "Total_Records": len(df),
                "Urban_Records": int((df["Region_Type"].str.lower() == "urban").sum()),
                "Rural_Records": int((df["Region_Type"].str.lower() == "rural").sum()),
                "Regions_Count": int(df["Region_Name"].nunique()),
                "Features_Count": len(self.preprocessor.feature_names),
                "Years_Covered": f"{df['Year'].min()} - {df['Year'].max()}"
            }
        }

        # Store models
        self.models = {
            "svm_water": svm_water,
            "svm_energy": svm_energy,
            "svm_clf": svm_clf,
            "knn_water": knn_water,
            "knn_energy": knn_energy,
            "knn_clf": knn_clf,
            "logistic_clf": log_clf,
            "linear_water": linear_water,
            "linear_energy": linear_energy
        }

        self.save_artifacts()
        return self.metrics

    def save_artifacts(self):
        os.makedirs(self.models_dir, exist_ok=True)
        self.preprocessor.save(self.models_dir)
        
        for name, model in self.models.items():
            joblib.dump(model, os.path.join(self.models_dir, f"{name}.joblib"))

        metrics_file = os.path.join(self.models_dir, "metrics.json")
        with open(metrics_file, "w") as f:
            json.dump(self.metrics, f, indent=4)
        print(f"All models and metrics successfully saved to {self.models_dir}")


class DemandPredictor:
    def __init__(self, models_dir: str):
        self.models_dir = models_dir
        self.preprocessor = DemandPreprocessor()
        self.preprocessor.load(models_dir)
        
        self.models = {}
        for name in ["svm_water", "svm_energy", "svm_clf", "knn_water", "knn_energy", "knn_clf", "logistic_clf", "linear_water", "linear_energy"]:
            model_path = os.path.join(models_dir, f"{name}.joblib")
            if os.path.exists(model_path):
                self.models[name] = joblib.load(model_path)
            else:
                raise FileNotFoundError(f"Missing model: {model_path}")

        metrics_path = os.path.join(models_dir, "metrics.json")
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                self.metrics = json.load(f)
        else:
            self.metrics = {}

    def predict_single(self, input_dict: dict) -> dict:
        input_df = pd.DataFrame([input_dict])
        X_scaled, _ = self.preprocessor.transform(input_df)

        # 1. SVM Predictions
        svm_w = float(self.models["svm_water"].predict(X_scaled)[0])
        svm_e = float(self.models["svm_energy"].predict(X_scaled)[0])
        svm_risk_prob = float(self.models["svm_clf"].predict_proba(X_scaled)[0][1])
        svm_risk_cls = int(self.models["svm_clf"].predict(X_scaled)[0])

        # 2. KNN Predictions
        knn_w = float(self.models["knn_water"].predict(X_scaled)[0])
        knn_e = float(self.models["knn_energy"].predict(X_scaled)[0])
        knn_risk_prob = float(self.models["knn_clf"].predict_proba(X_scaled)[0][1])
        knn_risk_cls = int(self.models["knn_clf"].predict(X_scaled)[0])

        # 3. Logistic Regression & Linear
        log_risk_prob = float(self.models["logistic_clf"].predict_proba(X_scaled)[0][1])
        log_risk_cls = int(self.models["logistic_clf"].predict(X_scaled)[0])
        lin_w = float(self.models["linear_water"].predict(X_scaled)[0])
        lin_e = float(self.models["linear_energy"].predict(X_scaled)[0])

        # Ensemble / Consensus Averages
        avg_w = round((svm_w * 0.45 + knn_w * 0.35 + lin_w * 0.20), 2)
        avg_e = round((svm_e * 0.45 + knn_e * 0.35 + lin_e * 0.20), 2)
        avg_risk_prob = round((svm_risk_prob * 0.35 + knn_risk_prob * 0.30 + log_risk_prob * 0.35), 3)

        pop = max(1, float(input_dict.get("Population", 100000)))
        lpcd = round((avg_w * 1_000_000.0) / pop, 1)
        kwh_capita = round((avg_e * 1000.0) / pop, 2)

        # Actionable insights generation based on context
        is_urban = str(input_dict.get("Region_Type", "")).lower() == "urban"
        actionable_insights = []
        if avg_risk_prob > 0.60:
            if is_urban:
                actionable_insights.append("CRITICAL: Implement urban water zoning, promote commercial greywater recycling, and shift non-essential industrial power loads to off-peak hours.")
            else:
                actionable_insights.append("CRITICAL: Agricultural drought stress detected. Restrict unmetered canal discharge, activate solar micro-irrigation scheduling, and stagger 3-phase agricultural power feeders.")
        elif avg_risk_prob > 0.35:
            actionable_insights.append("MODERATE STRESS: Monitor reservoir capacity and feeder substations. Encourage decentralized rainwater harvesting.")
        else:
            actionable_insights.append("STABLE DEMAND: Supply buffers are healthy. Maintain standard distribution schedules.")

        return {
            "Consensus_Forecast": {
                "Water_Demand_MLD": avg_w,
                "Energy_Demand_MWh": avg_e,
                "Scarcity_Probability": avg_risk_prob,
                "Scarcity_Risk_Level": "High Scarcity Risk" if avg_risk_prob >= 0.5 else "Normal Demand",
                "Water_LPCD": lpcd,
                "Energy_kWh_Capita": kwh_capita
            },
            "Model_Breakdown": {
                "SVM": {
                    "Water_Demand_MLD": round(svm_w, 2),
                    "Energy_Demand_MWh": round(svm_e, 2),
                    "Scarcity_Probability": round(svm_risk_prob, 3),
                    "Classification": "High Risk" if svm_risk_cls == 1 else "Normal"
                },
                "KNN": {
                    "Water_Demand_MLD": round(knn_w, 2),
                    "Energy_Demand_MWh": round(knn_e, 2),
                    "Scarcity_Probability": round(knn_risk_prob, 3),
                    "Classification": "High Risk" if knn_risk_cls == 1 else "Normal"
                },
                "Logistic_Regression": {
                    "Scarcity_Probability": round(log_risk_prob, 3),
                    "Classification": "High Risk" if log_risk_cls == 1 else "Normal",
                    "Linear_Water_Demand_MLD": round(lin_w, 2),
                    "Linear_Energy_Demand_MWh": round(lin_e, 2)
                }
            },
            "Input_Summary": input_dict,
            "Actionable_Insights": actionable_insights
        }
