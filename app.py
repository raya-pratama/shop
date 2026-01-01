import streamlit as st
import requests

# --- KONFIGURASI TELEGRAM (Ambil dari Secrets) ---
TOKEN_BOT = st.secrets["8524772260:AAF-RVpHSIqzwwsbkQ1D-6VEqQ2_YC3smhY"]
CHAT_ID_KAMU = st.secrets["6392404663"]

def kirim_ke_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    data = {"chat_id": CHAT_ID_KAMU, "text": pesan, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# --- SETTING HALAMAN ---
st.set_page_config(page_title="Digital Card Shop", layout="wide")

st.title("🛒 Digital Store")
st.write("Pilih produk terbaik kami dan selesaikan pembayaran.")

# --- DATA PRODUK ---
# Ganti URL gambar dengan link gambar aslimu
products = [
    {
        "id": "1",
        "nama": "Modul Cisco CCNA",
        "harga": 50000,
        "gambar": "https://via.placeholder.com/300x200.png?text=Modul+CCNA",
        "desc": "Panduan lengkap konfigurasi Routing & Switching."
    },
    {
        "id": "2",
        "nama": "Python Automation",
        "harga": 75000,
        "gambar": "https://via.placeholder.com/300x200.png?text=Python+Auto",
        "desc": "Belajar membuat bot otomatisasi dengan Python."
    },
    {
        "id": "3",
        "nama": "E-Book Mikrotik",
        "harga": 45000,
        "gambar": "https://via.placeholder.com/300x200.png?text=Mikrotik+Guide",
        "desc": "Kuasai MTCNA dalam waktu singkat."
    }
]

# --- TAMPILAN CARD ---
cols = st.columns(3) # Membuat 3 kolom menyamping

for i, p in enumerate(products):
    with cols[i % 3]:
        with st.container(border=True): # Membuat border seperti Card
            st.image(p['gambar'], use_container_width=True)
            st.subheader(p['nama'])
            st.write(f"**Harga: Rp{p['harga']:,}**")
            st.caption(p['desc'])
            
            # Tombol Beli tiap produk
            if st.button(f"Beli {p['nama']}", key=f"btn_{p['id']}"):
                st.session_state['produk_dipilih'] = p
                st.session_state['show_form'] = True

st.divider()

# --- FORM PEMBELIAN (Akan muncul jika tombol di klik) ---
if st.session_state.get('show_form'):
    p = st.session_state['produk_dipilih']
    st.subheader(f"📝 Form Pembelian: {p['nama']}")
    
    with st.form("form_checkout"):
        email_user = st.text_input("Masukkan Email Anda:", placeholder="contoh@mail.com")
        st.write(f"Total yang harus dibayar: **Rp{p['harga']:,}**")
        
        btn_confirm = st.form_submit_button("Konfirmasi & Kirim Pesanan")
        
        if btn_confirm:
            if email_user:
                # Susun pesan untuk Telegram
                pesan = f"""
🚀 *PESANAN BARU MASUK!*
--------------------------
📦 *Produk:* {p['nama']}
💰 *Harga:* Rp{p['harga']:,}
📧 *Email:* {email_user}
--------------------------
                """
                kirim_ke_telegram(pesan)
                
                st.success(f"Terima kasih! Pesanan {p['nama']} telah diteruskan ke admin. Cek email Anda segera.")
                st.balloons()
                # Reset form
                st.session_state['show_form'] = False
            else:
                st.error("Email wajib diisi!")
