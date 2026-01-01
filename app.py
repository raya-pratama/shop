import streamlit as st
import requests

# --- 1. KONFIGURASI (PASTIKAN SUDAH DI SECRETS) ---
TOKEN_BOT = st.secrets["TOKEN_BOT"]
CHAT_ID_KAMU = st.secrets["CHAT_ID_KAMU"]
# Ganti dengan link foto QRIS yang sudah kamu screenshot tadi
URL_QRIS = "https://your-link-to-qris.com/my-qris.png" 

def kirim_ke_telegram(pesan, file_gambar=None):
    # Kirim Pesan Teks
    url_text = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    requests.post(url_text, data={"chat_id": CHAT_ID_KAMU, "text": pesan, "parse_mode": "Markdown"})
    
    # Kirim Gambar Bukti jika ada
    if file_gambar:
        url_photo = f"https://api.telegram.org/bot{TOKEN_BOT}/sendPhoto"
        requests.post(url_photo, data={"chat_id": CHAT_ID_KAMU}, files={"photo": file_gambar})

# --- 2. TAMPILAN POP-UP (DIALOG) ---
@st.dialog("Pembayaran & Konfirmasi")
def pop_up_bayar(produk):
    st.subheader(f"Produk: {produk['nama']}")
    st.write(f"Total yang harus dibayar: **Rp{produk['harga']:,}**")
    
    # Menampilkan QRIS
    st.image(URL_QRIS, caption="Scan QRIS ini untuk membayar", use_container_width=True)
    st.warning("⚠️ Pastikan nominal yang dimasukkan tepat!")
    
    st.divider()
    
    # Form Konfirmasi
    email = st.text_input("Masukkan Email Anda:")
    bukti = st.file_uploader("Upload Bukti Transfer (Gambar)", type=['jpg', 'jpeg', 'png'])
    
    if st.button("Kirim Konfirmasi 🚀", use_container_width=True):
        if email and bukti:
            with st.spinner("Mengirim konfirmasi..."):
                # Siapkan pesan untuk Telegram
                pesan_tele = f"""
💰 *PEMBAYARAN BARU MASUK!*
--------------------------
📦 *Produk:* {produk['nama']}
💰 *Nominal:* Rp{produk['harga']:,}
📧 *Email:* {email}
--------------------------
📢 *Cek foto bukti di bawah ini!*
                """
                
                # Jalankan fungsi kirim
                kirim_ke_telegram(pesan_tele, bukti.getvalue())
                
                st.success("Berhasil! Admin akan segera mengecek saldo dan mengirimkan file ke email Anda.")
                st.balloons()
        else:
            st.error("Mohon lengkapi email dan upload bukti bayar!")

# --- 3. TAMPILAN KATALOG (CARD) ---
st.set_page_config(page_title="Shop QRIS", layout="wide")
st.title("🛍️ Digital Card Store")

products = [
    {"id": "01", "nama": "Modul Cisco CCNA", "harga": 50000, "gambar": "https://via.placeholder.com/300x200?text=CCNA"},
    {"id": "02", "nama": "E-Book Python", "harga": 75000, "gambar": "https://via.placeholder.com/300x200?text=Python"},
    {"id": "03", "nama": "Simulator Lab", "harga": 100000, "gambar": "https://via.placeholder.com/300x200?text=Simulator"}
]

cols = st.columns(3)
for i, p in enumerate(products):
    with cols[i % 3]:
        with st.container(border=True):
            st.image(p['gambar'], use_container_width=True)
            st.subheader(p['nama'])
            st.write(f"Harga: **Rp{p['harga']:,}**")
            
            if st.button(f"Beli {p['nama']}", key=f"btn_{p['id']}", use_container_width=True):
                pop_up_bayar(p)
