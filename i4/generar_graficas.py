#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I4 - Graficas y calculos de circuitos serie, paralelo y mixto
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["figure.dpi"] = 120

# Resistores medidos (ohm)
R = {
    "R1": 46.5,
    "R2": 98.8,
    "R3": 149.5,
    "R4": 326.8,
    "R5": 216.1,
}

# Serie: I en mA, V en V
serie_I_mA = np.array([389.2, 390.1, 386.9, 390.0, 389.2])
serie_V = np.array([0.019, 0.040, 0.088, 0.133, 0.067])
serie_labels = ["R1", "R2", "R3", "R4", "R5"]

# Paralelo (sin R4): I en uA, V comun ~0.015 V
paralelo_labels = ["R1", "R2", "R3", "R5"]
paralelo_I_uA = np.array([153.7, 85.3, 64.1, 49.2])
paralelo_V = 0.015

# Mixto: I en uA, V en V (se reportan R1, R2, R3, R5)
mixto_labels = ["R1", "R2", "R3", "R5"]
mixto_I_uA = np.array([556.9, 156.2, 156.1, 156.3])
mixto_V = np.array([0.027, 0.019, 0.059, 0.041])

def ensure_dir():
    Path("graficas").mkdir(exist_ok=True)

def grafica_serie():
    # I promedio en A
    I_A_prom = serie_I_mA.mean() * 1e-3
    # V calculado por Ohm
    R_vals = np.array([R[k] for k in serie_labels])
    V_calc = I_A_prom * R_vals

    x = np.arange(len(serie_labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - width/2, serie_V, width, label="V medido")
    ax.bar(x + width/2, V_calc, width, label="I_prom*R (Ohm)")
    ax.set_xticks(x)
    ax.set_xticklabels(serie_labels)
    ax.set_ylabel("Voltaje [V]")
    ax.set_title(f"Serie: I_prom={I_A_prom*1e3:.1f} mA")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig("graficas/serie_validacion.png", bbox_inches="tight")
    plt.close()

    # Req serie
    Req = R_vals.sum()
    return Req

def grafica_paralelo():
    # Corrientes calculadas con V comun
    R_vals = np.array([R[k] for k in paralelo_labels])
    I_calc_uA = (paralelo_V / R_vals) * 1e6

    x = np.arange(len(paralelo_labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - width/2, paralelo_I_uA, width, label="I medido")
    ax.bar(x + width/2, I_calc_uA, width, label="V/R (Ohm)")
    ax.set_xticks(x)
    ax.set_xticklabels(paralelo_labels)
    ax.set_ylabel("Corriente [µA]")
    ax.set_title(f"Paralelo: V_comun={paralelo_V:.3f} V")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig("graficas/paralelo_validacion.png", bbox_inches="tight")
    plt.close()

    # Req paralelo
    Req = 1.0 / np.sum(1.0 / R_vals)
    return Req

def grafica_mixto():
    # Validacion local: R_implicita = V/I
    I_A = mixto_I_uA * 1e-6
    R_imp = mixto_V / I_A

    x = np.arange(len(mixto_labels))
    width = 0.35
    R_vals = np.array([R[k] for k in mixto_labels])

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - width/2, R_vals, width, label="R medida (ohmetro)")
    ax.bar(x + width/2, R_imp, width, label="V/I (Ohm)")
    ax.set_xticks(x)
    ax.set_xticklabels(mixto_labels)
    ax.set_ylabel("Resistencia [Ω]")
    ax.set_title("Mixto: consistencia de R por V/I")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig("graficas/mixto_validacion.png", bbox_inches="tight")
    plt.close()

def grafica_equivalentes(Req_s, Req_p, Req_m_report=149.3):
    etiquetas = ["Serie", "Paralelo", "Mixto"]
    # Calculo de paralelo y mixto teoricos/estimados ya vienen arriba; mixto se reporta
    valores = [Req_s, Req_p, Req_m_report]
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(etiquetas, valores, color=["#4c78a8", "#72b7b2", "#f58518"])
    ax.set_ylabel("R_eq [Ω]")
    ax.set_title("Resistencias equivalentes")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("graficas/equivalentes.png", bbox_inches="tight")
    plt.close()

def main():
    ensure_dir()
    Req_s = grafica_serie()
    Req_p = grafica_paralelo()
    grafica_mixto()
    grafica_equivalentes(Req_s, Req_p, Req_m_report=149.3)
    print("[OK] Graficas generadas en i4/graficas")
    print(f"Req serie   (calc) = {Req_s:.2f} ohm")
    print(f"Req paralelo(calc) = {Req_p:.2f} ohm")
    print("Req mixto   (repo) = 149.30 ohm")

if __name__ == "__main__":
    main()

