import pandas as pd
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv("web_traffic.csv")
data['Date'] = pd.to_datetime(data['Date'])
data['Day'] = data['Date'].dt.day
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year
le = LabelEncoder()
data['Source'] = le.fit_transform(data['Source'])

