import streamlit as st
import requests

# --- 1. KONFIGURASI (Ambil dari Secrets) ---
TOKEN_BOT = st.secrets["TOKEN_BOT"]
CHAT_ID_KAMU = st.secrets["CHAT_ID_KAMU"]
# Ganti dengan link gambar QRIS kamu (bisa upload ke GitHub atau Imgur)
URL_QRIS = "https://your-link-to-qris.com/my-qris.png" 

def kirim_ke_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": CHAT_ID_KAMU, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        st.error(f"Gagal lapor ke Telegram: {e}")

# --- 2. FUNGSI ALERT/POP-UP ---
@st.dialog("Konfirmasi Pembayaran")
def pop_up_bayar(produk):
    st.write(f"Produk: **{produk['nama']}**")
    st.write(f"Total Transfer: **Rp{produk['harga']:,}**")
    st.divider()
    
    # Menampilkan QRIS
    st.image(URL_QRIS, caption="Scan menggunakan Dana, GoPay, OVO, atau M-Banking", use_container_width=True)
    
    st.info("💡 Silakan transfer sesuai nominal, lalu isi form di bawah untuk konfirmasi.")
    
    email = st.text_input("Masukkan Email Anda:", placeholder="email@contoh.com")
    
    if st.button("Sudah Bayar & Kirim Notifikasi 🚀", use_container_width=True):
        if email:
            # Kirim pesan ke Telegram
            pesan_admin = f"""
💰 *ADA PEMBAYARAN MASUK!*
--------------------------
📦 *Produk:* {produk['nama']}
💰 *Nominal:* Rp{produk['harga']:,}
📧 *Email:* {email}
--------------------------
📢 *Segera cek mutasi saldo kamu!*
            """
            kirim_ke_telegram(pesan_admin)
            
            st.success("Notifikasi terkirim! Admin akan mengecek saldo dan mengirimkan produk ke email Anda secepatnya.")
            st.balloons()
        else:
            st.error("Mohon isi email agar admin bisa mengirimkan produknya!")

# --- 3. TAMPILAN KATALOG ---
st.set_page_config(page_title="My Shop QRIS", layout="wide")
st.title("🛍️ Digital Store (QRIS Payment)")
st.write("Belanja instan, kirim cepat via Telegram.")

# Daftar Produk (Bisa kamu tambah sesukanya)
products = [
    {"id": "01", "nama": "Modul Cisco CCNA", "harga": 50000, "gambar": "https://via.placeholder.com/300x200?text=CCNA"},
    {"id": "02", "nama": "E-Book Python", "harga": 75000, "gambar": "https://via.placeholder.com/300x200?text=Python"},
    {"id": "03", "nama": "Akses Simulator", "harga": 0, "gambar": "https://via.placeholder.com/300x200?text=Gratis"}
]

cols = st.columns(3)
for i, p in enumerate(products):
    with cols[i % 3]:
        with st.container(border=True):
            st.image(p['gambar'], use_container_width=True)
            st.subheader(p['nama'])
            st.write(f"Harga: **Rp{p['harga']:,}**" if p['harga'] > 0 else "**GRATIS**")
            
            if st.button(f"Beli {p['nama']}", key=f"beli_{p['id']}", use_container_width=True):
                pop_up_bayar(p)
