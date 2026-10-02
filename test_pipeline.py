import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app
from ml.models import DemandPredictor

class TestDemandForecastingSystem(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.models_dir = os.path.join(BASE_DIR, "saved_models")
        self.predictor = DemandPredictor(self.models_dir)

    def test_01_models_loaded_and_metrics_target(self):
        """Verify models are loaded and all metrics exceed the >85% requirement."""
        self.assertTrue(len(self.predictor.models) >= 8)
        metrics = self.predictor.metrics
        
        svm_w_r2 = metrics["Water_Demand"]["SVM"]["R2_Pct"]
        knn_w_r2 = metrics["Water_Demand"]["KNN"]["R2_Pct"]
        self.assertGreater(svm_w_r2, 85.0)
        self.assertGreater(knn_w_r2, 85.0)

        svm_e_r2 = metrics["Energy_Demand"]["SVM"]["R2_Pct"]
        knn_e_r2 = metrics["Energy_Demand"]["KNN"]["R2_Pct"]
        self.assertGreater(svm_e_r2, 85.0)
        self.assertGreater(knn_e_r2, 85.0)

        log_acc = metrics["Scarcity_Classification"]["Logistic_Regression"]["Accuracy_Pct"]
        self.assertGreater(log_acc, 85.0)
        print(f"\n[PASS] Model Verification: SVM Water R²={svm_w_r2}%, KNN Water R²={knn_w_r2}%, LogReg Acc={log_acc}%")

    def test_02_web_and_auth_endpoints(self):
        """Verify unauthenticated requests redirect to /login, and authenticated requests get 200 OK."""
        # Unauthenticated access to root / should redirect to /login
        res_root = self.app.get("/")
        self.assertEqual(res_root.status_code, 302)

        # Login
        self.app.post("/login", data={"username": "officer@sjmit.ac.in", "password": "password123"})

        # Now all protected routes return 200 OK
        routes = ["/home", "/dashboard", "/login", "/register", "/forgot-password", "/map", "/predict", "/comparative", "/models", "/simulation", "/dataset", "/report"]
        for route in routes:
            response = self.app.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")
            print(f"[PASS] Authenticated HTTP Route: {route} -> 200 OK")

    def test_03_password_reset(self):
        """Verify password reset workflow."""
        reset_payload = {
            "email": "officer@sjmit.ac.in",
            "otp_code": "849201",
            "new_password": "newpassword456",
            "confirm_password": "newpassword456"
        }
        res = self.app.post("/forgot-password", data=reset_payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"successfully reset", res.data)

        # Verify can login with new password
        login_data = {
            "username": "officer@sjmit.ac.in",
            "password": "newpassword456"
        }
        res_login = self.app.post("/login", data=login_data, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        print(f"[PASS] Password Reset & Re-Authentication verified")

    def test_03_login_authentication(self):
        """Verify user login and session authentication."""
        login_data = {
            "username": "officer@sjmit.ac.in",
            "password": "password123"
        }
        res = self.app.post("/login", data=login_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        print(f"[PASS] Authentication & Session Management verified")

    def test_04_api_predict(self):
        """Verify POST /api/predict returns valid JSON."""
        payload = {
            "Region_Name": "Chitradurga Urban Core",
            "Region_Type": "Urban",
            "Population": 220000,
            "Population_Density": 3900,
            "Household_Size": 4.0,
            "Avg_Temperature_C": 36.5,
            "Rainfall_mm": 15.0,
            "Industrial_Index": 68.0,
            "Agricultural_Index": 8.0,
            "Water_Piped_Coverage_Pct": 92.0,
            "Electrification_Pct": 99.0,
            "Season": "Summer"
        }
        response = self.app.post("/api/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        print(f"[PASS] REST API /api/predict returned success")

if __name__ == "__main__":
    unittest.main()
