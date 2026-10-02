// Charts initialization using Chart.js

const ChartTheme = {
    textColor: '#94a3b8',
    gridColor: 'rgba(99, 140, 219, 0.12)',
    waterColor: '#06b6d4',
    waterBg: 'rgba(6, 182, 212, 0.2)',
    energyColor: '#f59e0b',
    energyBg: 'rgba(245, 158, 11, 0.2)',
    urbanColor: '#38bdf8',
    ruralColor: '#10b981',
    svmColor: '#818cf8',
    knnColor: '#ec4899',
    logregColor: '#10b981'
};

// Global default styling for Chart.js
if (window.Chart) {
    Chart.defaults.color = ChartTheme.textColor;
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.9)';
    Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
    Chart.defaults.plugins.tooltip.bodyColor = '#f1f5f9';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(99, 140, 219, 0.3)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
}

window.renderDashboardCharts = function(trends) {
    const ctxTrend = document.getElementById('demandTrendsChart');
    if (!ctxTrend || !trends) return;

    // Combine historical and forecast labels
    const labels = trends.all_years;
    const nHist = trends.historical_years.length;

    // Build series
    const uWaterHist = trends.urban_water_historical.concat(Array(trends.forecast_years.length).fill(null));
    const uWaterFore = Array(nHist - 1).fill(null).concat([trends.urban_water_historical[nHist - 1]]).concat(trends.urban_water_forecast);

    const rWaterHist = trends.rural_water_historical.concat(Array(trends.forecast_years.length).fill(null));
    const rWaterFore = Array(nHist - 1).fill(null).concat([trends.rural_water_historical[nHist - 1]]).concat(trends.rural_water_forecast);

    new Chart(ctxTrend, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Urban Water Demand (Historical MLD)',
                    data: uWaterHist,
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    tension: 0.3,
                    borderWidth: 2.5,
                    fill: false
                },
                {
                    label: 'Urban Water Demand (ML Model Forecast 2026-35)',
                    data: uWaterFore,
                    borderColor: '#38bdf8',
                    borderDash: [6, 6],
                    tension: 0.3,
                    borderWidth: 2.5,
                    fill: false
                },
                {
                    label: 'Rural Water Demand (Historical MLD)',
                    data: rWaterHist,
                    borderColor: '#10b981',
                    tension: 0.3,
                    borderWidth: 2.5,
                    fill: false
                },
                {
                    label: 'Rural Water Demand (ML Model Forecast 2026-35)',
                    data: rWaterFore,
                    borderColor: '#10b981',
                    borderDash: [6, 6],
                    tension: 0.3,
                    borderWidth: 2.5,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { color: ChartTheme.gridColor } },
                y: { 
                    grid: { color: ChartTheme.gridColor },
                    title: { display: true, text: 'Demand in Million Litres / Day (MLD)' }
                }
            },
            plugins: {
                legend: { position: 'top', labels: { boxWidth: 14 } }
            }
        }
    });

    // Energy Trends Chart
    const ctxEnergy = document.getElementById('energyTrendsChart');
    if (ctxEnergy) {
        const uEnergyHist = trends.urban_energy_historical.concat(Array(trends.forecast_years.length).fill(null));
        const uEnergyFore = Array(nHist - 1).fill(null).concat([trends.urban_energy_historical[nHist - 1]]).concat(trends.urban_energy_forecast);

        const rEnergyHist = trends.rural_energy_historical.concat(Array(trends.forecast_years.length).fill(null));
        const rEnergyFore = Array(nHist - 1).fill(null).concat([trends.rural_energy_historical[nHist - 1]]).concat(trends.rural_energy_forecast);

        new Chart(ctxEnergy, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Urban Energy (Historical MWh)',
                        data: uEnergyHist,
                        borderColor: '#f59e0b',
                        tension: 0.3,
                        borderWidth: 2.5
                    },
                    {
                        label: 'Urban Energy (Forecast MWh)',
                        data: uEnergyFore,
                        borderColor: '#f59e0b',
                        borderDash: [6, 6],
                        tension: 0.3,
                        borderWidth: 2.5
                    },
                    {
                        label: 'Rural Energy (Historical MWh)',
                        data: rEnergyHist,
                        borderColor: '#a855f7',
                        tension: 0.3,
                        borderWidth: 2.5
                    },
                    {
                        label: 'Rural Energy (Forecast MWh)',
                        data: rEnergyFore,
                        borderColor: '#a855f7',
                        borderDash: [6, 6],
                        tension: 0.3,
                        borderWidth: 2.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: ChartTheme.gridColor } },
                    y: { 
                        grid: { color: ChartTheme.gridColor },
                        title: { display: true, text: 'Energy Demand (MWh/Day)' }
                    }
                },
                plugins: {
                    legend: { position: 'top', labels: { boxWidth: 14 } }
                }
            }
        });
    }
};

window.renderComparativeCharts = function(comp) {
    const ctxBar = document.getElementById('seasonalComparisonBar');
    if (ctxBar && comp) {
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['Summer', 'Monsoon', 'Winter'],
                datasets: [
                    {
                        label: 'Urban Water LPCD (Litres/Capita/Day)',
                        data: comp.Urban.water_lpcd,
                        backgroundColor: 'rgba(56, 189, 248, 0.8)',
                        borderRadius: 6
                    },
                    {
                        label: 'Rural Water LPCD (Litres/Capita/Day)',
                        data: comp.Rural.water_lpcd,
                        backgroundColor: 'rgba(16, 185, 129, 0.8)',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: ChartTheme.gridColor } },
                    y: { 
                        grid: { color: ChartTheme.gridColor },
                        title: { display: true, text: 'Litres per Capita per Day (LPCD)' }
                    }
                }
            }
        });
    }

    const ctxRadar = document.getElementById('disparityRadarChart');
    if (ctxRadar) {
        new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ['Population Density', 'Piped Water %', 'Domestic LPCD', 'Industrial Load', 'Electrification %', 'Drought Sensitivity'],
                datasets: [
                    {
                        label: 'Urban Sector Profile',
                        data: [95, 93, 85, 88, 98, 45],
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.25)',
                        borderWidth: 2
                    },
                    {
                        label: 'Rural Sector Profile',
                        data: [15, 48, 42, 14, 85, 88],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.25)',
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: ChartTheme.gridColor },
                        grid: { color: ChartTheme.gridColor },
                        pointLabels: { color: ChartTheme.textColor, font: { size: 11 } },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
    }
};

window.renderModelCharts = function(metrics) {
    const ctxR2 = document.getElementById('modelR2Chart');
    if (ctxR2 && metrics) {
        new Chart(ctxR2, {
            type: 'bar',
            data: {
                labels: ['Support Vector Machine (SVM)', 'K-Nearest Neighbors (KNN)', 'Linear Baseline'],
                datasets: [
                    {
                        label: 'Water Demand R² (%)',
                        data: [
                            metrics.Water_Demand.SVM.R2_Pct,
                            metrics.Water_Demand.KNN.R2_Pct,
                            metrics.Water_Demand.Linear_Regression.R2_Pct
                        ],
                        backgroundColor: 'rgba(6, 182, 212, 0.8)',
                        borderRadius: 6
                    },
                    {
                        label: 'Energy Demand R² (%)',
                        data: [
                            metrics.Energy_Demand.SVM.R2_Pct,
                            metrics.Energy_Demand.KNN.R2_Pct,
                            metrics.Energy_Demand.Linear_Regression.R2_Pct
                        ],
                        backgroundColor: 'rgba(245, 158, 11, 0.8)',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: ChartTheme.gridColor } },
                    y: { 
                        min: 80,
                        max: 100,
                        grid: { color: ChartTheme.gridColor },
                        title: { display: true, text: 'Variance Explained R² (%)' }
                    }
                }
            }
        });
    }

    const ctxClf = document.getElementById('classifierAccuracyChart');
    if (ctxClf && metrics) {
        new Chart(ctxClf, {
            type: 'bar',
            data: {
                labels: ['Logistic Regression', 'SVM Classifier', 'KNN Classifier'],
                datasets: [
                    {
                        label: 'Accuracy (%)',
                        data: [
                            metrics.Scarcity_Classification.Logistic_Regression.Accuracy_Pct,
                            metrics.Scarcity_Classification.SVM_Classifier.Accuracy_Pct,
                            metrics.Scarcity_Classification.KNN_Classifier.Accuracy_Pct
                        ],
                        backgroundColor: 'rgba(16, 185, 129, 0.85)',
                        borderRadius: 6
                    },
                    {
                        label: '5-Fold CV Accuracy (%)',
                        data: [
                            metrics.Scarcity_Classification.Logistic_Regression.CV_5Fold_Accuracy,
                            metrics.Scarcity_Classification.SVM_Classifier.CV_5Fold_Accuracy,
                            metrics.Scarcity_Classification.KNN_Classifier.CV_5Fold_Accuracy
                        ],
                        backgroundColor: 'rgba(129, 140, 248, 0.85)',
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: ChartTheme.gridColor } },
                    y: { 
                        min: 75,
                        max: 100,
                        grid: { color: ChartTheme.gridColor },
                        title: { display: true, text: 'Percentage Score (%)' }
                    }
                }
            }
        });
    }
};
