import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul aplikasi
st.title("Analisis Data Pengguna Kasual berdasarkan Musim")

# Memuat data
customers_df = pd.read_csv("https://raw.githubusercontent.com/anzhelinkr/final-project-angeline/refs/heads/main/day.csv")

# Menampilkan data dan informasi
st.header("Data Pengguna Kasual")
st.write(customers_df.head())
st.write(customers_df.info())
st.write(customers_df.describe())

# Mengubah kolom tanggal menjadi datetime
datetime_columns = ["dteday"]
for column in datetime_columns:
    customers_df[column] = pd.to_datetime(customers_df[column])

# Mengelompokkan data berdasarkan musim dan menghitung statistik
seasonal_stats = customers_df.groupby(by="season").agg({
    "casual": ["max", "min", "mean", "std"]
}).reset_index()

seasonal_stats.columns = ['season', 'max_casual', 'min_casual', 'mean_casual', 'std_casual']

# Visualisasi statistik pengguna kasual berdasarkan musim
st.header("Statistik Pengguna Kasual berdasarkan Musim")

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(seasonal_stats['season'], seasonal_stats['mean_casual'], 
       yerr=seasonal_stats['std_casual'], capsize=5, color='skyblue', label='Mean Casual')
ax.scatter(seasonal_stats['season'], seasonal_stats['min_casual'], color='red', label='Min Casual', zorder=5)
ax.scatter(seasonal_stats['season'], seasonal_stats['max_casual'], color='green', label='Max Casual', zorder=5)

ax.set_title('Hubungan Antara Musim dan Jumlah Pengguna Kasual')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Pengguna Kasual')
ax.legend()
st.pyplot(fig)

# Mengelompokkan data untuk visualisasi 3D
agg_data = customers_df.groupby(by=["temp", "hum", "windspeed"]).agg({
    "cnt": "mean"
}).reset_index()

# Visualisasi scatter plot 3D
st.header("Visualisasi 3D Jumlah Pengguna Berdasarkan Suhu, Kelembapan, dan Kecepatan Angin")

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(agg_data['temp'], agg_data['hum'], agg_data['windspeed'],
           c=agg_data['cnt'], cmap='viridis', s=50)

ax.set_xlabel('Suhu (temp)')
ax.set_ylabel('Kelembapan (hum)')
ax.set_zlabel('Kecepatan Angin (windspeed)')
ax.set_title('Scatter Plot 3D: Jumlah Pengguna Berdasarkan Suhu, Kelembapan, dan Kecepatan Angin')

cbar = plt.colorbar(ax.collections[0], ax=ax, pad=0.1)
cbar.set_label('Rata-rata Jumlah Pengguna (cnt)')

st.pyplot(fig)