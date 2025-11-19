#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de graficas para el analisis de resistividad
I3: Determinacion de la resistividad de dos conductores: Constantan y Cromo-Niquel
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Configuracion de matplotlib para espanol
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.titlesize'] = 16

# Valores teoricos de resistividad (en ohm-metro)
# Constantan: aproximadamente 49 x 10^-8 ohm-m
# Cromo-Niquel: aproximadamente 110 x 10^-8 ohm-m
rho_constantan_teorico = 49e-8  # ohm-m
rho_cromoniquel_teorico = 110e-8  # ohm-m

# Datos experimentales - Fase 1: Medicion directa
# Constantan 0.4mm
constantan_04_directa = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'R': np.array([0.6, 0.7, 0.9, 1.1, 1.3, 1.4, 1.8, 1.9, 2.1, 2.3]),
    'D': 0.4e-3,  # m
    'material': 'Constantan',
    'diametro': '0.4 mm'
}

# Constantan 0.35mm
constantan_035_directa = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'R': np.array([0.6, 0.8, 1.0, 1.3, 1.6, 1.9, 2.1, 2.3, 2.7, 2.9]),
    'D': 0.35e-3,  # m
    'material': 'Constantan',
    'diametro': '0.35 mm'
}

# Cromo-Niquel 0.4mm
cromoniquel_04_directa = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'R': np.array([0.4, 1.1, 1.2, 1.9, 2.2, 2.9, 3.2, 3.7, 3.8, 4.3]),
    'D': 0.4e-3,  # m
    'material': 'Cromo-Niquel',
    'diametro': '0.4 mm'
}

# Cromo-Niquel 0.35mm
cromoniquel_035_directa = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'R': np.array([0.3, 0.9, 1.5, 2.2, 2.6, 3.1, 3.7, 4.3, 4.9, 5.5]),
    'D': 0.35e-3,  # m
    'material': 'Cromo-Niquel',
    'diametro': '0.35 mm'
}

# Datos experimentales - Fase 2: Medicion indirecta (Ley de Ohm)
# Constantan 0.4mm
constantan_04_ohm = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'V': np.array([0.007, 0.020, 0.033, 0.034, 0.040, 0.044, 0.045, 0.043, 0.049, 0.054]),
    'I': np.array([0.027, 0.027, None, None, None, None, None, None, None, None]),
    'D': 0.4e-3,  # m
    'material': 'Constantan',
    'diametro': '0.4 mm'
}

# Constantan 0.35mm
constantan_035_ohm = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'V': np.array([0.009, 0.015, 0.023, 0.030, 0.041, 0.046, 0.053, 0.058, 0.064, 0.071]),
    'I': None,  # No se especifica corriente constante
    'D': 0.35e-3,  # m
    'material': 'Constantan',
    'diametro': '0.35 mm'
}

# Cromo-Niquel 0.35mm (I = 0.025 A constante)
cromoniquel_035_ohm = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'V': np.array([0.015, 0.034, 0.054, 0.069, 0.082, 0.096, 0.115, 0.121, 0.147, 0.154]),
    'I': 0.025,  # A constante
    'D': 0.35e-3,  # m
    'material': 'Cromo-Niquel',
    'diametro': '0.35 mm'
}

# Cromo-Niquel 0.4mm
cromoniquel_04_ohm = {
    'L_cm': np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50]),
    'V': np.array([0.020, 0.026, 0.042, 0.052, 0.059, 0.100, 0.108, 0.114, 0.125, 0.134]),
    'I': None,  # No se especifica
    'D': 0.4e-3,  # m
    'material': 'Cromo-Niquel',
    'diametro': '0.4 mm'
}

def calcular_area(diametro):
    """Calcular area transversal del alambre"""
    r = diametro / 2
    return np.pi * r**2

def calcular_L_A(longitudes_cm, diametro):
    """Calcular L/A para cada longitud"""
    L = longitudes_cm * 1e-2  # Convertir a metros
    A = calcular_area(diametro)
    return L / A

def ajuste_lineal(x, y):
    """Realizar ajuste lineal y calcular resistividad"""
    # Filtrar valores None si existen
    mask = ~(np.isnan(x) | np.isnan(y))
    x_clean = x[mask]
    y_clean = y[mask]
    
    if len(x_clean) < 2:
        return None, None, None, None
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
    return slope, intercept, r_value**2, std_err

def grafica_fase1_material(data, material_name):
    """Grafica R vs L/A para un material en Fase 1"""
    L_cm = data['L_cm']
    R = data['R']
    D = data['D']
    
    L_A = calcular_L_A(L_cm, D)
    
    # Ajuste lineal
    slope, intercept, r2, std_err = ajuste_lineal(L_A, R)
    rho_exp = slope  # La pendiente es la resistividad
    
    # Linea de ajuste
    L_A_fit = np.linspace(0, L_A.max() * 1.1, 100)
    R_fit = slope * L_A_fit + intercept
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(L_A, R, 'bo', markersize=8, label='Datos experimentales')
    ax.plot(L_A_fit, R_fit, 'r-', linewidth=2, label=f'Ajuste lineal (R²={r2:.4f})')
    
    ax.set_xlabel('L/A [m⁻¹]')
    ax.set_ylabel('Resistencia R [Ω]')
    ax.set_title(f'{data["material"]} {data["diametro"]} - Fase 1: Medicion directa\nρ = {rho_exp*1e8:.2f}×10⁻⁸ Ω·m')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    filename = f'graficas/{material_name.lower().replace("-", "_")}_{data["diametro"].replace(".", "")}_fase1.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: {filename}")
    return rho_exp, r2

def grafica_fase2_material(data, material_name):
    """Grafica R vs L/A para un material en Fase 2"""
    L_cm = data['L_cm']
    V = data['V']
    I = data['I']
    D = data['D']
    
    # Calcular R usando ley de Ohm
    if isinstance(I, (int, float)):
        # Corriente constante
        R = V / I
    elif I is None or len([x for x in I if x is not None]) < 2:
        # No hay suficientes datos de corriente, usar solo V
        # Asumir que podemos calcular R si tenemos al menos algunos valores de I
        # Para este caso, usaremos solo los datos donde tenemos I
        if 'I' in data and data['I'] is not None and isinstance(data['I'], np.ndarray):
            mask = ~np.isnan(data['I'])
            R = np.full_like(V, np.nan)
            R[mask] = V[mask] / data['I'][mask]
        else:
            # No podemos calcular R sin I
            print(f"[WARNING] No se puede calcular R para {material_name} {data['diametro']} sin valores de corriente")
            return None, None
    else:
        # I es un array, calcular R para cada punto
        R = np.array([v / i if i is not None and i != 0 else np.nan for v, i in zip(V, I)])
    
    # Filtrar valores validos
    mask = ~np.isnan(R)
    L_cm_valid = L_cm[mask]
    R_valid = R[mask]
    
    if len(R_valid) < 2:
        print(f"[WARNING] No hay suficientes datos validos para {material_name} {data['diametro']}")
        return None, None
    
    L_A = calcular_L_A(L_cm_valid, D)
    
    # Ajuste lineal
    slope, intercept, r2, std_err = ajuste_lineal(L_A, R_valid)
    if slope is None:
        return None, None
    
    rho_exp = slope
    
    # Linea de ajuste
    L_A_fit = np.linspace(0, L_A.max() * 1.1, 100)
    R_fit = slope * L_A_fit + intercept
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(L_A, R_valid, 'go', markersize=8, label='Datos experimentales')
    ax.plot(L_A_fit, R_fit, 'r-', linewidth=2, label=f'Ajuste lineal (R²={r2:.4f})')
    
    ax.set_xlabel('L/A [m⁻¹]')
    ax.set_ylabel('Resistencia R [Ω]')
    ax.set_title(f'{data["material"]} {data["diametro"]} - Fase 2: Ley de Ohm\nρ = {rho_exp*1e8:.2f}×10⁻⁸ Ω·m')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    filename = f'graficas/{material_name.lower().replace("-", "_")}_{data["diametro"].replace(".", "")}_fase2.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: {filename}")
    return rho_exp, r2

def calcular_resistividad_fase1(data):
    """Calcular resistividad sin generar grafica"""
    L_cm = data['L_cm']
    R = data['R']
    D = data['D']
    
    L_A = calcular_L_A(L_cm, D)
    slope, intercept, r2, std_err = ajuste_lineal(L_A, R)
    
    if slope is None:
        return None, None
    return slope, r2

def calcular_resistividad_fase2(data):
    """Calcular resistividad sin generar grafica"""
    L_cm = data['L_cm']
    V = data['V']
    I = data['I']
    D = data['D']
    
    # Calcular R usando ley de Ohm
    if isinstance(I, (int, float)):
        R = V / I
    elif I is None or (isinstance(I, np.ndarray) and len([x for x in I if x is not None]) < 2):
        return None, None
    else:
        R = np.array([v / i if i is not None and i != 0 else np.nan for v, i in zip(V, I)])
    
    mask = ~np.isnan(R)
    L_cm_valid = L_cm[mask]
    R_valid = R[mask]
    
    if len(R_valid) < 2:
        return None, None
    
    L_A = calcular_L_A(L_cm_valid, D)
    slope, intercept, r2, std_err = ajuste_lineal(L_A, R_valid)
    
    if slope is None:
        return None, None
    return slope, r2

def grafica_comparacion_resistividades(rho_values):
    """Grafica comparativa de resistividades obtenidas"""
    # rho_values es un diccionario con los valores ya calculados
    
    # Preparar datos para grafica
    configuraciones = []
    valores_fase1 = []
    valores_fase2 = []
    valores_teoricos = []
    
    rho_c04_1 = rho_values.get('constantan_04_fase1', (None, None))[0]
    rho_c035_1 = rho_values.get('constantan_035_fase1', (None, None))[0]
    rho_cn04_1 = rho_values.get('cromoniquel_04_fase1', (None, None))[0]
    rho_cn035_1 = rho_values.get('cromoniquel_035_fase1', (None, None))[0]
    rho_cn035_2 = rho_values.get('cromoniquel_035_fase2', (None, None))[0]
    
    if rho_c04_1:
        configuraciones.append('Constantan\n0.4mm')
        valores_fase1.append(rho_c04_1 * 1e8)
        valores_fase2.append(None)
        valores_teoricos.append(rho_constantan_teorico * 1e8)
    
    if rho_c035_1:
        configuraciones.append('Constantan\n0.35mm')
        valores_fase1.append(rho_c035_1 * 1e8)
        valores_fase2.append(None)
        valores_teoricos.append(rho_constantan_teorico * 1e8)
    
    if rho_cn04_1:
        configuraciones.append('Cromo-Niquel\n0.4mm')
        valores_fase1.append(rho_cn04_1 * 1e8)
        valores_fase2.append(None)
        valores_teoricos.append(rho_cromoniquel_teorico * 1e8)
    
    if rho_cn035_1:
        configuraciones.append('Cromo-Niquel\n0.35mm')
        valores_fase1.append(rho_cn035_1 * 1e8)
        valores_fase2.append(rho_cn035_2 * 1e8 if rho_cn035_2 else None)
        valores_teoricos.append(rho_cromoniquel_teorico * 1e8)
    
    x_pos = np.arange(len(configuraciones))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Filtrar valores None
    valores_f1_clean = [v if v is not None else 0 for v in valores_fase1]
    valores_f2_clean = [v if v is not None else 0 for v in valores_fase2]
    valores_teo_clean = valores_teoricos
    
    bars1 = ax.bar(x_pos - width, valores_f1_clean, width, label='Fase 1 (Directa)', color='skyblue', alpha=0.8)
    bars2 = ax.bar(x_pos, valores_f2_clean, width, label='Fase 2 (Ohm)', color='lightgreen', alpha=0.8)
    bars3 = ax.bar(x_pos + width, valores_teo_clean, width, label='Teorico', color='lightcoral', alpha=0.8)
    
    ax.set_xlabel('Configuracion')
    ax.set_ylabel('Resistividad ρ [×10⁻⁸ Ω·m]')
    ax.set_title('Comparacion de resistividades obtenidas experimentalmente')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(configuraciones)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores sobre las barras
    for i, (bar, val) in enumerate(zip(bars1, valores_fase1)):
        if val is not None:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9)
    
    for i, (bar, val) in enumerate(zip(bars2, valores_fase2)):
        if val is not None:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('graficas/comparacion_resistividades.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: graficas/comparacion_resistividades.png")

def grafica_R_vs_L():
    """Grafica R vs L para visualizar la dependencia lineal"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Constantan 0.4mm
    L = constantan_04_directa['L_cm'] * 1e-2
    R = constantan_04_directa['R']
    slope, intercept, r2, _ = ajuste_lineal(L, R)
    L_fit = np.linspace(0, L.max() * 1.1, 100)
    R_fit = slope * L_fit + intercept
    ax1.plot(L, R, 'bo', markersize=6, label='Datos')
    ax1.plot(L_fit, R_fit, 'r-', linewidth=2, label=f'Ajuste (R²={r2:.4f})')
    ax1.set_xlabel('Longitud L [m]')
    ax1.set_ylabel('Resistencia R [Ω]')
    ax1.set_title('Constantan 0.4mm')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Constantan 0.35mm
    L = constantan_035_directa['L_cm'] * 1e-2
    R = constantan_035_directa['R']
    slope, intercept, r2, _ = ajuste_lineal(L, R)
    L_fit = np.linspace(0, L.max() * 1.1, 100)
    R_fit = slope * L_fit + intercept
    ax2.plot(L, R, 'go', markersize=6, label='Datos')
    ax2.plot(L_fit, R_fit, 'r-', linewidth=2, label=f'Ajuste (R²={r2:.4f})')
    ax2.set_xlabel('Longitud L [m]')
    ax2.set_ylabel('Resistencia R [Ω]')
    ax2.set_title('Constantan 0.35mm')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Cromo-Niquel 0.4mm
    L = cromoniquel_04_directa['L_cm'] * 1e-2
    R = cromoniquel_04_directa['R']
    slope, intercept, r2, _ = ajuste_lineal(L, R)
    L_fit = np.linspace(0, L.max() * 1.1, 100)
    R_fit = slope * L_fit + intercept
    ax3.plot(L, R, 'mo', markersize=6, label='Datos')
    ax3.plot(L_fit, R_fit, 'r-', linewidth=2, label=f'Ajuste (R²={r2:.4f})')
    ax3.set_xlabel('Longitud L [m]')
    ax3.set_ylabel('Resistencia R [Ω]')
    ax3.set_title('Cromo-Niquel 0.4mm')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Cromo-Niquel 0.35mm
    L = cromoniquel_035_directa['L_cm'] * 1e-2
    R = cromoniquel_035_directa['R']
    slope, intercept, r2, _ = ajuste_lineal(L, R)
    L_fit = np.linspace(0, L.max() * 1.1, 100)
    R_fit = slope * L_fit + intercept
    ax4.plot(L, R, 'co', markersize=6, label='Datos')
    ax4.plot(L_fit, R_fit, 'r-', linewidth=2, label=f'Ajuste (R²={r2:.4f})')
    ax4.set_xlabel('Longitud L [m]')
    ax4.set_ylabel('Resistencia R [Ω]')
    ax4.set_title('Cromo-Niquel 0.35mm')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('graficas/R_vs_L.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Grafica guardada: graficas/R_vs_L.png")

def crear_carpeta_graficas():
    """Crear carpeta graficas si no existe"""
    graficas_dir = Path('graficas')
    graficas_dir.mkdir(exist_ok=True)
    return graficas_dir

def resumen_estadistico(rho_values):
    """Imprimir resumen estadistico"""
    print("\n" + "="*60)
    print("RESUMEN ESTADISTICO - VALORES DE RESISTIVIDAD")
    print("="*60)
    print(f"Valor teorico Constantan: rho = {rho_constantan_teorico*1e8:.2f}x10^-8 ohm-m")
    print(f"Valor teorico Cromo-Niquel: rho = {rho_cromoniquel_teorico*1e8:.2f}x10^-8 ohm-m")
    print()
    
    # Mostrar resultados
    print("FASE 1 - Medicion directa:")
    for key, (rho, r2) in rho_values.items():
        if 'fase1' in key and rho:
            if 'constantan' in key:
                error = abs(rho - rho_constantan_teorico) / rho_constantan_teorico * 100
                material = "Constantan"
            else:
                error = abs(rho - rho_cromoniquel_teorico) / rho_cromoniquel_teorico * 100
                material = "Cromo-Niquel"
            diam = "0.4mm" if "04" in key else "0.35mm"
            print(f"  {material} {diam}: rho = {rho*1e8:.2f}x10^-8 ohm-m, Error: {error:.1f}%, R2: {r2:.4f}")
    
    print()
    print("FASE 2 - Ley de Ohm:")
    for key, (rho, r2) in rho_values.items():
        if 'fase2' in key and rho:
            error = abs(rho - rho_cromoniquel_teorico) / rho_cromoniquel_teorico * 100
            diam = "0.4mm" if "04" in key else "0.35mm"
            print(f"  Cromo-Niquel {diam}: rho = {rho*1e8:.2f}x10^-8 ohm-m, Error: {error:.1f}%, R2: {r2:.4f}")
    
    print("="*60)

def main():
    """Funcion principal"""
    print("Generando graficas para el analisis de resistividad...")
    print("="*60)
    
    graficas_dir = crear_carpeta_graficas()
    print(f"[OK] Carpeta de graficas creada: {graficas_dir}")
    
    try:
        # Generar graficas individuales Fase 1
        print("\nGenerando graficas Fase 1 (Medicion directa)...")
        rho_c04_1, r2_c04_1 = grafica_fase1_material(constantan_04_directa, 'Constantan')
        rho_c035_1, r2_c035_1 = grafica_fase1_material(constantan_035_directa, 'Constantan')
        rho_cn04_1, r2_cn04_1 = grafica_fase1_material(cromoniquel_04_directa, 'Cromo-Niquel')
        rho_cn035_1, r2_cn035_1 = grafica_fase1_material(cromoniquel_035_directa, 'Cromo-Niquel')
        
        # Generar graficas individuales Fase 2
        print("\nGenerando graficas Fase 2 (Ley de Ohm)...")
        rho_cn035_2, r2_cn035_2 = grafica_fase2_material(cromoniquel_035_ohm, 'Cromo-Niquel')
        
        # Guardar valores para comparacion
        rho_values = {
            'constantan_04_fase1': (rho_c04_1, r2_c04_1),
            'constantan_035_fase1': (rho_c035_1, r2_c035_1),
            'cromoniquel_04_fase1': (rho_cn04_1, r2_cn04_1),
            'cromoniquel_035_fase1': (rho_cn035_1, r2_cn035_1),
            'cromoniquel_035_fase2': (rho_cn035_2, r2_cn035_2)
        }
        
        # Generar graficas adicionales
        print("\nGenerando graficas adicionales...")
        grafica_R_vs_L()
        grafica_comparacion_resistividades(rho_values)
        resumen_estadistico(rho_values)
        
        print("\n" + "="*60)
        print("[OK] TODAS LAS GRAFICAS GENERADAS EXITOSAMENTE")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Error al generar graficas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
