# predictive_maintenance_basics.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# -------------------------
# شبیه‌سازی داده‌های حسگر
# -------------------------
np.random.seed(42)
n_machines = 5
n_steps = 50

data_list = []

for machine_id in range(1, n_machines+1):
    for step in range(n_steps):
        temperature = np.random.normal(70, 10)
        vibration = np.random.normal(0.5, 0.1)
        pressure = np.random.normal(30, 5)
        run_hours = np.random.randint(100, 2000)
        # تعریف خرابی بر اساس آستانه
        failure = int(
            (temperature > 65) |
            (vibration > 0.7) |
            (pressure > 40) |
            (run_hours > 1500)
        )
        data_list.append([machine_id, step, temperature, vibration, pressure, run_hours, failure])

df = pd.DataFrame(data_list, columns=["machine_id", "time_step", "temperature", "vibration", "pressure", "run_hours", "failure"])
print("نمونه داده‌ها:\n", df.head())

# -------------------------
# آموزش مدل Random Forest
# -------------------------
X = df[["temperature", "vibration", "pressure", "run_hours"]]
y = df["failure"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -------------------------
# پیش‌بینی و ارزیابی
# -------------------------
y_pred = model.predict(X)
print("\nگزارش طبقه‌بندی:")
print(classification_report(y, y_pred))

print("\nماتریس سردرگمی:")
print(confusion_matrix(y, y_pred))

# -------------------------
# اهمیت ویژگی‌ها
# -------------------------
importances = pd.Series(model.feature_importances_, index=X.columns)
importances.sort_values().plot(kind="barh", title="اهمیت ویژگی‌ها")
plt.show()
