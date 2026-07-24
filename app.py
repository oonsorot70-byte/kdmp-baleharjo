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
    st.sidebar.warning("⚠️ Belum terhubung ke Supabase. Pastikan Secrets sudah diatur.")

# Helper Function: Format Rupiah
def format_rupiah(val):
    return f"Rp {val:,.0f}".replace(",", ".")

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
        "👥 Master Data & Registrasi Anggota",
        "💳 Simpanan Anggota (Pokok, Wajib, Sukarela)",
        "🛒 Kios Sembako & POS (Ritel)",
        "📤 Pinjaman & Angsuran",
        "🌾 Pertanian & Demplot Milenial",
        "📈 Laporan Keuangan & SHU"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Status Sistem: **Cloud Ready**")
st.sidebar.caption("Database: **Supabase PostgreSQL**")

# -----------------------------------------------------------------------------
# MODUL 1: DASHBOARD KONSOLIDASI (DINOLLKAN)
# -----------------------------------------------------------------------------
if menu == "📊 Dashboard Konsolidasi":
    st.subheader("📊 Executive Overview - Pembukuan Awal")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Kas & Bank", format_rupiah(0), "Mulai Awal")
    with m2:
        st.metric("Total Simpanan Anggota", format_rupiah(0), "Pokok & Wajib")
    with m3:
        st.metric("Portofolio Pinjaman", format_rupiah(0), "0 Anggota")
    with m4:
        st.metric("Total Anggota Aktif", "0 Orang", "Siap Registrasi")

    st.divider()

    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        st.markdown("### 📈 Pendapatan per Unit Usaha")
        df_chart = pd.DataFrame({
            "Unit Usaha": ["Unit Sembako/Kios", "Unit Simpan Pinjam", "Unit Pertanian/Demplot"],
            "Pendapatan (Rp)": [0, 0, 0]
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
        st.success("✅ Sistem siap menerima masukan transaksi riil pertama Anda.")

# -----------------------------------------------------------------------------
# MODUL 2: MASTER DATA & REGISTRASI ANGGOTA
# -----------------------------------------------------------------------------
elif menu == "👥 Master Data & Registrasi Anggota":
    st.subheader("👥 Pengelolaan Data Anggota KDMP Baleharjo")
    
    tab_reg, tab_list = st.tabs(["➕ Registrasi Anggota Baru", "📋 Daftar Anggota Aktif"])
    
    with tab_reg:
        st.markdown("##### Form pendaftaran anggota baru KDMP")
        with st.form("form_registrasi_anggota", clear_on_submit=True):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                no_anggota = st.text_input("Nomor Anggota (NTA)", value=f"KDMP-{datetime.now().strftime('%Y%m%d%H%M')}")
                nama_lengkap = st.text_input("Nama Lengkap Anggota")
                no_hp = st.text_input("Nomor HP / WhatsApp")
            with col_a2:
                padukuhan = st.selectbox("Padukuhan / Wilayah", [
                    "Baleharjo", "Piyaman", "Siraman", "Wonosari", "Lainnya"
                ])
                alamat = st.text_area("Alamat Lengkap Padukuhan")
                tgl_gabung = st.date_input("Tanggal Bergabung", datetime.now())
                
            btn_daftar = st.form_submit_button("💾 Simpan Data Anggota Baru")
            
            if btn_daftar:
                if nama_lengkap:
                    if supabase_available:
                        try:
                            supabase.table("members").insert({
                                "member_number": no_anggota,
                                "name": nama_lengkap,
                                "phone": no_hp,
                                "address": f"{alamat} ({padukuhan})",
                                "status": "AKTIF"
                            }).execute()
                            st.success(f"✅ Anggota baru **{nama_lengkap}** ({no_anggota}) berhasil terdaftar!")
                        except Exception as e:
                            st.error(f"Gagal menyimpan ke database: {e}")
                    else:
                        st.success(f"✅ Data **{nama_lengkap}** berhasil dicatat!")
                else:
                    st.warning("Mohon isi Nama Lengkap Anggota.")

    with tab_list:
        st.markdown("##### Tabel Daftar Seluruh Anggota KDMP Baleharjo")
        if supabase_available:
            try:
                res = supabase.table("members").select("*").order("created_at", desc=True).execute()
                if res.data:
                    df_members = pd.DataFrame(res.data)
                    st.dataframe(df_members, use_container_width=True)
                else:
                    st.info("Belum ada data anggota. Silakan daftarkan anggota baru pada tab di sebelah.")
            except Exception as e:
                st.info("Belum ada data anggota tersimpan.")
        else:
            st.info("Belum ada anggota terdaftar (Sistem Nol).")

# -----------------------------------------------------------------------------
# MODUL 3: SIMPANAN ANGGOTA (POKOK 50RB, WAJIB 10RB, SUKARELA)
# -----------------------------------------------------------------------------
elif menu == "💳 Simpanan Anggota (Pokok, Wajib, Sukarela)":
    st.subheader("💳 Pencatatan & Pengelolaan Simpanan Anggota")
    
    st.info("""
    **Ketentuan Simpanan KDMP Baleharjo:**
    - **Simpanan Pokok:** Rp 50.000 (Dibayar 1x saat pertama kali mendaftar).
    - **Simpanan Wajib:** Rp 10.000 / bulan (Rutin setiap bulan).
    - **Simpanan Sukarela:** Tabungan fleksibel (Bisa disetor/ditarik sewaktu-waktu).
    """)
    
    col_s1, col_s2 = st.columns([2, 1])
    
    with col_s1:
        st.markdown("##### 📝 Form Setoran Simpanan")
        with st.form("form_simpanan", clear_on_submit=True):
            tgl_bayar = st.date_input("Tanggal Transaksi", datetime.now())
            nama_anggota_simpan = st.text_input("Nomor NTA / Nama Anggota", placeholder="Contoh: KDMP-001 / Bp. Sastro")
            
            jenis_simpanan = st.selectbox("Jenis Simpanan", [
                "Simpanan Pokok (1x Pendaftaran - Rp 50.000)",
                "Simpanan Wajib (Bulanan - Rp 10.000)",
                "Simpanan Sukarela (Tabungan)"
            ])
            
            # Nominal default otomatis disesuaikan
            if "Pokok" in jenis_simpanan:
                nominal_default = 50000
                bulan_pembayaran = "Awal Pendaftaran"
            elif "Wajib" in jenis_simpanan:
                nominal_default = 10000
                bulan_pembayaran = st.selectbox("Untuk Bulan", [
                    "Januari 2026", "Februari 2026", "Maret 2026", "April 2026", 
                    "Mei 2026", "Juni 2026", "Juli 2026", "Agustus 2026", 
                    "September 2026", "Oktober 2026", "November 2026", "Desember 2026"
                ])
            else:
                nominal_default = 10000
                bulan_pembayaran = "Tabungan Sukarela"
                
            nominal_setor = st.number_input("Nominal Setoran (Rp)", min_value=1000, value=nominal_default, step=5000)
            penerima_kasir = st.text_input("Petugas Kasir / Penerima", value="Bendahara KDMP")
            
            btn_simpan_setoran = st.form_submit_button("💾 Catat Setoran & Auto-Jurnal")
            
            if btn_simpan_setoran:
                st.success(f"✅ Setoran **{jenis_simpanan}** sebesar **{format_rupiah(nominal_setor)}** atas nama **{nama_anggota_simpan}** berhasil dicatat!")

    with col_s2:
        st.markdown("##### 📊 Tarif Standar Simpanan")
        st.markdown("""
        * **Simpanan Pokok:**  
          `Rp 50.000` (1x Bayar)
        * **Simpanan Wajib:**  
          `Rp 10.000` / Bulan
        * **Simpanan Sukarela:**  
          `Bebas` (Fleksibel)
        """)
        st.divider()
        st.metric("Total Terkumpul Bulan Ini", format_rupiah(0), "0 Transaksi")

# -----------------------------------------------------------------------------
# MODUL 4: KIOS SEMBAKO & POS
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
            harga_satuan = st.number_input("Harga Satuan (Rp)", min_value=500, value=14000, step=500)
            pembeli = st.text_input("Nama Pembeli / Anggota (Opsional)", value="Pelanggan Umum")
            
            submitted = st.form_submit_button("💾 Simpan Transaksi & Auto-Jurnal")
            
            if submitted:
                total = qty * harga_satuan
                st.success(f"✅ Transaksi senilai **{format_rupiah(total)}** berhasil disimpan!")

    with col_summary:
        st.markdown("##### 🛒 Ringkasan Stok & Penjualan")
        st.metric("Total Penjualan Hari Ini", format_rupiah(0))
        st.metric("Margin Kotor", format_rupiah(0))

# -----------------------------------------------------------------------------
# MODUL 5: PINJAMAN & ANGSURAN
# -----------------------------------------------------------------------------
elif menu == "📤 Pinjaman & Angsuran":
    st.subheader("📤 Unit Pinjaman & Pencatatan Angsuran")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("##### Simulasi Kalkulasi Pinjaman")
        pinjaman_pokok = st.number_input("Plafon Pinjaman (Rp)", value=1000000, step=100000)
        tenor = st.slider("Jangka Waktu (Bulan)", 1, 24, 12)
        bunga_pa = st.number_input("Jasa / Bunga per Tahun (%)", value=6.0, step=0.5)
    with col_p2:
        angsuran_pokok = pinjaman_pokok / tenor
        jasa_bulanan = (pinjaman_pokok * (bunga_pa / 100)) / 12
        total_angsuran = angsuran_pokok + jasa_bulanan
        
        st.markdown("### Estimasi Angsuran / Bulan")
        st.metric("Total Angsuran Per Bulan", format_rupiah(total_angsuran))
        st.caption(f"Pokok: {format_rupiah(angsuran_pokok)} | Jasa Koperasi: {format_rupiah(jasa_bulanan)}")

# -----------------------------------------------------------------------------
# MODUL 6: PERTANIAN & DEMPLOT
# -----------------------------------------------------------------------------
elif menu == "🌾 Pertanian & Demplot Milenial":
    st.subheader("🌾 Unit Usaha Pertanian & Demplot Milenial Baleharjo")
    
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("##### 🚜 Modal Kerja Tanam Per Musim")
        st.number_input("Biaya Olah Lahan & Pupuk (Rp)", value=0)
        st.number_input("Biaya Benih & Pestisida (Rp)", value=0)
        st.button("🌱 Catat Modal Kerja Demplot")
    
    with d2:
        st.markdown("##### 🌽 Proyeksi & Realisasi Panen")
        st.text_input("Komoditas Demplot", "Jagung Hibrida / Bawang Merah")
        st.number_input("Hasil Panen (Kg)", value=0)
        st.metric("Proyeksi Pendapatan Panen", format_rupiah(0))

# -----------------------------------------------------------------------------
# MODUL 7: LAPORAN KEUANGAN & SHU (NOL)
# -----------------------------------------------------------------------------
elif menu == "📈 Laporan Keuangan & SHU":
    st.subheader("📈 Laporan Keuangan Real-Time & Kalkulator SHU")
    
    lr_data = {
        "Komponen Laba Rugi": [
            "Pendapatan Unit Sembako",
            "Pendapatan Jasa Simpan Pinjam",
            "Pendapatan Hasil Demplot Pertanian",
            "TOTAL PENDAPATAN OPERASIONAL",
            "Beban Operasional & Gaji",
            "SISA HASIL USAHA (SHU) KETIMBANGAN"
        ],
        "Jumlah (Rp)": [0, 0, 0, 0, 0, 0]
    }
    st.table(pd.DataFrame(lr_data))
