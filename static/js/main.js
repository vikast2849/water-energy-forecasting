// Main interactive utilities
document.addEventListener('DOMContentLoaded', () => {
    // Preset loader for Prediction Studio
    const presets = {
        chitradurga_urban: {
            Region_Name: "Chitradurga Urban Core",
            Region_Type: "Urban",
            Population: 230000,
            Population_Density: 4100,
            Household_Size: 3.9,
            Avg_Temperature_C: 37.5,
            Rainfall_mm: 12.0,
            Industrial_Index: 72.0,
            Agricultural_Index: 8.0,
            Water_Piped_Coverage_Pct: 94.0,
            Electrification_Pct: 99.5,
            Season: "Summer"
        },
        challakere_rural: {
            Region_Name: "Challakere Rural Agrarian",
            Region_Type: "Rural",
            Population: 88000,
            Population_Density: 215,
            Household_Size: 5.4,
            Avg_Temperature_C: 38.0,
            Rainfall_mm: 8.0,
            Industrial_Index: 12.0,
            Agricultural_Index: 92.0,
            Water_Piped_Coverage_Pct: 46.0,
            Electrification_Pct: 86.0,
            Season: "Summer"
        },
        hiriyur_monsoon: {
            Region_Name: "Hiriyur Agro-Cluster",
            Region_Type: "Rural",
            Population: 95000,
            Population_Density: 245,
            Household_Size: 5.2,
            Avg_Temperature_C: 27.0,
            Rainfall_mm: 165.0,
            Industrial_Index: 18.0,
            Agricultural_Index: 95.0,
            Water_Piped_Coverage_Pct: 55.0,
            Electrification_Pct: 89.0,
            Season: "Monsoon"
        },
        bengaluru_metro: {
            Region_Name: "Bengaluru Peri-Urban Hub",
            Region_Type: "Urban",
            Population: 980000,
            Population_Density: 7900,
            Household_Size: 3.6,
            Avg_Temperature_C: 31.0,
            Rainfall_mm: 45.0,
            Industrial_Index: 90.0,
            Agricultural_Index: 5.0,
            Water_Piped_Coverage_Pct: 97.0,
            Electrification_Pct: 100.0,
            Season: "Summer"
        }
    };

    window.applyPreset = function(presetKey) {
        const data = presets[presetKey];
        if (!data) return;
        for (const [key, value] of Object.entries(data)) {
            const el = document.getElementById(key);
            if (el) {
                el.value = value;
                // Dispatch event if slider
                el.dispatchEvent(new Event('input'));
            }
        }
    };

    // Live update for range sliders
    const rangeSliders = document.querySelectorAll('input[type="range"]');
    rangeSliders.forEach(slider => {
        const valSpan = document.getElementById(slider.id + '_val');
        if (valSpan) {
            valSpan.textContent = slider.value;
            slider.addEventListener('input', () => {
                valSpan.textContent = slider.value;
            });
        }
    });

    // Retrain button handler
    const retrainBtn = document.getElementById('retrainModelsBtn');
    if (retrainBtn) {
        retrainBtn.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to retrain all 3 models (SVM, KNN, Logistic Regression) on the current dataset?')) return;
            retrainBtn.disabled = true;
            retrainBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Retraining Models...';
            try {
                const res = await fetch('/api/retrain', { method: 'POST' });
                const json = await res.json();
                if (json.status === 'success') {
                    alert('Models successfully retrained and validated!');
                    window.location.reload();
                } else {
                    alert('Retraining error: ' + json.message);
                }
            } catch (err) {
                alert('Network error while retraining: ' + err.message);
            } finally {
                retrainBtn.disabled = false;
                retrainBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Retrain All Models';
            }
        });
    }

    // CSV Upload handler
    const uploadForm = document.getElementById('uploadDatasetForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('datasetFileInput');
            if (!fileInput || !fileInput.files.length) {
                alert('Please select a valid CSV file first.');
                return;
            }
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            const submitBtn = uploadForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading & Retraining...';

            try {
                const res = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                const json = await res.json();
                if (json.status === 'success') {
                    alert('Dataset uploaded and all 3 models retrained with updated accuracy metrics!');
                    window.location.reload();
                } else {
                    alert('Upload failed: ' + json.message);
                }
            } catch (err) {
                alert('Upload error: ' + err.message);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Upload & Retrain';
            }
        });
    }
});
