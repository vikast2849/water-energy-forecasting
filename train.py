import os
import sys

# Ensure current dir is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.models import ModelTrainer

def main():
    data_file = os.path.join(BASE_DIR, "data", "water_energy_demand.csv")
    models_dir = os.path.join(BASE_DIR, "saved_models")
    
    print(f"Starting model training on: {data_file}")
    trainer = ModelTrainer(data_path=data_file, models_dir=models_dir)
    metrics = trainer.train_and_evaluate()
    
    print("\n--- MODEL PERFORMANCE RESULTS ---")
    print("WATER DEMAND FORECASTING (R2 Score):")
    for m, vals in metrics["Water_Demand"].items():
        print(f"  {m}: R2 = {vals['R2_Pct']}%, MAE = {vals['MAE']}, RMSE = {vals['RMSE']}, 5-Fold CV R2 = {vals['CV_5Fold_R2']}%")

    print("\nENERGY DEMAND FORECASTING (R2 Score):")
    for m, vals in metrics["Energy_Demand"].items():
        print(f"  {m}: R2 = {vals['R2_Pct']}%, MAE = {vals['MAE']}, RMSE = {vals['RMSE']}, 5-Fold CV R2 = {vals['CV_5Fold_R2']}%")

    print("\nSCARCITY RISK CLASSIFICATION (Accuracy & F1):")
    for m, vals in metrics["Scarcity_Classification"].items():
        print(f"  {m}: Accuracy = {vals['Accuracy_Pct']}%, Precision = {vals['Precision']}, Recall = {vals['Recall']}, F1 = {vals['F1_Score']}")

if __name__ == "__main__":
    main()
