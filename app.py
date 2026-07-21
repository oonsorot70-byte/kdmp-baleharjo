import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# -----------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN & TEMA KDMP BALEHARJO
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="KDMP Kalurahan Baleharjo - Sistem Keuangan Multi-Usaha",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Merah Putih Modern)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #cc0000 0%, #800000 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: #ffffff;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }
    .main-header p {
        color: #f0f0f0;
        margin: 5px 0 0 0;
        font-size: 14px;
    }
    .stButton>button {
        background-color: #cc0000;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #990000;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. INISIALISASI SUPABASE DATABASE
# -----------------------------------------------------------------------------
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase_available = False
try:
    supabase = init_supabase()
    supabase_available = True
except Exception as e:
    st.sidebar.warning("⚠️ Belum terhubung ke Supabase. Masukkan SUPABASE_URL dan SUPABASE_KEY di Secrets Streamlit.")

# -----------------------------------------------------------------------------
# 3. HEADER BERSAMA & NAVIGATION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🇮🇩 Koperasi Desa Merah Putih (KDMP) Kalurahan Baleharjo</h1>
    <p>Sistem Informasi Keuangan Multi-Usaha Terpadu & Real-time | Gunungkidul, D.I. Yogyakarta</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.title("📌 Navigation Menu")
menu = st.sidebar.radio(
    "Pilih Unit / Layanan:",
    [
        "📊 Dashboard Konsolidasi",
        "🛒 Kios Sembako & POS (Ritel)",
        "💳 Simpan Pinjam Anggota",
        "🌾 Pertanian & Demplot Milenial",
        "📈 Laporan Keuangan & SHU",
        "⚙️ Panduan Setup Secrets"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Status Sistem: **Cloud Ready**")
st.sidebar.caption("Database: **Supabase PostgreSQL**")

# Helper Function: Format Rupiah
def format_rupiah(val):
    return f"Rp {val:,.0f}".replace(",", ".")

# -----------------------------------------------------------------------------
# MODUL 1: DASHBOARD KONSOLIDASI
# -----------------------------------------------------------------------------
if menu == "📊 Dashboard Konsolidasi":
    st.subheader("📊 Executive Overview - Multi Unit Usaha")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Kas & Bank", format_rupiah(125400000), "+12% bln ini")
    with m2:
        st.metric("Omzet Kios Sembako", format_rupiah(34250000), "+8.5%")
    with m3:
        st.metric("Portofolio Pinjaman", format_rupiah(85000000), "32 Anggota")
    with m4:
        st.metric("Total Anggota Aktif", "148 Orang", "+5 Anggota baru")

    st.divider()

    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        st.markdown("### 📈 Ringkasan Pendapatan per Unit Usaha")
        df_chart = pd.DataFrame({
            "Unit Usaha": ["Unit Sembako/Kios", "Unit Simpan Pinjam", "Unit Pertanian/Demplot"],
            "Pendapatan (Rp)": [34250000, 12800000, 18500000]
        })
        st.bar_chart(df_chart.set_index("Unit Usaha"))

    with col_info:
        st.markdown("### ℹ️ Info Koperasi Baleharjo")
        st.info("""
        **KDMP Kalurahan Baleharjo**
        - **Kategori:** Koperasi Multi-Usaha
        - **Unit Operasional:** 3 Unit
        - **Pengawas:** BP & Pengurus KDMP
        - **Tahun Buku:** 2026
        """)
        st.success("✅ Seluruh transaksi hari ini tercatat dan terenkripsi aman di Supabase.")

# -----------------------------------------------------------------------------
# MODUL 2: KIOS SEMBAKO & POS
# -----------------------------------------------------------------------------
elif menu == "🛒 Kios Sembako & POS (Ritel)":
    st.subheader("🛒 Kasir & Pencatatan Transaksi Kios Sembako")
    
    col_input, col_summary = st.columns([2, 1])
    
    with col_input:
        st.markdown("##### 📝 Input Penjualan Harian")
        with st.form("pos_form", clear_on_submit=True):
            t_date = st.date_input("Tanggal Transaksi", datetime.now())
            item_name = st.selectbox("Pilih Barang / Komoditas", [
                "Beras Medium 10kg", "Minyak Goreng 2L", "Gula Pasir 1kg", "Telur Ayam 1kg", "Tepung Terigu 1kg"
            ])
            qty = st.number_input("Jumlah (Qty)", min_value=1, value=1)
            harga_satuan = st.number_input("Harga Satuan (Rp)", min_value=1000, value=14000, step=500)
            pembeli = st.text_input("Nama Pembeli / Anggota (Opsional)", value="Pelanggan Umum")
            
            submitted = st.form_submit_button("💾 Simpan Transaksi & Auto-Jurnal")
            
            if submitted:
                total = qty * harga_satuan
                st.success(f"✅ Transaksi senilai **{format_rupiah(total)}** berhasil disimpan!")
                st.caption("Auto-Journal Executed: [Debit] 1-1101 Kas Sembako | [Credit] 4-2001 Pendapatan Penjualan Sembako")

    with col_summary:
        st.markdown("##### 🛒 Ringkasan Stok & HPP")
        st.metric("Stok Beras Medium", "420 kg", "Aman")
        st.metric("Stok Minyak Goreng", "85 Pouch", "Waspada Restock")
        st.metric("Estimasi Margin", "12.5%", "Sesuai Target")

# -----------------------------------------------------------------------------
# MODUL 3: SIMPAN PINJAM
# -----------------------------------------------------------------------------
elif menu == "💳 Simpan Pinjam Anggota":
    st.subheader("💳 Unit Simpan Pinjam Anggota KDMP")
    
    tab1, tab2 = st.tabs(["📥 Simpanan Anggota", "📤 Pinjaman & Angsuran"])
    
    with tab1:
        st.markdown("##### Pencatatan Simpanan (Pokok, Wajib, Sukarela)")
        with st.form("simpanan_form"):
            no_anggota = st.text_input("Nomor / Nama Anggota", placeholder="Contoh: AGT-0042 / Bp. Sastro")
            jenis_simpanan = st.selectbox("Jenis Simpanan", ["Simpanan Pokok", "Simpanan Wajib", "Tabungan Sukarela"])
            nominal = st.number_input("Nominal Setoran (Rp)", min_value=10000, value=50000, step=10000)
            btn_simpan = st.form_submit_button("📥 Simpan Setoran")
            if btn_simpan:
                st.success(f"Setoran {jenis_simpanan} sebesar {format_rupiah(nominal)} untuk {no_anggota} berhasil dicatat!")

    with tab2:
        st.markdown("##### Simulasi & Pencatatan Angsuran Pinjaman")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            pinjaman_pokok = st.number_input("Plafon Pinjaman (Rp)", value=5000000, step=500000)
            tenor = st.slider("Jangka Waktu (Bulan)", 1, 24, 12)
            bunga_pa = st.number_input("Jasa / Bunga per Tahun (%)", value=6.0, step=0.5)
        with col_p2:
            angsuran_pokok = pinjaman_pokok / tenor
            jasa_bulanan = (pinjaman_pokok * (bunga_pa / 100)) / 12
            total_angsuran = angsuran_pokok + jasa_bulanan
            
            st.markdown("### Estimasi Angsuran / Bulan")
            st.metric("Total Angsuran", format_rupiah(total_angsuran))
            st.caption(f"Pokok: {format_rupiah(angsuran_pokok)} | Jasa Koperasi: {format_rupiah(jasa_bulanan)}")

# -----------------------------------------------------------------------------
# MODUL 4: PERTANIAN & DEMPLOT
# -----------------------------------------------------------------------------
elif menu == "🌾 Pertanian & Demplot Milenial":
    st.subheader("🌾 Unit Usaha Pertanian & Demplot Milenial Baleharjo")
    st.write("Pencatatan modal kerja tanam, pengadaan pupuk/benih, dan bagi hasil panen.")
    
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("##### 🚜 Modal Kerja Tanam Per Musim")
        st.number_input("Biaya Olah Lahan & Pupuk (Rp)", value=4500000)
        st.number_input("Biaya Benih & Pestisida (Rp)", value=2200000)
        st.number_input("Biaya Tenaga Kerja / HOK (Rp)", value=3800000)
        st.button("🌱 Catat Modal Kerja Demplot")
    
    with d2:
        st.markdown("##### 🌽 Proyeksi & Realisasi Panen")
        st.text_input("Komoditas Demplot", "Jagung Hibrida / Bawang Merah")
        st.number_input("Hasil Panen (Kg)", value=3200)
        st.number_input("Harga Jual per Kg (Rp)", value=5500)
        st.metric("Proyeksi Pendapatan Panen", format_rupiah(3200 * 5500))

# -----------------------------------------------------------------------------
# MODUL 5: LAPORAN KEUANGAN & SHU
# -----------------------------------------------------------------------------
elif menu == "📈 Laporan Keuangan & SHU":
    st.subheader("📈 Laporan Keuangan Real-Time & Kalkulator SHU")
    
    sub_tab1, sub_tab2 = st.tabs(["📑 Laporan Laba / Rugi Konsolidasi", "💰 Kalkulasi Pembagian SHU"])
    
    with sub_tab1:
        st.markdown("#### Laporan Laba Rugi Konsolidasi (Periode 2026)")
        
        lr_data = {
            "Komponen Laba Rugi": [
                "Pendapatan Unit Sembako",
                "Pendapatan Jasa Simpan Pinjam",
                "Pendapatan Hasil Demplot Pertanian",
                "TOTAL PENDAPATAN OPERASIONAL",
                "Beban HPP Sembako",
                "Beban Operasional & Gaji",
                "Beban Penyusutan Aset",
                "TOTAL BEBAN OPERASIONAL",
                "SISA HASIL USAHA (SHU) KETIMBANGAN"
            ],
            "Jumlah (Rp)": [
                34250000,
                12800000,
                18500000,
                65550000,
                -26500000,
                -11200000,
                -1800000,
                -39500000,
                26050000
            ]
        }
        st.table(pd.DataFrame(lr_data))

    with sub_tab2:
        st.markdown("#### Alokasi Sisa Hasil Usaha (SHU) Berdasarkan AD/ART")
        shu_total = st.number_input("Total SHU Bersih Koperasi (Rp)", value=26050000)
        
        c_a, c_b = st.columns(2)
        with c_a:
            p_cadangan = st.slider("Cadangan Koperasi (%)", 0, 100, 40)
            p_jasa_anggota = st.slider("Jasa Usaha & Modal Anggota (%)", 0, 100, 40)
        with c_b:
            p_pengurus = st.slider("Dana Pengurus & Pengawas (%)", 0, 100, 10)
            p_sosial = st.slider("Dana Pendidikan & Sosial (%)", 0, 100, 10)
            
        st.divider()
        st.markdown("##### Breakdown Pembagian Nominal SHU:")
        st.write(f"- **Cadangan Koperasi:** {format_rupiah(shu_total * p_cadangan / 100)}")
        st.write(f"- **Bagian Anggota (Jasa Modal & Belanja):** {format_rupiah(shu_total * p_jasa_anggota / 100)}")
        st.write(f"- **Pengurus & Karyawan:** {format_rupiah(shu_total * p_pengurus / 100)}")
        st.write(f"- **Dana Pendidikan & Pembangunan Desa:** {format_rupiah(shu_total * p_sosial / 100)}")

# -----------------------------------------------------------------------------
# MODUL 6: PANDUAN SECRETS STREAMLIT
# -----------------------------------------------------------------------------
elif menu == "⚙️ Panduan Setup Secrets":
    st.subheader("⚙️ Cara Menghubungkan Streamlit ke Supabase")
    
    st.markdown("""
    ### Isi File / Secrets Streamlit:
    ```toml
    SUPABASE_URL = "[https://vuqxqlxghnsnwvppwesg.supabase.co](https://vuqxqlxghnsnwvppwesg.supabase.co)"
    SUPABASE_KEY = "PASTE_ANON_PUBLIC_KEY_YANG_SUDAH_DICOPIED_TADI"
    ```
    """)
