import zipfile
import os
import pandas as pd
import numpy as np
import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Распаковка архива данных
with zipfile.ZipFile("cicids2017.zip", "r") as zip_ref:
    zip_ref.extractall("data_folder")

# Сбор всех CSV файлов в один DataFrame
file_pattern = "data_folder/MachineLearningCSV/MachineLearningCVE/*.csv"
csv_files = glob.glob(file_pattern)
dataframes = []
for f in csv_files:
    df = pd.read_csv(f, encoding='cp1252')  # Указание кодировки из-за возможных проблем с чтением
    dataframes.append(df)
combined_df = pd.concat(dataframes, ignore_index=True)

# Нормализация названий столбцов
combined_df.columns = combined_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# Очистка и масштабирование данных
features = combined_df.drop(columns=["label"])
features.replace([np.inf, -np.inf], np.nan, inplace=True)
features.fillna(features.mean(), inplace=True)
labels = pd.get_dummies(combined_df["label"])  # Использование one-hot encoding для меток

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels, test_size=0.2, random_state=42)

# Изменение формы данных для LSTM
X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# Создание и обучение модели LSTM
model = Sequential([
    LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
    LSTM(32),
    Dense(labels.shape[1], activation='softmax')  # Использование softmax для многоклассовой классификации
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test))

# Оценка модели
loss, accuracy = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

# Предсказание и экспорт данных для анализа
y_pred_prob = model.predict(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)

# Сохранение предсказаний и вероятностей
results_df = pd.DataFrame({
    'Actual': np.argmax(y_test.to_numpy(), axis=1),
    'Predicted': y_pred,
    'Probability': y_pred_prob.max(axis=1)
})
results_df.to_csv('predictions.csv', index=False)

# Визуализация матрицы ошибок
conf_matrix = confusion_matrix(np.argmax(y_test.to_numpy(), axis=1), y_pred)
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()
