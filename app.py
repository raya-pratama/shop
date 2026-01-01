import streamlit as st
import requests

# --- KONFIGURASI (Ambil dari Secrets) ---
TOKEN_BOT = st.secrets["TOKEN_BOT"]
CHAT_ID_KAMU = st.secrets["CHAT_ID_KAMU"]
QRIS_IMAGE_URL = "https://link-ke-foto-qris-kamu.com/qris.jpg" # Ganti dengan link foto QRIS kamu

def kirim_ke_telegram(pesan, file=None):
    url_msg = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    requests.post(url_msg, data={"chat_id": CHAT_ID_KAMU, "text": pesan, "parse_mode": "Markdown"})
    
    if file:
        url_file = f"https://api.telegram.org/bot{TOKEN_BOT}/sendPhoto"
        requests.post(url_file, data={"chat_id": CHAT_ID_KAMU}, files={"photo": file})

# --- SETTING HALAMAN ---
st.set_page_config(page_title="Digital Shop", layout="wide")

@st.dialog("Langkah Pembayaran")
def bayar_dan_konfirmasi(produk):
    st.warning(f"Silakan transfer **Rp{produk['harga']:,}** terlebih dahulu.")
    
    # 1. TAMPILKAN QRIS
    st.image(QRIS_IMAGE_URL, caption="Scan QRIS ini untuk membayar (GoPay/Dana/OVO/ShopeePay)")
    
    st.divider()
    
    # 2. FORM KONFIRMASI (Hanya diisi setelah bayar)
    st.subheader("Konfirmasi Setelah Bayar")
    email = st.text_input("Masukkan Email Anda:")
    bukti_bayar = st.file_uploader("Upload Bukti Transfer (Gambar)", type=['jpg', 'png', 'jpeg'])
    
    if st.button("Sudah Bayar & Kirim Pesanan 🚀", use_container_width=True):
        if email and bukti_bayar:
            # Notifikasi ke Telegram
            pesan_tele = f"""
💰 *PEMBAYARAN TERKONFIRMASI!*
--------------------------
📦 *Produk:* {produk['nama']}
💰 *Harga:* Rp{produk['harga']:,}
📧 *Email:* {email}
--------------------------
Admin, silakan cek mutasi dan kirim produk!
            """
            # Kirim Pesan & Foto Bukti ke Telegram
            kirim_ke_telegram(pesan_tele, bukti_bayar.getvalue())
            
            st.success("Terima kasih! Bukti bayar telah dikirim ke Admin. Produk akan segera diproses ke email Anda.")
            st.balloons()
        else:
            st.error("Mohon isi email dan upload bukti transfer!")

# --- TAMPILAN KATALOG ---
st.title("🛒 Digital Store")
products = [
    {"id": "1", "nama": "Modul CCNA", "harga": 50000, "gambar": "https://via.placeholder.com/300x200?text=CCNA"},
    {"id": "2", "nama": "Python Auto", "harga": 75000, "gambar": "https://via.placeholder.com/300x200?text=Python"}
]

cols = st.columns(3)
for i, p in enumerate(products):
    with cols[i % 3]:
        with st.container(border=True):
            st.image(p['gambar'], use_container_width=True)
            st.subheader(p['nama'])
            st.write(f"Harga: **Rp{p['harga']:,}**")
            
            if st.button(f"Beli {p['nama']}", key=f"btn_{p['id']}", use_container_width=True):
                bayar_dan_konfirmasi(p)
