import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Model Operasional", layout="wide")
st.title("📊 Aplikasi Model Operasional - Streamlit")

# Tab menu utama
tabs = st.tabs([
    "⚙️ Optimasi Produksi (Linear Programming)",
    "📦 Model Persediaan (EOQ)",
    "⏳ Model Antrian (M/M/1)",
    "📈 Pertumbuhan (Exponential Model)"
])

# =====================
# Tab 1: Linear Programming
# =====================
with tabs[0]:
    st.header("Optimasi Produksi - Linear Programming")
    
    st.markdown("Contoh: Maksimalkan Z = c1 * x1 + c2 * x2 dengan batasan linear")

    c1 = st.number_input("Koefisien x1 (objektif)", value=3.0)
    c2 = st.number_input("Koefisien x2 (objektif)", value=5.0)
    
    A = np.array([[1, 0], [0, 2], [3, 2]])
    b = np.array([4, 12, 18])
    c = [-c1, -c2]  # Linprog meminimalkan, jadi ubah tanda

    if st.button("Hitung Optimasi"):
        res = linprog(c, A_ub=A, b_ub=b, method='highs')
        if res.success:
            st.success(f"Solusi optimal: x1 = {res.x[0]:.2f}, x2 = {res.x[1]:.2f}, Z = {-res.fun:.2f}")
        else:
            st.error("Gagal menemukan solusi optimal.")

# =====================
# Tab 2: EOQ
# =====================
with tabs[1]:
    st.header("Model Persediaan - Economic Order Quantity (EOQ)")
    
    D = st.number_input("Permintaan Tahunan (D)", value=1000.0)
    S = st.number_input("Biaya Pemesanan (S)", value=50.0)
    H = st.number_input("Biaya Penyimpanan per unit per tahun (H)", value=2.0)

    if st.button("Hitung EOQ"):
        eoq = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ (Jumlah Ekonomis Pembelian): {eoq:.2f} unit")

# =====================
# Tab 3: M/M/1 Queue
# =====================
with tabs[2]:
    st.header("Model Antrian - M/M/1")

    lam = st.number_input("Laju Kedatangan (λ)", value=2.0)
    mu = st.number_input("Laju Pelayanan (μ)", value=5.0)

    if st.button("Hitung Antrian M/M/1"):
        if lam < mu:
            rho = lam / mu
            L = rho / (1 - rho)
            Lq = rho**2 / (1 - rho)
            W = 1 / (mu - lam)
            Wq = rho / (mu - lam)
            st.success(f"ρ (utilisasi): {rho:.2f}")
            st.write(f"Jumlah rata-rata dalam sistem (L): {L:.2f}")
            st.write(f"Jumlah rata-rata dalam antrian (Lq): {Lq:.2f}")
            st.write(f"Waktu rata-rata dalam sistem (W): {W:.2f}")
            st.write(f"Waktu rata-rata dalam antrian (Wq): {Wq:.2f}")
        else:
            st.error("Sistem tidak stabil (λ harus lebih kecil dari μ)")

# =====================
# Tab 4: Exponential Growth Model
# =====================
with tabs[3]:
    st.header("Pertumbuhan Eksponensial")

    P0 = st.number_input("Populasi awal (P₀)", value=100.0)
    r = st.number_input("Tingkat Pertumbuhan (r)", value=0.05)
    t = st.slider("Waktu (tahun)", min_value=1, max_value=50, value=10)

    if st.button("Hitung Pertumbuhan"):
        time = np.linspace(0, t, 100)
        Pt = P0 * np.exp(r * time)

        fig, ax = plt.subplots()
        ax.plot(time, Pt, label="P(t)")
        ax.set_title("Model Pertumbuhan Eksponensial")
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Populasi")
        ax.grid(True)
        st.pyplot(fig)

        st.success(f"Populasi pada t={t} tahun: {P0 * np.exp(r * t):.2f}")
