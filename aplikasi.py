import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.title("🚗 Aplikasi Turunan Parsial: Kecepatan Mobil")

# Variabel simbolik untuk waktu dan jarak
t, s = sp.symbols('t s')
fungsi_str = st.text_input("Masukkan fungsi kecepatan v(t, s):", "3*t**2 + 2*s + t*s")

try:
    v = sp.sympify(fungsi_str)
    vt = sp.diff(v, t)
    vs = sp.diff(v, s)

    st.latex(f"v(t, s) = {sp.latex(v)}")
    st.latex(f"\\frac{{\\partial v}}{{\\partial t}} = {sp.latex(vt)}")
    st.latex(f"\\frac{{\\partial v}}{{\\partial s}} = {sp.latex(vs)}")

    t0 = st.number_input("Nilai waktu (t₀):", value=1.0)
    s0 = st.number_input("Nilai jarak (s₀):", value=10.0)

    v_val = v.subs({t: t0, s: s0})
    vt_val = vt.subs({t: t0, s: s0})
    vs_val = vs.subs({t: t0, s: s0})

    st.write("Nilai kecepatan di titik (t₀, s₀):", v_val)
    st.write("Gradien kecepatan di titik (t₀, s₀):", f"({vt_val}, {vs_val})")

    st.subheader("📊 Grafik Kecepatan dan Bidang Singgungnya")

    t_vals = np.linspace(t0 - 2, t0 + 2, 50)
    s_vals = np.linspace(s0 - 5, s0 + 5, 50)
    T, S = np.meshgrid(t_vals, s_vals)
    V = sp.lambdify((t, s), v, 'numpy')(T, S)
    V_tangent = float(v_val) + float(vt_val)*(T - t0) + float(vs_val)*(S - s0)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(T, S, V, alpha=0.7, cmap='viridis')
    ax.plot_surface(T, S, V_tangent, alpha=0.5, color='red')
    ax.set_title("Permukaan Kecepatan v(t, s) dan bidang singgungnya")
    ax.set_xlabel('t (waktu)')
    ax.set_ylabel('s (jarak)')
    ax.set_zlabel('v (kecepatan)')
    st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
