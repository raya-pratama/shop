import streamlit as st
import requests

# --- KONFIGURASI TELEGRAM ---
# Masukkan Token dan Chat ID kamu di sini (atau di Secrets Streamlit)
TOKEN_BOT = "ISI_TOKEN_BOT_KAMU"
CHAT_ID_KAMU = "ISI_CHAT_ID_KAMU"

def kirim_ke_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    data = {"chat_id": CHAT_ID_KAMU, "text": pesan, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# --- TAMPILAN WEBSITE ---
st.set_page_config(page_title="My Simple Shop", page_icon="🛍️")
st.title("🛍️ Digital Product Shop")

# Data Produk
products = {
    "Modul Cisco CCNA": 50000,
    "E-Book Python Dasar": 35000,
    "Akses Simulator Premium": 100000
}

# 1. Pilih Produk
st.subheader("Pilih Produk")
pilihan_produk = st.selectbox("Produk yang tersedia:", list(products.keys()))
harga = products[pilihan_produk]
st.info(f"Harga: Rp{harga:,}")

# 2. Form Pembelian
st.subheader("Form Pembeli")
with st.form("checkout_form"):
    email = st.text_input("Alamat Email", placeholder="email@contoh.com")
    metode_bayar = st.selectbox("Metode Pembayaran", ["QRIS", "Transfer Bank", "Dana/OVO"])
    catatan = st.text_area("Catatan Tambahan (Opsional)")
    
    submit = st.form_submit_button("Konfirmasi Pembelian 🚀")

if submit:
    if email:
        # Susun Pesan untuk Telegram
        pesan_tele = f"""
🔔 *ADA PESANAN BARU!*
----------------------------
📦 *Produk:* {pilihan_produk}
💰 *Harga:* Rp{harga:,}
📧 *Email:* {email}
💳 *Bayar:* {metode_bayar}
📝 *Catatan:* {catatan if catatan else '-'}
----------------------------
        """
        
        # Kirim Notifikasi
        try:
            kirim_ke_telegram(pesan_tele)
            st.success("✅ Pesanan berhasil dikirim! Kami akan menghubungi email Anda untuk instruksi pembayaran.")
            st.balloons()
        except Exception as e:
            st.error("Gagal mengirim pesanan. Coba lagi nanti.")
    else:
        st.warning("Mohon isi email Anda terlebih dahulu.")

# Footer
st.divider()
st.caption("© 2024 Simple Shop System - Notifikasi via Telegram")
