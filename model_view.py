import pickle
import matplotlib.pyplot as plt

with open("forecast.pkl", "rb") as f:
    forecast = pickle.load(f)

with open("model.pkl", "rb") as f:
    m = pickle.load(f)

print(forecast)