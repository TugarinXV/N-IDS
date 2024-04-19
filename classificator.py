import pandas as pd

def evaluate(value):
    classification = {
        0: "BENIGN(Normal Human Activities)",
        1: "Bot",
        2: "DDoS",
        3: "DoS GoldenEye",
        4: "DoS Hulk",
        5: "DoS Slowhttptest",
        6: "DoS Slowloris",
        7: "FTP-Potator",
        8: "Heartbleed",
        9: "Infiltration",
        10: "PortScan",
        11: "SSH-Potator",
        12: "Web Attack - Brute Force",
        13: "Web Attack - SQL Injection",
    }
    return classification.get(value, "Неизвестное значение")

df = pd.read_csv('predictions.csv')

processed_data = []


for row in df.iterrows():

    first_value = evaluate(row.iloc[0])
    second_value = evaluate(row.iloc[1]) 
    value = row.iloc[2]
    third_value = f"{row.iloc[2]:.2f}"
    # Добавление обработанных значений в список
    processed_data.append([first_value, second_value, third_value])

# Преобразование списка обратно в DataFrame для удобства работы
processed_df = pd.DataFrame(processed_data, columns=['Actual', 'Predicted', "Probability"])

# Показать обработанный DataFrame
print(processed_df)