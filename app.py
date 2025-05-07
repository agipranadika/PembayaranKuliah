    import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from datetime import date
import io
from PIL import Image
import base64

# Koneksi ke database PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="gondola.proxy.rlwy.net",
        port=57367,
        dbname="railway",
        user="postgres",
        password="tAwxGzaYZTkTejKfaZCsZoMHrnSOCNVk"
    )

def run_query(query, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    data = None
    if fetch:
        data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data


# Incorporate it in your main home function
def home():
    # ===== STYLE CUSTOMIZATION =====
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main-title {
            color: #2b5876;
            font-size: 2.8rem !important;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .sub-title {
            color: #4e4376;
            font-size: 1.2rem !important;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .welcome-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }
        
        .action-btn {
            background: linear-gradient(135deg, #1a3b7c 0%, #3a6ea5 100%) !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.75rem 2rem !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            color: white !important;
        }
        
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(26, 59, 124, 0.4) !important;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1a3b7c 0%, #3a6ea5 100%);
            color: white;
        }
        
        .sidebar .sidebar-content .stRadio > div {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER SECTION =====
    st.markdown('<p class="main-title">🎓 Sistem Pembayaran Kuliah</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">STT Wastukancana</p>', unsafe_allow_html=True)
    
    # ===== HERO SECTION =====
    with st.container():
        col1, col2 = st.columns([1, 1.3])
        
        with col1:
            st.markdown("""
            <div class="welcome-card">
                <h2 style="color: #2b5876;">Selamat Datang!</h2>
                <p style="font-size: 1.1rem;">
                    Sistem terpadu untuk mengelola pembayaran kuliah mahasiswa 
                    STT Wastukancana dengan mudah dan efisien.
                </p>
                <div style="text-align: center; margin-top: 2rem;">
                    <button class="action-btn">Masuk ke Dashboard</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Pie chart to display payment categories distribution
            st.markdown("### 📊 Statistik Pembayaran")

            perc_lunas = 70  # Example percentage for "Lunas"
            perc_angsuran = 20  # Example percentage for "Angsuran"
            perc_tunggakan = 10  # Example percentage for "Tunggakan"

            fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'pie'}]])

            fig.add_trace(
                go.Pie(
                    labels=["Lunas","Angsuran","Tunggakan"],
                    values=[perc_lunas, perc_angsuran, perc_tunggakan],
                    hole=0.4,
                    textinfo="percent",
                    marker=dict(colors=["#28a745", "#ffc107", "#dc3545"]),
                )
            )

            fig.update_layout(
                title="Distribusi Pembayaran",
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

    # ===== FOOTER =====
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin: 2rem 0;">
        <p>© 2025 Bagian Keuangan STT Wastukancana</p>
        <p style="font-size: 0.8rem;">Versi 2.1.0 | Terakhir diperbarui: 30 April 2025</p>
    </div>
    """, unsafe_allow_html=True)

# Main App
def main():
    # Sidebar navigation
    st.sidebar.title("Menu Navigasi")
    
    # Using radio buttons for navigation
    menu_options = [
        "Beranda",
        "Input Biaya Kuliah", 
        "Bayar Angsuran", 
        "Pencarian Angsuran", 
        "Laporan Sudah Lunas", 
        "Laporan Belum Lunas"
    ]
    
    selected_menu = st.sidebar.radio("Pilih Menu", menu_options)

# Halaman: Input Biaya Kuliah
def input_biaya_kuliah():
    st.header("Input Biaya Kuliah")
    with st.form("form_biaya"):
        program_studi = st.selectbox("Program Studi", [
            "Teknik Informatika", 
            "Teknik Mesin", 
            "Teknik Industri", 
            "Teknik Tekstil", 
            "Teknik BOM"
        ])
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        sks_kuliah = st.number_input("SKS Kuliah", min_value=0)
        tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        biaya = st.number_input("Biaya Kuliah", min_value=0.0, format="%.2f")
        
        submit = st.form_submit_button("Simpan")
        tombol_cari = st.form_submit_button("Cari")
        tombol_hapus = st.form_submit_button("Hapus")
        tombol_cek_biaya = st.form_submit_button("Cek Biaya")
        
        if submit:
            query = '''INSERT INTO biaya_kuliah
                       (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya_total)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            run_query(query, (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya))
            st.success("Biaya kuliah berhasil disimpan.")
        
        if tombol_cari:
            query = '''SELECT * FROM biaya_kuliah WHERE nim = %s'''
            results = run_query(query, (nim,), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Data tidak ditemukan.")
        
        if tombol_hapus:
            query = '''DELETE FROM biaya_kuliah WHERE nim = %s'''
            run_query(query, (nim,))
            st.success("Data biaya kuliah berhasil dihapus.")
        
        if tombol_cek_biaya:
            query = '''SELECT biaya_total FROM biaya_kuliah WHERE nim = %s'''
            result = run_query(query, (nim,), fetch=True)
            if result:
                st.write(f"Total Biaya Kuliah: Rp {result[0][0]:,.2f}")
            else:
                st.warning("Data biaya kuliah tidak ditemukan.")

# Halaman: Bayar Angsuran Biaya Kuliah
def bayar_angsuran():
    st.header("Bayar Angsuran Biaya Kuliah")
    with st.form("form_angsuran"):
        program_studi = st.selectbox("Program Studi", [
            "Teknik Informatika", 
            "Teknik Mesin", 
            "Teknik Industri", 
            "Teknik Tekstil", 
            "Teknik BOM"
        ])
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        angsuran_ke = st.number_input("Angsuran Ke-", min_value=1)
        tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        tanggal = st.date_input("Tanggal", value=date.today())
        bayar = st.number_input("Jumlah Bayar", min_value=0.0, format="%.2f")
        
        submit = st.form_submit_button("Simpan")
        tombol_cari = st.form_submit_button("Cari")
        tombol_hapus = st.form_submit_button("Hapus")
        
        if submit:
            query = '''INSERT INTO angsuran_kuliah
                       (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal_pembayaran, jumlah_bayar)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            run_query(query, (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal, bayar))
            st.success("Pembayaran angsuran berhasil disimpan.")
        
        if tombol_cari:
            query = '''SELECT * FROM angsuran_kuliah WHERE nim = %s AND angsuran_ke = %s'''
            results = run_query(query, (nim, angsuran_ke), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Data angsuran tidak ditemukan.")
        
        if tombol_hapus:
            query = '''DELETE FROM angsuran_kuliah WHERE nim = %s AND angsuran_ke = %s'''
            run_query(query, (nim, angsuran_ke))
            st.success("Data angsuran berhasil dihapus.")

# Halaman: Pencarian Angsuran
def cari_angsuran():
    st.header("Pencarian Angsuran Biaya Kuliah")
    program_studi = st.selectbox("Program Studi", [
        "Teknik Informatika", 
        "Teknik Mesin", 
        "Teknik Industri", 
        "Teknik Tekstil", 
        "Teknik BOM"
    ])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    tanggal = st.date_input("Tanggal")

    if st.button("Cari"):
        query = '''
        SELECT nim, nama, angsuran_ke, tanggal_pembayaran, jumlah_bayar
        FROM angsuran_kuliah
        WHERE program_studi = %s AND tahun = %s AND semester = %s AND tanggal_pembayaran = %s
        '''
        results = run_query(query, (program_studi, tahun, semester, tanggal), fetch=True)
        st.dataframe(results, use_container_width=True)

def laporan_lunas():
    st.header("Laporan Angsuran Lunas")
    
    program_studi = st.selectbox("Program Studi", [
        "Teknik Informatika", 
        "Teknik Mesin", 
        "Teknik Industri", 
        "Teknik Tekstil", 
        "Teknik BOM"
    ])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    
    if st.button("Cari Lunas"):
        query = '''
            SELECT nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            FROM angsuran_kuliah
            WHERE program_studi = %s AND tahun = %s AND semester = %s
            GROUP BY nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            HAVING SUM(jumlah_bayar) >= (SELECT biaya_total FROM biaya_kuliah WHERE nim = angsuran_kuliah.nim)
        '''
        
        try:
            results = run_query(query, (program_studi, tahun, semester), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Tidak ada data angsuran yang lunas untuk kriteria tersebut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengambil data: {str(e)}")

def laporan_belum_lunas():
    st.header("Laporan Angsuran Belum Lunas")
    
    program_studi = st.selectbox("Program Studi", [
        "Teknik Informatika", 
        "Teknik Mesin", 
        "Teknik Industri", 
        "Teknik Tekstil", 
        "Teknik BOM"
    ])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    
    if st.button("Cari Belum Lunas"):
        query = '''
            SELECT nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            FROM angsuran_kuliah
            WHERE program_studi = %s AND tahun = %s AND semester = %s
            GROUP BY nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            HAVING SUM(jumlah_bayar) < (SELECT biaya_total FROM biaya_kuliah WHERE nim = angsuran_kuliah.nim)
        '''
        
        try:
            results = run_query(query, (program_studi, tahun, semester), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Tidak ada data angsuran yang belum lunas untuk kriteria tersebut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengambil data: {str(e)}")

# Main App
def main():
    # Sidebar navigation
    st.sidebar.title("Menu Navigasi")
    
    # Using radio buttons for navigation
    menu_options = [
        "Beranda",
        "Input Biaya Kuliah", 
        "Bayar Angsuran", 
        "Pencarian Angsuran", 
        "Laporan Sudah Lunas", 
        "Laporan Belum Lunas"
    ]
    
    selected_menu = st.sidebar.radio("Pilih Menu", menu_options)
    
    # Display the selected page
    if selected_menu == "Beranda":
        home()
    elif selected_menu == "Input Biaya Kuliah":
        input_biaya_kuliah()
    elif selected_menu == "Bayar Angsuran":
        bayar_angsuran()
    elif selected_menu == "Pencarian Angsuran":
        cari_angsuran()
    elif selected_menu == "Laporan Sudah Lunas":
        laporan_lunas()
    elif selected_menu == "Laporan Belum Lunas":
        laporan_belum_lunas()

if __name__ == "__main__":
    main()