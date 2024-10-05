import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_number

def calculate_average_rentals(df):
    total_rentals = df['cnt'].sum()  # Total penyewaan
    rental_days = (df['dteday'].max() - df['dteday'].min()).days + 1  # Jumlah hari
    avg_rentals_per_day = total_rentals / rental_days if rental_days > 0 else 0  # Rata-rata penyewaan per hari
    return rental_days, avg_rentals_per_day

def calculate_yearly_rentals(df):
    df['yr'].replace({0: '2011', 1: '2012'}, inplace=True) 
    rental_counts = df.groupby('yr')['cnt'].sum() 
    return rental_counts

def create_user_count(df):
    total_casual = df["casual"].sum()
    total_registered = df["registered"].sum()

    comparison_df = pd.DataFrame({
        'User Type': ['Casual', 'Registered'],
        'Total Users': [total_casual, total_registered]
    })
    return comparison_df

def create_bike_sharing_dashboard(df):
    st.title('Bike Sharing Dashboard :bike:')

    with st.sidebar:
        st.image("bike_sharing_logo.png")

        min_date = df['dteday'].min()
        max_date = df['dteday'].max()
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    df_filtered = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

    total_users, avg_rentals = calculate_average_rentals(df_filtered)

    formatted_total_users = format_number(total_users, locale='id_ID')  
    formatted_avg_rentals = format_number(avg_rentals, locale='id_ID')  

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Penyewa", value=formatted_total_users)

    with col2:
        st.metric("Rata-Rata Penyewaan Sepeda per Hari", value=formatted_avg_rentals)

    rental_counts = calculate_yearly_rentals(df_filtered)
    rental_counts = calculate_yearly_rentals(df_filtered)
    comparison_df = create_user_count(df_filtered)

   # Menampilkan donut chart untuk total penyewaan berdasarkan tahun
    st.subheader("Persentase Penyewaan Sepeda Tahun 2011-2012")
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax.pie(
        rental_counts,
        labels=rental_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85,
        colors=sns.color_palette(['skyblue', 'orange'])
    )
    
    # Membuat lingkaran di tengah untuk efek donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white', ec='white')
    fig.gca().add_artist(centre_circle) 
    ax.axis('equal')  

    st.pyplot(fig)

    # Membuat figure untuk Matplotlib
    plt.figure(figsize=(6, 4))
    colors = ['skyblue', 'orange']

    # Membuat grafik batang untuk perbandingan pengguna
    plt.bar(comparison_df['User Type'], comparison_df['Total Users'], color=colors)

    # Memberi label pada grafik
    plt.title('Perbandingan Total Pengguna Kasual dan Terdaftar', fontsize=16, pad=20)
    plt.xlabel('Tipe Pengguna', fontsize=14)
    plt.ylabel('Total Pengguna', fontsize=14)

    # Menampilkan nilai di atas batang
    for i, v in enumerate(comparison_df['Total Users']):
        plt.text(i, v + 0.01 * max(comparison_df['Total Users']), str(v), ha='center', fontsize=12)

    # Menampilkan grafik di Streamlit
    st.pyplot(plt)
    
    #Menampilkan copyright
    st.caption('Copyright (c) Adri Bangkit 2024')

df_day = pd.read_csv('main_data.csv')

df_day['dteday'] = pd.to_datetime(df_day['dteday'])

create_bike_sharing_dashboard(df_day)