import os
import numpy as np
import pandas as pd

def generate_water_energy_data(n_samples_per_region=120, random_seed=42):
    np.random.seed(random_seed)

    regions = [
        # Urban Centers
        {"name": "Chitradurga Urban", "type": "Urban", "base_pop": 210000, "pop_density": 3800, "ind_idx": 65, "agr_idx": 8, "piped_pct": 92, "elec_pct": 99},
        {"name": "Davanagere City", "type": "Urban", "base_pop": 480000, "pop_density": 5200, "ind_idx": 78, "agr_idx": 12, "piped_pct": 95, "elec_pct": 100},
        {"name": "Bengaluru Peri-Urban", "type": "Urban", "base_pop": 950000, "pop_density": 7800, "ind_idx": 88, "agr_idx": 5, "piped_pct": 96, "elec_pct": 100},
        {"name": "Hubballi-Dharwad Urban", "type": "Urban", "base_pop": 620000, "pop_density": 4600, "ind_idx": 72, "agr_idx": 10, "piped_pct": 91, "elec_pct": 98},
        {"name": "Ballari Industrial Urban", "type": "Urban", "base_pop": 390000, "pop_density": 4100, "ind_idx": 85, "agr_idx": 7, "piped_pct": 89, "elec_pct": 97},
        
        # Rural Taluks & Farming Clusters
        {"name": "Challakere Rural", "type": "Rural", "base_pop": 85000, "pop_density": 210, "ind_idx": 15, "agr_idx": 88, "piped_pct": 48, "elec_pct": 86},
        {"name": "Hiriyur Agro-Cluster", "type": "Rural", "base_pop": 92000, "pop_density": 240, "ind_idx": 18, "agr_idx": 92, "piped_pct": 52, "elec_pct": 88},
        {"name": "Holalkere Rural", "type": "Rural", "base_pop": 68000, "pop_density": 190, "ind_idx": 12, "agr_idx": 82, "piped_pct": 45, "elec_pct": 85},
        {"name": "Hosadurga Rural", "type": "Rural", "base_pop": 76000, "pop_density": 205, "ind_idx": 14, "agr_idx": 85, "piped_pct": 49, "elec_pct": 87},
        {"name": "Molakalmuru Drylands", "type": "Rural", "base_pop": 54000, "pop_density": 165, "ind_idx": 10, "agr_idx": 79, "piped_pct": 38, "elec_pct": 82},
        {"name": "Jagalur Agricultural Basin", "type": "Rural", "base_pop": 62000, "pop_density": 180, "ind_idx": 11, "agr_idx": 84, "piped_pct": 42, "elec_pct": 84}
    ]

    records = []
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    months = list(range(1, 13))

    for region in regions:
        reg_name = region["name"]
        reg_type = region["type"]
        is_urban = 1 if reg_type == "Urban" else 0

        for year in years:
            # Year-over-year population growth: urban grows faster (1.8-2.5%), rural slower (0.8-1.2%)
            growth_mult = (1 + (0.022 if is_urban else 0.009)) ** (year - 2019)
            base_pop = region["base_pop"] * growth_mult

            for month in months:
                # Season determination
                if month in [3, 4, 5]:
                    season = "Summer"
                    temp_mean = 35.5 if is_urban else 36.2
                    rain_mean = 18.0
                elif month in [6, 7, 8, 9]:
                    season = "Monsoon"
                    temp_mean = 27.5 if is_urban else 27.0
                    rain_mean = 145.0
                else:
                    season = "Winter"
                    temp_mean = 24.0 if is_urban else 23.0
                    rain_mean = 12.0

                temp = np.clip(np.random.normal(temp_mean, 2.2), 16.0, 43.0)
                rain = np.clip(np.random.exponential(rain_mean), 0.0, 380.0)

                # Population variations (seasonal migration, festive periods)
                pop_noise = np.random.normal(1.0, 0.02)
                current_pop = int(base_pop * pop_noise)

                # Household size: urban smaller, rural larger
                hh_size = round(float(np.random.normal(3.9 if is_urban else 5.4, 0.3)), 1)
                
                # Densities & Indices
                density = int(region["pop_density"] * growth_mult * np.random.normal(1.0, 0.01))
                ind_idx = np.clip(region["ind_idx"] + np.random.normal(0, 3), 0, 100)
                agr_idx = np.clip(region["agr_idx"] + np.random.normal(0, 3), 0, 100)
                piped_cov = np.clip(region["piped_pct"] + (year - 2019) * 0.8 + np.random.normal(0, 1.5), 25, 99.5)
                elec_cov = np.clip(region["elec_pct"] + (year - 2019) * 0.5 + np.random.normal(0, 1.0), 75, 100.0)

                # WATER DEMAND MODELING (Million Litres per Day - MLD)
                if is_urban:
                    domestic_lpcd = 135.0 + (temp - 25.0) * 1.8 + np.random.normal(0, 4.0)
                    industrial_water_mld = (ind_idx / 100.0) * (current_pop / 100000.0) * 8.5
                    water_mld = (current_pop * domestic_lpcd / 1_000_000.0) + industrial_water_mld
                else:
                    domestic_lpcd = 70.0 + (temp - 25.0) * 1.1 + np.random.normal(0, 3.0)
                    irrigation_mult = max(0.2, (40.0 - min(rain, 35.0)) / 35.0) * (temp / 28.0)
                    agri_water_mld = (agr_idx / 100.0) * (current_pop / 50000.0) * 14.0 * irrigation_mult
                    water_mld = (current_pop * domestic_lpcd / 1_000_000.0) + agri_water_mld

                water_mld = max(0.5, round(float(water_mld), 2))

                # ENERGY DEMAND MODELING (Megawatt-Hours per Day - MWh)
                if is_urban:
                    domestic_kwh_per_capita = 3.4 + max(0, (temp - 26.0) * 0.22) + np.random.normal(0, 0.15)
                    industrial_energy_mwh = (ind_idx / 100.0) * (current_pop / 10000.0) * 15.0
                    energy_mwh = (current_pop * domestic_kwh_per_capita / 1000.0) + industrial_energy_mwh
                else:
                    domestic_kwh_per_capita = 1.3 + (temp - 25.0) * 0.05 + np.random.normal(0, 0.08)
                    agri_pump_mwh = (agr_idx / 100.0) * (current_pop / 20000.0) * 18.0 * (1.6 if season == "Summer" else (0.7 if season == "Monsoon" else 1.2))
                    energy_mwh = (current_pop * domestic_kwh_per_capita / 1000.0) + agri_pump_mwh

                energy_mwh = max(1.0, round(float(energy_mwh), 2))

                # Per capita indicators
                water_lpcd_effective = round((water_mld * 1_000_000.0) / current_pop, 1)
                energy_kwh_per_capita_effective = round((energy_mwh * 1000.0) / current_pop, 2)

                # Scarcity Risk Calculation
                if is_urban:
                    stress_score = 0.35 * (temp / 38.0) + 0.30 * (density / 7500.0) + 0.25 * (ind_idx / 90.0) - 0.10 * (rain / 200.0)
                else:
                    stress_score = 0.45 * (temp / 38.0) + 0.40 * (agr_idx / 95.0) - 0.35 * (rain / 150.0) + 0.15 * (100.0 - piped_cov) / 100.0

                stress_score += np.random.normal(0, 0.08)

                if stress_score > 0.65:
                    stress_level = "Critical"
                    scarcity_risk = 1
                elif stress_score > 0.50:
                    stress_level = "High"
                    scarcity_risk = 1
                elif stress_score > 0.35:
                    stress_level = "Moderate"
                    scarcity_risk = 0
                else:
                    stress_level = "Low"
                    scarcity_risk = 0

                records.append({
                    "Region_Name": reg_name,
                    "Region_Type": reg_type,
                    "Year": year,
                    "Month": month,
                    "Season": season,
                    "Population": current_pop,
                    "Population_Density": density,
                    "Household_Size": hh_size,
                    "Avg_Temperature_C": round(float(temp), 1),
                    "Rainfall_mm": round(float(rain), 1),
                    "Industrial_Index": round(float(ind_idx), 1),
                    "Agricultural_Index": round(float(agr_idx), 1),
                    "Water_Piped_Coverage_Pct": round(float(piped_cov), 1),
                    "Electrification_Pct": round(float(elec_cov), 1),
                    "Water_Demand_MLD": water_mld,
                    "Energy_Demand_MWh": energy_mwh,
                    "Water_LPCD": water_lpcd_effective,
                    "Energy_kWh_Capita": energy_kwh_per_capita_effective,
                    "Demand_Stress_Level": stress_level,
                    "Scarcity_Risk": scarcity_risk
                })

    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(out_dir, "water_energy_demand.csv")
    df = generate_water_energy_data()
    df.to_csv(data_path, index=False)
    print(f"Dataset successfully generated with {len(df)} records across {df['Region_Name'].nunique()} regions.")
    print(f"Saved to: {data_path}")
