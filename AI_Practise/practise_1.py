# predictive_maintenance_rul.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------
# شبیه‌سازی داده‌ها
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
        # زمان باقی‌مانده تا خرابی (RUL) را شبیه‌سازی می‌کنیم
        rul_hours = max(0, 2000 - run_hours + np.random.randint(-50,50))
        data_list.append([machine_id, step, temperature, vibration, pressure, run_hours, rul_hours])

df = pd.DataFrame(data_list, columns=["machine_id", "time_step", "temperature", "vibration", "pressure", "run_hours", "rul_hours"])
print("نمونه داده‌ها:\n", df.head())

# -------------------------
# آموزش مدل رگرسیون
# -------------------------
X = df[["temperature", "vibration", "pressure", "run_hours"]]
y = df["rul_hours"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------
# پیش‌بینی و ارزیابی
# -------------------------
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE = {mse:.2f}, R2 = {r2:.2f}")

# نمودار پیش‌بینی‌ها در مقابل مقدار واقعی
plt.scatter(y_test, y_pred)
plt.xlabel("RUL واقعی")
plt.ylabel("RUL پیش‌بینی شده")
plt.title("پیش‌بینی RUL")
plt.plot([0, 2000],[0,2000], "r--")  # خط مرجع
plt.show()
