import streamlit as st
import requests
import base64
import time

# --- 1. KONFIGURASI (Pastikan sudah ada di Secrets) ---
SERVER_KEY = st.secrets["MIDTRANS_SERVER_KEY"]
TOKEN_BOT = st.secrets["TOKEN_BOT"]
CHAT_ID_KAMU = st.secrets["CHAT_ID_KAMU"]

# Fungsi Header untuk Midtrans
def get_auth_header():
    auth_string = f"{SERVER_KEY}:"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    return {"Authorization": f"Basic {encoded_auth}", "Content-Type": "application/json"}

# Fungsi kirim notifikasi ke Telegram
def kirim_ke_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID_KAMU, "text": pesan, "parse_mode": "Markdown"})

# Fungsi membuat transaksi di Midtrans
def buat_link_pembayaran(produk, email):
    # Gunakan URL sandbox untuk latihan, ganti ke 'api.midtrans.com' untuk asli
    url = "https://app.sandbox.midtrans.com/snap/v1/transactions" 
    order_id = f"ORDER-{int(time.time())}" # ID unik berdasarkan waktu
    
    payload = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": produk['harga']
        },
        "customer_details": {"email": email},
        "item_details": [{
            "id": produk['id'],
            "price": produk['harga'],
            "quantity": 1,
            "name": produk['nama']
        }]
    }
    
    response = requests.post(url, json=payload, headers=get_auth_header())
    return response.json()

# --- 2. TAMPILAN POP-UP (DIALOG) ---
@st.dialog("Konfirmasi Pembelian")
def checkout_otomatis(produk):
    st.write(f"Produk: **{produk['nama']}**")
    st.write(f"Total: **Rp{produk['harga']:,}**")
    
    email = st.text_input("Masukkan Email Anda:", placeholder="email@anda.com")
    st.caption("Link pembayaran QRIS/E-Wallet akan muncul setelah klik tombol di bawah.")
    
    if st.button("Proses Pembayaran 💳", use_container_width=True):
        if email:
            with st.spinner("Menghubungkan ke Midtrans..."):
                res = buat_link_pembayaran(produk, email)
                link_bayar = res.get('redirect_url')
                
                if link_bayar:
                    # Kirim info ke Telegram Admin bahwa ada yang baru buat order
                    pesan_admin = f"⏳ *PENDING ORDER*\n\n📦 {produk['nama']}\n📧 {email}\n💰 Rp{produk['harga']:,}\n\nUser sedang menuju halaman pembayaran."
                    kirim_ke_telegram(pesan_admin)
                    
                    st.success("Berhasil! Silakan klik tombol bayar di bawah:")
                    st.link_button("🔥 BAYAR SEKARANG (QRIS/DANA/GOPAY)", link_bayar, use_container_width=True)
                    st.info("Setelah bayar, simpan bukti bayar Anda.")
                else:
                    st.error("Gagal mengambil link pembayaran. Cek Server Key Midtrans Anda.")
        else:
            st.error("Email wajib diisi!")

# --- 3. TAMPILAN UTAMA (KATALOG) ---
st.set_page_config(page_title="My Digital Store", layout="wide")
st.title("🛒 Toko Digital")
st.write("Dapatkan produk digital terbaik dengan pembayaran instan.")

products = [
    {"id": "PROD-001", "nama": "Modul Cisco CCNA", "harga": 50000, "gambar": "https://via.placeholder.com/300x200?text=CCNA"},
    {"id": "PROD-002", "nama": "Python Automation", "harga": 75000, "gambar": "https://via.placeholder.com/300x200?text=Python"},
    {"id": "PROD-003", "nama": "E-Book Mikrotik", "harga": 45000, "gambar": "https://via.placeholder.com/300x200?text=Mikrotik"}
]

cols = st.columns(3)
for i, p in enumerate(products):
    with cols[i % 3]:
        with st.container(border=True):
            st.image(p['gambar'], use_container_width=True)
            st.subheader(p['nama'])
            st.write(f"Harga: **Rp{p['harga']:,}**")
            
            if st.button(f"Beli {p['nama']}", key=f"btn_{p['id']}", use_container_width=True):
                checkout_otomatis(p)
