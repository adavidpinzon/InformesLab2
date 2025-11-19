#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de gráficas para el análisis de campos magnéticos
I9: Estudio del campo magnético producido por diferentes configuraciones de corriente
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Configuración de matplotlib para español
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.titlesize'] = 16

# Valor teorico de mu0
mu0_teorico = 4 * np.pi * 1e-7  # T·m/A

# Datos experimentales
# I. Conductor rectilíneo (s = 1 mm = 0.001 m)
conductor_data = {
    'I': np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 9.5]),
    'B': np.array([0.040, 0.083, 0.125, 0.170, 0.220, 0.260, 0.295, 0.350, 0.380, 0.400]),  # mT
    's': 0.001,  # m
    'etiqueta': 'Conductor rectilíneo'
}

# II. Espiras conductoras (R = 2 cm = 0.02 m)
espiras_data = {
    'I': np.array([1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9]),
    'B': np.array([0.038, 0.060, 0.080, 0.090, 0.095, 0.120, 0.125, 0.130, 0.143, 0.148]),  # mT
    'R': 0.02,  # m
    'etiqueta': 'Espira circular'
}

# III. Solenoide 1 (N=500, L=9 mH)
solenoide1_data = {
    'I': np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]),
    'B': np.array([1.333, 2.805, 3.735, 4.445, 5.863, 7.205, 8.165, 9.110, 10.420, 11.490]),  # mT
    'N': 500,
    'L': 9e-3,  # mH a H
    'etiqueta': 'Solenoide (N=500, L=9 mH)'
}

# III. Solenoide 2 (N=1000, L=36 mH)
solenoide2_data = {
    'I': np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]),
    'B': np.array([2.978, 4.515, 6.365, 8.488, 11.095, 12.520, 15.070, 17.290, 18.950, 21.120]),  # mT
    'N': 1000,
    'L': 36e-3,  # mH a H
    'etiqueta': 'Solenoide (N=1000, L=36 mH)'
}

def crear_carpeta_graficas():
    """Crear carpeta graficas si no existe"""
    graficas_dir = Path('graficas')
    graficas_dir.mkdir(exist_ok=True)
    return graficas_dir

def ajuste_lineal(I, B):
    """Realizar ajuste lineal B vs I y calcular mu0"""
    # Convertir B de mT a T
    B_T = B * 1e-3
    
    # Ajuste lineal: B = m * I
    slope, intercept, r_value, p_value, std_err = stats.linregress(I, B_T)
    
    return slope, intercept, r_value**2, std_err

def grafica_conductor_rectilineo():
    """Gráfica 1: B vs I para conductor rectilíneo"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    I = conductor_data['I']
    B = conductor_data['B']
    
    # Ajuste lineal
    slope, intercept, r2, std_err = ajuste_lineal(I, B)
    
    # Calcular mu0 experimental
    s = conductor_data['s']
    mu0_exp = 2 * np.pi * s * slope
    
    # Línea de ajuste
    I_fit = np.linspace(0, 10, 100)
    B_fit = (slope * I_fit + intercept) * 1e3  # Convertir a mT
    
    ax.plot(I, B, 'bo', markersize=8, label='Datos experimentales')
    ax.plot(I_fit, B_fit, 'r-', linewidth=2, label=f'Ajuste lineal (R²={r2:.4f})')
    
    ax.set_xlabel('Corriente I [A]')
    ax.set_ylabel('Campo magnético B [mT]')
    ax.set_title(f'{conductor_data["etiqueta"]}\nmu0 experimental = {mu0_exp*1e6:.2f}x10^-6 T·m/A')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('graficas/conductor_rectilineo.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: graficas/conductor_rectilineo.png")
    print(f"    mu0 experimental: {mu0_exp*1e6:.2f}x10^-6 T·m/A (teorico: {mu0_teorico*1e6:.2f}x10^-6)")

def grafica_espiras():
    """Gráfica 2: B vs I para espiras circulares"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    I = espiras_data['I']
    B = espiras_data['B']
    
    # Ajuste lineal
    slope, intercept, r2, std_err = ajuste_lineal(I, B)
    
    # Calcular mu0 experimental
    R = espiras_data['R']
    mu0_exp = 2 * R * slope
    
    # Línea de ajuste
    I_fit = np.linspace(1, 4, 100)
    B_fit = (slope * I_fit + intercept) * 1e3  # Convertir a mT
    
    ax.plot(I, B, 'go', markersize=8, label='Datos experimentales')
    ax.plot(I_fit, B_fit, 'r-', linewidth=2, label=f'Ajuste lineal (R²={r2:.4f})')
    
    ax.set_xlabel('Corriente I [A]')
    ax.set_ylabel('Campo magnético B [mT]')
    ax.set_title(f'{espiras_data["etiqueta"]} (R={espiras_data["R"]*1000:.0f} mm)\nmu0 experimental = {mu0_exp*1e6:.2f}x10^-6 T·m/A')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('graficas/espiras_circulares.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: graficas/espiras_circulares.png")
    print(f"    mu0 experimental: {mu0_exp*1e6:.2f}x10^-6 T·m/A (teorico: {mu0_teorico*1e6:.2f}x10^-6)")

def grafica_solenoides():
    """Gráfica 3: B vs I para ambos solenoides"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Solenoide 1
    I1 = solenoide1_data['I']
    B1 = solenoide1_data['B']
    slope1, intercept1, r2_1, std_err1 = ajuste_lineal(I1, B1)
    n1 = solenoide1_data['N'] / solenoide1_data['L']  # espiras por metro
    mu0_exp1 = slope1 / n1
    
    I_fit1 = np.linspace(0, 2.2, 100)
    B_fit1 = (slope1 * I_fit1 + intercept1) * 1e3
    
    ax1.plot(I1, B1, 'bo', markersize=8, label='Datos experimentales')
    ax1.plot(I_fit1, B_fit1, 'r-', linewidth=2, label=f'Ajuste lineal (R²={r2_1:.4f})')
    ax1.set_xlabel('Corriente I [A]')
    ax1.set_ylabel('Campo magnético B [mT]')
    ax1.set_title(f'{solenoide1_data["etiqueta"]}\nmu0 = {mu0_exp1*1e6:.2f}x10^-6 T·m/A')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Solenoide 2
    I2 = solenoide2_data['I']
    B2 = solenoide2_data['B']
    slope2, intercept2, r2_2, std_err2 = ajuste_lineal(I2, B2)
    n2 = solenoide2_data['N'] / solenoide2_data['L']  # espiras por metro
    mu0_exp2 = slope2 / n2
    
    I_fit2 = np.linspace(0, 2.2, 100)
    B_fit2 = (slope2 * I_fit2 + intercept2) * 1e3
    
    ax2.plot(I2, B2, 'go', markersize=8, label='Datos experimentales')
    ax2.plot(I_fit2, B_fit2, 'r-', linewidth=2, label=f'Ajuste lineal (R²={r2_2:.4f})')
    ax2.set_xlabel('Corriente I [A]')
    ax2.set_ylabel('Campo magnético B [mT]')
    ax2.set_title(f'{solenoide2_data["etiqueta"]}\nmu0 = {mu0_exp2*1e6:.2f}x10^-6 T·m/A')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('graficas/solenoides.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: graficas/solenoides.png")
    print(f"    Solenoide 1 - mu0: {mu0_exp1*1e6:.2f}x10^-6 T·m/A")
    print(f"    Solenoide 2 - mu0: {mu0_exp2*1e6:.2f}x10^-6 T·m/A")

def grafica_comparacion_mu0():
    """Grafica 4: Comparacion de valores de mu0 obtenidos"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calcular mu0 para cada configuracion
    slope_c, _, _, _ = ajuste_lineal(conductor_data['I'], conductor_data['B'])
    mu0_c = 2 * np.pi * conductor_data['s'] * slope_c
    
    slope_e, _, _, _ = ajuste_lineal(espiras_data['I'], espiras_data['B'])
    mu0_e = 2 * espiras_data['R'] * slope_e
    
    slope_s1, _, _, _ = ajuste_lineal(solenoide1_data['I'], solenoide1_data['B'])
    n1 = solenoide1_data['N'] / solenoide1_data['L']
    mu0_s1 = slope_s1 / n1
    
    slope_s2, _, _, _ = ajuste_lineal(solenoide2_data['I'], solenoide2_data['B'])
    n2 = solenoide2_data['N'] / solenoide2_data['L']
    mu0_s2 = slope_s2 / n2
    
    configuraciones = ['Conductor\nrectilíneo', 'Espira\ncircular', 'Solenoide\n(N=500)', 'Solenoide\n(N=1000)']
    mu0_valores = [mu0_c, mu0_e, mu0_s1, mu0_s2]
    mu0_teorico_list = [mu0_teorico] * 4
    
    x_pos = np.arange(len(configuraciones))
    width = 0.35
    
    bars1 = ax.bar(x_pos - width/2, [m*1e6 for m in mu0_valores], width, 
                   label='mu0 experimental', color='skyblue', alpha=0.8)
    bars2 = ax.bar(x_pos + width/2, [mu0_teorico*1e6] * 4, width, 
                   label='mu0 teorico', color='lightcoral', alpha=0.8)
    
    ax.set_xlabel('Configuracion')
    ax.set_ylabel('mu0 [x10^-6 T·m/A]')
    ax.set_title('Comparacion de valores de mu0 obtenidos experimentalmente')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(configuraciones)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores sobre las barras
    for i, (bar, val) in enumerate(zip(bars1, mu0_valores)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{val*1e6:.2f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('graficas/comparacion_mu0.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: graficas/comparacion_mu0.png")

def resumen_estadistico():
    """Imprimir resumen estadístico"""
    print("\n" + "="*60)
    print("RESUMEN ESTADISTICO - VALORES DE mu0")
    print("="*60)
    print(f"Valor teorico: mu0 = {mu0_teorico*1e6:.2f}x10^-6 T·m/A")
    print()
    
    # Conductor
    slope, _, r2, _ = ajuste_lineal(conductor_data['I'], conductor_data['B'])
    mu0_c = 2 * np.pi * conductor_data['s'] * slope
    error_c = abs(mu0_c - mu0_teorico) / mu0_teorico * 100
    print(f"Conductor rectilineo:")
    print(f"  mu0 experimental: {mu0_c*1e6:.2f}x10^-6 T·m/A")
    print(f"  Error relativo: {error_c:.2f}%")
    print(f"  R² del ajuste: {r2:.4f}")
    print()
    
    # Espiras
    slope, _, r2, _ = ajuste_lineal(espiras_data['I'], espiras_data['B'])
    mu0_e = 2 * espiras_data['R'] * slope
    error_e = abs(mu0_e - mu0_teorico) / mu0_teorico * 100
    print(f"Espira circular:")
    print(f"  mu0 experimental: {mu0_e*1e6:.2f}x10^-6 T·m/A")
    print(f"  Error relativo: {error_e:.2f}%")
    print(f"  R² del ajuste: {r2:.4f}")
    print()
    
    # Solenoide 1
    slope, _, r2, _ = ajuste_lineal(solenoide1_data['I'], solenoide1_data['B'])
    n1 = solenoide1_data['N'] / solenoide1_data['L']
    mu0_s1 = slope / n1
    error_s1 = abs(mu0_s1 - mu0_teorico) / mu0_teorico * 100
    print(f"Solenoide (N=500, L=9 mH):")
    print(f"  mu0 experimental: {mu0_s1*1e6:.2f}x10^-6 T·m/A")
    print(f"  Error relativo: {error_s1:.2f}%")
    print(f"  R² del ajuste: {r2:.4f}")
    print()
    
    # Solenoide 2
    slope, _, r2, _ = ajuste_lineal(solenoide2_data['I'], solenoide2_data['B'])
    n2 = solenoide2_data['N'] / solenoide2_data['L']
    mu0_s2 = slope / n2
    error_s2 = abs(mu0_s2 - mu0_teorico) / mu0_teorico * 100
    print(f"Solenoide (N=1000, L=36 mH):")
    print(f"  mu0 experimental: {mu0_s2*1e6:.2f}x10^-6 T·m/A")
    print(f"  Error relativo: {error_s2:.2f}%")
    print(f"  R² del ajuste: {r2:.4f}")
    print()
    
    # Promedio
    mu0_promedio = np.mean([mu0_c, mu0_e, mu0_s1, mu0_s2])
    error_promedio = abs(mu0_promedio - mu0_teorico) / mu0_teorico * 100
    print(f"Promedio de todas las configuraciones:")
    print(f"  mu0 promedio: {mu0_promedio*1e6:.2f}x10^-6 T·m/A")
    print(f"  Error relativo: {error_promedio:.2f}%")
    print("="*60)

def main():
    """Función principal"""
    print("Generando graficas para el analisis de campos magneticos...")
    print("="*60)
    
    graficas_dir = crear_carpeta_graficas()
    print(f"[OK] Carpeta de graficas creada: {graficas_dir}")
    
    try:
        grafica_conductor_rectilineo()
        grafica_espiras()
        grafica_solenoides()
        grafica_comparacion_mu0()
        resumen_estadistico()
        
        print("\n" + "="*60)
        print("[OK] TODAS LAS GRAFICAS GENERADAS EXITOSAMENTE")
        print("  - graficas/conductor_rectilineo.png")
        print("  - graficas/espiras_circulares.png")
        print("  - graficas/solenoides.png")
        print("  - graficas/comparacion_mu0.png")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Error al generar graficas: {e}")

if __name__ == "__main__":
    main()
