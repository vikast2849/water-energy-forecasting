import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = [
    "Population",
    "Population_Density",
    "Household_Size",
    "Avg_Temperature_C",
    "Rainfall_mm",
    "Industrial_Index",
    "Agricultural_Index",
    "Water_Piped_Coverage_Pct",
    "Electrification_Pct",
    "Is_Urban",
    "Season_Summer",
    "Season_Monsoon",
    "Season_Winter",
    "Thermal_Stress_Index",
    "Dryness_Factor"
]

class DemandPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = FEATURE_COLUMNS
        self.is_fitted = False

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        
        # Binary Urban/Rural
        if "Region_Type" in data.columns:
            data["Is_Urban"] = (data["Region_Type"].astype(str).str.lower() == "urban").astype(int)
        elif "Is_Urban" not in data.columns:
            data["Is_Urban"] = 1

        # Season one-hot flags
        if "Season" in data.columns:
            season_col = data["Season"].astype(str).str.capitalize()
            data["Season_Summer"] = (season_col == "Summer").astype(int)
            data["Season_Monsoon"] = (season_col == "Monsoon").astype(int)
            data["Season_Winter"] = (season_col == "Winter").astype(int)
        else:
            for s in ["Summer", "Monsoon", "Winter"]:
                if f"Season_{s}" not in data.columns:
                    data[f"Season_{s}"] = 0

        # Domain feature engineering
        temp = data["Avg_Temperature_C"].astype(float)
        rain = data["Rainfall_mm"].astype(float)

        data["Thermal_Stress_Index"] = temp / 30.0
        data["Dryness_Factor"] = temp / (rain + 15.0)

        # Fill missing values if any
        for col in self.feature_names:
            if col not in data.columns:
                data[col] = 0.0
            else:
                data[col] = data[col].fillna(data[col].median() if len(data) > 1 else 0.0)

        return data[self.feature_names]

    def fit_transform(self, df: pd.DataFrame):
        engineered_df = self._engineer_features(df)
        X_scaled = self.scaler.fit_transform(engineered_df)
        self.is_fitted = True
        return X_scaled, engineered_df

    def transform(self, df: pd.DataFrame):
        if not self.is_fitted:
            raise RuntimeError("DemandPreprocessor is not fitted yet.")
        engineered_df = self._engineer_features(df)
        X_scaled = self.scaler.transform(engineered_df)
        return X_scaled, engineered_df

    def save(self, directory: str):
        os.makedirs(directory, exist_ok=True)
        joblib.dump(self.scaler, os.path.join(directory, "scaler.joblib"))
        joblib.dump(self.feature_names, os.path.join(directory, "feature_names.joblib"))

    def load(self, directory: str):
        scaler_path = os.path.join(directory, "scaler.joblib")
        names_path = os.path.join(directory, "feature_names.joblib")
        if os.path.exists(scaler_path) and os.path.exists(names_path):
            self.scaler = joblib.load(scaler_path)
            self.feature_names = joblib.load(names_path)
            self.is_fitted = True
        else:
            raise FileNotFoundError(f"Scaler files missing in {directory}")
