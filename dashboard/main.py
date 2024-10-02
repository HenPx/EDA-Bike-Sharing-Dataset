import streamlit as st
import pandas as pd
import plotly.express as px

# Load data untuk kebutuhan visualisasi
day_df = pd.read_csv('dashboard/day_clean.csv')

st.title("Data Analyst | Sharing Bike Dashboard")
st.markdown("""
    by:
    - Name: I Nyoman Adi Mahendra Putra
    - Email: henptra@gmail.com

""", unsafe_allow_html=True)

# Sidebar menu options
option = st.sidebar.selectbox(
    "Silahkah memilih opsi dibawah ini:",
    ['Beranda', 'Tren data (2011-2012)', 'Rental berdasarkan Musim', 'Dampak dari Workingday']
)

# Untuk memunculkan beranda/landing page
if option == 'Beranda':
    st.subheader("Deskripsi")
    st.write("""Dashboard ini akan memvisualisasikan Dataset kedalam beberapa pertanyaan bisnis berikut.\n
    - Bagaimana perkembangan penggunaan rental sepeda dari tahun 2011 ke 2012?\n
    - Seberapa banyak penggunaan rental sepeda berdasarkan musim atau season (spring, summer, fall, winter)?\n
    - Bagaimanakah dampak hari kerja (workingday) dan hari libur(holiday) terhadap pengguna (casual dan registered) saat melakukan rental?
    \n**Silahkan pilih opsi yang ada di sidebar untuk hasil perhitungan.**""")
    st.write("Berikut adalah tampilan dari dataset yang digunakan:")
    st.write(day_df)

# Menu 1: Tren data (2011-2012)
elif option == 'Tren data (2011-2012)':
    st.subheader("Tren Data (2011-2012)")

    # Group data berdasarkan bulan dan tahun
    show_data = day_df.groupby(by=["mnth", "yr"]).agg({"cnt": "sum"}).reset_index()

    # Membuat urutan bulan dengan nama yang benar
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    show_data['mnth'] = pd.Categorical(show_data['mnth'], categories=month_order, ordered=True)

    # Mengurutkan data agar sesuai dengan urutan bulan yang benar
    show_data = show_data.sort_values(by=['yr', 'mnth'])
    show_data

    fig = px.line(
        show_data,
        x='mnth',
        y='cnt',
        color='yr', 
        labels={'cnt': 'Jumlah Pengguna', 'mnth': 'Bulan', 'yr': 'Tahun'},
        title='Trenm Pengguna Rental Sepeda 2011-2012',
        markers=True,
        color_discrete_map={2011: 'red', 2012: 'green'}
    )

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(12)),
            ticktext=month_order  
        ),
        xaxis_title="Bulan",
        yaxis_title="Jumlah Pengguna",
        title_x=0.5 
    )

    st.plotly_chart(fig)
    st.subheader("Hasil analisa:")
    st.write("Dari tahun 2011 ke 2012, terjadi perkembangan penggunaan rental sepeda yang cukup mengalami kenaikan. Terlihat pada visualisasi bahwa setiap bulannya mengalami angka kenaikan pengguna rental sepeda.")

# Menu 2: Rental berdasarkan Musim
elif option == 'Rental berdasarkan Musim':
    st.subheader("Rental berdasarkan Musim")

    # Group data berdasarkan musim
    show_data2 = day_df.groupby('season')['cnt'].sum().reset_index()
    show_data2
    # Tampilkan
    fig = px.bar(show_data2, x='season', y='cnt',
                 labels={'cnt': 'Jumlah Pengguna', 'season': 'Musim'},
                 title='Rental berdasarkan Musim')
    st.plotly_chart(fig)

    # Plot sesuai urutan
    sort_df = show_data2.sort_values(by='cnt', ascending=True)
    fig_sorted = px.bar(sort_df, y='season', x='cnt', orientation='h',
                        labels={'cnt': 'Jumlah Pengguna', 'season': 'Musim'},
                        title='Rental berdasarkan Musim (Sudah Diurutkan)')
    st.plotly_chart(fig_sorted)
    
    st.subheader("Hasil analisa:")
    st.write("Berdasarkan hasil EDA dan visualisasi, pengguna rental sepeda lebih banyak terjadi pada musim Fall (1061129 pengguna), diikuti oleh Summer(918589 pengguna), Winter(841613 pengguna), dan Spring (471348).")

# Menu 3: Dampak dari Workingday
elif option == 'Dampak dari Workingday':
    st.subheader("Dampak dari Workingday")

    # Group data berdasarkan workingday
    show_data3 = day_df.groupby('workingday').agg({'cnt': 'sum'}).reset_index()
    show_data3
    # tampilkan
    fig = px.bar(show_data3, x='workingday', y='cnt',
                 labels={'cnt': 'Total Pengguna', 'workingday': 'Workingday'},
                 title='Total Pengguna berdasarkan Working Day')
    st.plotly_chart(fig)

    # Group data berdasarkan casual dan registered users
    show_data4 = day_df.groupby('workingday').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
    show_data4_melt = show_data4.melt(id_vars='workingday', value_vars=['casual', 'registered'], 
                                      var_name='Tipe Pengguna', value_name='Count')
    show_data4_melt
    # tampilkann
    fig_comparison = px.bar(
        show_data4_melt, 
        x='workingday', 
        y='Count', 
        color='Tipe Pengguna', 
        barmode='group', 
        labels={'Count': 'Total Pengguna', 'workingday': 'Workingday'}, 
        title='Perbandingan Pengguna Casual vs Registered',
        color_discrete_map={'casual': 'blue', 'registered': 'orange'}
    )

    fig_comparison.update_layout(
        yaxis_title='Total Pengguna'
    )
    st.plotly_chart(fig_comparison)
    
    st.subheader("Hasil analisa:")
    st.write("Berdasarkan analisis, penggunaan rental sepeda workingday lebih banyak dua kali lipat dibanding holiday atau hari libur. Sehingga pada workingday pengguna rental sepeda lebih padat. Pengguna Registered lebih banyak melakukan rental daripada casual.")