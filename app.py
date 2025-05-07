import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from datetime import date

# === DATABASE CONNECTION ===
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
    data = cur.fetchall() if fetch else None
    conn.commit()
    cur.close()
    conn.close()
    return data

# === CUSTOM STYLE ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}
.stButton>button {
    background: linear-gradient(135deg, #1a3b7c, #3a6ea5);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
}
.stButton>button:hover {
    background: #355c9c;
}
</style>
""", unsafe_allow_html=True)

# === HOME PAGE ===
def home():
    st.markdown("<h2 style='text-align:center;'>🎓 Sistem Pembayaran Kuliah</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>STT Wastukancana</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.success("Selamat datang di Sistem Pembayaran Kuliah STT Wastukancana!")
        st.write("""
            Sistem ini dirancang untuk memudahkan pengelolaan pembayaran kuliah mahasiswa.
            Anda dapat menginput biaya kuliah, mencatat angsuran, dan melihat laporan pembayaran.
        """)

    with col2:
        fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'pie'}]])
        fig.add_trace(go.Pie(
            labels=["Lunas", "Angsuran", "Tunggakan"],
            values=[70, 20, 10],
            hole=0.4,
            marker=dict(colors=["#28a745", "#ffc107", "#dc3545"]),
            textinfo="percent"
        ))
        fig.update_layout(title="Distribusi Pembayaran")
        st.plotly_chart(fig, use_container_width=True)

# === INPUT BIAYA KULIAH ===
def input_biaya_kuliah():
    st.header("📥 Input Biaya Kuliah")
    with st.form("form_biaya"):
        col1, col2 = st.columns(2)
        with col1:
            program_studi = st.selectbox("Program Studi", [
                "Teknik Informatika", "Teknik Mesin", "Teknik Industri", "Teknik Tekstil", "Teknik BOM"])
            nim = st.text_input("NIM")
            nama = st.text_input("Nama")
            sks_kuliah = st.number_input("Jumlah SKS", min_value=0)
        with col2:
            tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
            semester = st.selectbox("Semester", ["Ganjil", "Genap"])
            biaya = st.number_input("Biaya Kuliah", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Simpan")
        tombol_cari = st.form_submit_button("Cari")
        tombol_hapus = st.form_submit_button("Hapus")
        tombol_cek_biaya = st.form_submit_button("Cek Biaya")

        if submit:
            run_query('''INSERT INTO biaya_kuliah 
                         (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya_total) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                      (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya))
            st.success("Biaya kuliah berhasil disimpan.")

        if tombol_cari:
            results = run_query('SELECT * FROM biaya_kuliah WHERE nim = %s', (nim,), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Data tidak ditemukan.")

        if tombol_hapus:
            run_query('DELETE FROM biaya_kuliah WHERE nim = %s', (nim,))
            st.success("Data berhasil dihapus.")

        if tombol_cek_biaya:
            result = run_query('SELECT biaya_total FROM biaya_kuliah WHERE nim = %s', (nim,), fetch=True)
            if result:
                st.success(f"Total Biaya Kuliah: Rp {result[0][0]:,.2f}")
            else:
                st.warning("Data tidak ditemukan.")

# === BAYAR ANGSURAN ===
def bayar_angsuran():
    st.header("💳 Bayar Angsuran Biaya Kuliah")
    with st.form("form_angsuran"):
        col1, col2 = st.columns(2)
        with col1:
            program_studi = st.selectbox("Program Studi", [
                "Teknik Informatika", "Teknik Mesin", "Teknik Industri", "Teknik Tekstil", "Teknik BOM"])
            nim = st.text_input("NIM")
            nama = st.text_input("Nama")
            angsuran_ke = st.number_input("Angsuran Ke-", min_value=1)
        with col2:
            tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
            semester = st.selectbox("Semester", ["Ganjil", "Genap"])
            tanggal = st.date_input("Tanggal", value=date.today())
            bayar = st.number_input("Jumlah Bayar", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Simpan")
        tombol_cari = st.form_submit_button("Cari")
        tombol_hapus = st.form_submit_button("Hapus")

        if submit:
            run_query('''INSERT INTO angsuran_kuliah 
                         (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal_pembayaran, jumlah_bayar)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                      (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal, bayar))
            st.success("Pembayaran angsuran berhasil disimpan.")

        if tombol_cari:
            results = run_query('''SELECT * FROM angsuran_kuliah WHERE nim = %s AND angsuran_ke = %s''',
                                (nim, angsuran_ke), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Data tidak ditemukan.")

        if tombol_hapus:
            run_query('''DELETE FROM angsuran_kuliah WHERE nim = %s AND angsuran_ke = %s''',
                      (nim, angsuran_ke))
            st.success("Data angsuran berhasil dihapus.")

# === CARI ANGSURAN ===
def cari_angsuran():
    st.header("🔍 Pencarian Angsuran")
    program_studi = st.selectbox("Program Studi", [
        "Teknik Informatika", "Teknik Mesin", "Teknik Industri", "Teknik Tekstil", "Teknik BOM"])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    tanggal = st.date_input("Tanggal")

    if st.button("Cari"):
        results = run_query('''
            SELECT nim, nama, angsuran_ke, tanggal_pembayaran, jumlah_bayar
            FROM angsuran_kuliah
            WHERE program_studi = %s AND tahun = %s AND semester = %s AND tanggal_pembayaran = %s
        ''', (program_studi, tahun, semester, tanggal), fetch=True)
        st.dataframe(results)

# === LAPORAN LUNAS ===
def laporan_lunas():
    st.header("📄 Laporan Sudah Lunas")
    program_studi = st.selectbox("Program Studi", [
        "Teknik Informatika", "Teknik Mesin", "Teknik Industri", "Teknik Tekstil", "Teknik BOM"])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    if st.button("Cari Lunas"):
        query = '''
            SELECT nim, nama, SUM(jumlah_bayar) AS total_bayar
            FROM angsuran_kuliah
            WHERE program_studi = %s AND tahun = %s AND semester = %s
            GROUP BY nim, nama
            HAVING SUM(jumlah_bayar) >= (
                SELECT biaya_total FROM biaya_kuliah WHERE nim = angsuran_kuliah.nim
            )
        '''
        results = run_query(query, (program_studi, tahun, semester), fetch=True)
        st.dataframe(results)

# === LAPORAN BELUM LUNAS ===
def laporan_belum_lunas():
    st.header("📄 Laporan Belum Lunas")
    program_studi = st.selectbox("Program Studi", [
        "Teknik Informatika", "Teknik Mesin", "Teknik Industri", "Teknik Tekstil", "Teknik BOM"])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    if st.button("Cari Belum Lunas"):
        query = '''
            SELECT nim, nama, SUM(jumlah_bayar) AS total_bayar
            FROM angsuran_kuliah
            WHERE program_studi = %s AND tahun = %s AND semester = %s
            GROUP BY nim, nama
            HAVING SUM(jumlah_bayar) < (
                SELECT biaya_total FROM biaya_kuliah WHERE nim = angsuran_kuliah.nim
            )
        '''
        results = run_query(query, (program_studi, tahun, semester), fetch=True)
        st.dataframe(results)

# === MAIN APP ===
def main():
    st.sidebar.title("📌 Menu Navigasi")
    menu_options = [
        "Beranda", "Input Biaya Kuliah", "Bayar Angsuran",
        "Pencarian Angsuran", "Laporan Sudah Lunas", "Laporan Belum Lunas"
    ]
    selected_menu = st.sidebar.radio("Pilih Menu", menu_options)

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
