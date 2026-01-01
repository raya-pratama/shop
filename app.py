import streamlit as st
import requests

# --- KONFIGURASI (Ambil dari Secrets) ---
TOKEN_BOT = st.secrets["TOKEN_BOT"]
CHAT_ID_KAMU = st.secrets["CHAT_ID_KAMU"]
LINK_PEMBAYARAN = "https://link-pembayaran-kamu.com" # Ganti dengan link QRIS/Dana/Midtrans

def kirim_ke_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    data = {"chat_id": CHAT_ID_KAMU, "text": pesan, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# --- SETTING HALAMAN ---
st.set_page_config(page_title="Digital Shop Pop-up", layout="wide")

# --- FUNGSI DIALOG (MODAL/ALERT) ---
@st.dialog("Konfirmasi Pembelian")
def form_checkout(produk):
    st.write(f"Anda memilih: **{produk['nama']}**")
    st.write(f"Total Harga: **Rp{produk['harga']:,}**")
    
    email = st.text_input("Masukkan Email Anda:", placeholder="contoh@mail.com")
    st.caption("Instruksi pembayaran akan dikirim ke email ini.")
    
    if st.button("Kirim Pesanan & Bayar 🚀", use_container_width=True):
        if email:
            # Kirim Notifikasi ke Telegram
            pesan_tele = f"""
🚀 *PESANAN BARU!*
--------------------------
📦 *Produk:* {produk['nama']}
💰 *Harga:* Rp{produk['harga']:,}
📧 *Email:* {email}
--------------------------
            """
            kirim_ke_telegram(pesan_tele)
            
            # Tampilkan link bayar
            st.success("Pesanan Terdaftar!")
            st.link_button("KLIK DI SINI UNTUK BAYAR (QRIS/DANA)", LINK_PEMBAYARAN, use_container_width=True)
            st.info("Setelah bayar, silakan tutup jendela ini.")
        else:
            st.error("Email wajib diisi!")

# --- TAMPILAN UTAMA ---
st.title("🛒 Toko Digital")
st.write("Klik tombol pada produk untuk memunculkan form pembayaran.")

products = [
    {"id": "1", "nama": "Modul CCNA", "harga": 50000, "gambar": "https://via.placeholder.com/300x200?text=CCNA", "desc": "Lab lengkap Cisco."},
    {"id": "2", "nama": "Python Auto", "harga": 75000, "gambar": "https://via.placeholder.com/300x200?text=Python", "desc": "Bot otomatisasi."},
    {"id": "3", "nama": "E-Book Mikrotik", "harga": 45000, "gambar": "https://via.placeholder.com/300x200?text=Mikrotik", "desc": "Kuasai RouterOS."}
]

cols = st.columns(3)

for i, p in enumerate(products):
    with cols[i % 3]:
        with st.container(border=True):
            st.image(p['gambar'], use_container_width=True)
            st.subheader(p['nama'])
            st.write(f"**Rp{p['harga']:,}**")
            
            # Saat diklik, fungsi dialog dipanggil
            if st.button(f"Beli {p['nama']}", key=f"btn_{p['id']}", use_container_width=True):
                form_checkout(p)
