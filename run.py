import os
import sys

# Ensure project root is in python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app

if __name__ == "__main__":
    print("==================================================================")
    print("  Population-Driven Water & Energy Demand Forecasting Framework  ")
    print("  Dept. of CS&E, SJMIT Chitradurga (2026-2027)                  ")
    print("  Models Active: SVM | KNN | Logistic Regression                ")
    print("==================================================================")
    print("  Starting Web Application at: http://127.0.0.1:5000            ")
    print("  Press CTRL+C to stop the server                                ")
    print("==================================================================")
    app.run(host="0.0.0.0", port=5000, debug=False)
