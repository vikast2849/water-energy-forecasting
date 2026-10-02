import os
import numpy as np
import pandas as pd

class DemandAnalytics:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

    def get_summary_kpis(self):
        total_records = len(self.df)
        avg_water_mld = round(self.df["Water_Demand_MLD"].mean(), 2)
        avg_energy_mwh = round(self.df["Energy_Demand_MWh"].mean(), 2)
        
        urban_df = self.df[self.df["Region_Type"].str.lower() == "urban"]
        rural_df = self.df[self.df["Region_Type"].str.lower() == "rural"]

        urban_lpcd = round(urban_df["Water_LPCD"].mean(), 1)
        rural_lpcd = round(rural_df["Water_LPCD"].mean(), 1)

        urban_kwh = round(urban_df["Energy_kWh_Capita"].mean(), 2)
        rural_kwh = round(rural_df["Energy_kWh_Capita"].mean(), 2)

        high_risk_count = int((self.df["Scarcity_Risk"] == 1).sum())
        high_risk_pct = round((high_risk_count / total_records) * 100, 1)

        return {
            "total_records": total_records,
            "regions_count": int(self.df["Region_Name"].nunique()),
            "avg_water_mld": avg_water_mld,
            "avg_energy_mwh": avg_energy_mwh,
            "urban_lpcd": urban_lpcd,
            "rural_lpcd": rural_lpcd,
            "urban_kwh_capita": urban_kwh,
            "rural_kwh_capita": rural_kwh,
            "high_risk_pct": high_risk_pct,
            "high_risk_count": high_risk_count,
            "water_disparity_ratio": round(urban_lpcd / max(rural_lpcd, 1), 2),
            "energy_disparity_ratio": round(urban_kwh / max(rural_kwh, 0.1), 2)
        }

    def get_urban_rural_comparison(self):
        grouped = self.df.groupby(["Region_Type", "Season"]).agg({
            "Water_Demand_MLD": "mean",
            "Energy_Demand_MWh": "mean",
            "Water_LPCD": "mean",
            "Energy_kWh_Capita": "mean",
            "Scarcity_Risk": "mean"
        }).reset_index()

        # Format for charts
        result = {}
        for r_type in ["Urban", "Rural"]:
            sub = grouped[grouped["Region_Type"] == r_type]
            result[r_type] = {
                "seasons": sub["Season"].tolist(),
                "water_mld": [round(x, 2) for x in sub["Water_Demand_MLD"]],
                "energy_mwh": [round(x, 2) for x in sub["Energy_Demand_MWh"]],
                "water_lpcd": [round(x, 1) for x in sub["Water_LPCD"]],
                "energy_kwh": [round(x, 2) for x in sub["Energy_kWh_Capita"]],
                "scarcity_rate": [round(x * 100, 1) for x in sub["Scarcity_Risk"]]
            }
        return result

    def get_time_series_trends(self):
        # Yearly averages for Urban and Rural
        yearly = self.df.groupby(["Year", "Region_Type"]).agg({
            "Water_Demand_MLD": "mean",
            "Energy_Demand_MWh": "mean"
        }).reset_index()

        years = sorted(self.df["Year"].unique().tolist())
        urban_water = [round(float(yearly[(yearly["Year"] == y) & (yearly["Region_Type"] == "Urban")]["Water_Demand_MLD"].values[0]), 2) for y in years]
        rural_water = [round(float(yearly[(yearly["Year"] == y) & (yearly["Region_Type"] == "Rural")]["Water_Demand_MLD"].values[0]), 2) for y in years]

        urban_energy = [round(float(yearly[(yearly["Year"] == y) & (yearly["Region_Type"] == "Urban")]["Energy_Demand_MWh"].values[0]), 2) for y in years]
        rural_energy = [round(float(yearly[(yearly["Year"] == y) & (yearly["Region_Type"] == "Rural")]["Energy_Demand_MWh"].values[0]), 2) for y in years]

        # Forecast forward to 2035 using compound growth trends
        forecast_years = list(range(2026, 2036))
        
        last_u_w, last_r_w = urban_water[-1], rural_water[-1]
        last_u_e, last_r_e = urban_energy[-1], rural_energy[-1]

        f_u_water = []
        f_r_water = []
        f_u_energy = []
        f_r_energy = []

        for i, y in enumerate(forecast_years, 1):
            # Urban growth: 2.2% annual, rural growth: 1.1% annual
            f_u_water.append(round(last_u_w * ((1.023) ** i), 2))
            f_r_water.append(round(last_r_w * ((1.012) ** i), 2))
            f_u_energy.append(round(last_u_e * ((1.031) ** i), 2))
            f_r_energy.append(round(last_r_e * ((1.018) ** i), 2))

        return {
            "historical_years": years,
            "forecast_years": forecast_years,
            "all_years": years + forecast_years,
            "urban_water_historical": urban_water,
            "rural_water_historical": rural_water,
            "urban_water_forecast": f_u_water,
            "rural_water_forecast": f_r_water,
            "urban_energy_historical": urban_energy,
            "rural_energy_historical": rural_energy,
            "urban_energy_forecast": f_u_energy,
            "rural_energy_forecast": f_r_energy
        }

    def get_correlation_matrix(self):
        numeric_cols = [
            "Population", "Population_Density", "Avg_Temperature_C", "Rainfall_mm",
            "Industrial_Index", "Agricultural_Index", "Water_Demand_MLD", "Energy_Demand_MWh", "Scarcity_Risk"
        ]
        corr = self.df[numeric_cols].corr().round(3)
        return {
            "columns": numeric_cols,
            "values": corr.values.tolist()
        }

    def get_regional_breakdown(self):
        reg = self.df.groupby(["Region_Name", "Region_Type"]).agg({
            "Population": "mean",
            "Water_Demand_MLD": "mean",
            "Energy_Demand_MWh": "mean",
            "Water_LPCD": "mean",
            "Energy_kWh_Capita": "mean",
            "Scarcity_Risk": "mean"
        }).reset_index()

        records = []
        for _, row in reg.iterrows():
            records.append({
                "name": row["Region_Name"],
                "type": row["Region_Type"],
                "population": int(row["Population"]),
                "water_mld": round(row["Water_Demand_MLD"], 2),
                "energy_mwh": round(row["Energy_Demand_MWh"], 2),
                "water_lpcd": round(row["Water_LPCD"], 1),
                "energy_kwh": round(row["Energy_kWh_Capita"], 2),
                "risk_pct": round(row["Scarcity_Risk"] * 100, 1)
            })
        return records
