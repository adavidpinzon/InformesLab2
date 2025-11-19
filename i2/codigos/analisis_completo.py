"""
Análisis Completo del Laboratorio de Ley de Ohm
Incluye todas las fases y comparaciones
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuración de matplotlib para español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Datos de todas las fases
datos_fase1 = {
    'Voltaje_V': [7.41, 11.86, 17.84, 21.57, 27.02, 32.15, 40.60, 46.31, 51.02, 55.34],
    'Corriente_A': [0.120, 0.190, 0.290, 0.350, 0.440, 0.530, 0.672, 0.761, 0.824, 0.918]
}

datos_fase2 = {
    'Corriente_medida_A': [0.660, 0.640, 0.620, 0.610, 0.600, 0.580, 0.560, 0.530, 0.510, 0.500],
    'Resistencia_Ohm': [60.0, 62.5, 64.0, 65.0, 67.0, 68.0, 70.0, 75.0, 77.5, 80.0]
}

datos_fase3 = {
    'Voltaje_V': [45, 50, 55, 60, 65, 75, 80, 85, 90, 95],
    'Corriente_A': [0.55, 0.58, 0.61, 0.67, 0.66, 0.713, 0.74, 0.76, 0.79, 0.80]
}

# Crear DataFrames
df1 = pd.DataFrame(datos_fase1)
df2 = pd.DataFrame(datos_fase2)
df3 = pd.DataFrame(datos_fase3)

# Análisis Fase 1
df1['Resistencia_Ohm'] = df1['Voltaje_V'] / df1['Corriente_A']
resistencia_nominal = 60.0
resistencia_promedio_f1 = df1['Resistencia_Ohm'].mean()
error_f1 = np.abs(df1['Resistencia_Ohm'] - resistencia_nominal) / resistencia_nominal * 100
error_promedio_f1 = error_f1.mean()

# Análisis Fase 2
voltaje_constante = 40.0
df2['Corriente_teorica_A'] = voltaje_constante / df2['Resistencia_Ohm']
error_f2 = np.abs(df2['Corriente_medida_A'] - df2['Corriente_teorica_A']) / df2['Corriente_teorica_A'] * 100
error_promedio_f2 = error_f2.mean()

# Análisis Fase 3
df3['Resistencia_Ohm'] = df3['Voltaje_V'] / df3['Corriente_A']
resistencia_promedio_f3 = df3['Resistencia_Ohm'].mean()

# Regresiones lineales
slope1, intercept1, r1, _, _ = stats.linregress(df1['Corriente_A'], df1['Voltaje_V'])
slope3, intercept3, r3, _, _ = stats.linregress(df3['Corriente_A'], df3['Voltaje_V'])

print("=== RESUMEN COMPLETO DEL LABORATORIO ===")
print(f"FASE 1 (Material óhmico):")
print(f"  - Resistencia promedio: {resistencia_promedio_f1:.2f} Ω (nominal: {resistencia_nominal} Ω)")
print(f"  - Error promedio: {error_promedio_f1:.2f}%")
print(f"  - R²: {r1**2:.4f}")
print()

print(f"FASE 2 (I vs R, V constante):")
print(f"  - Error promedio: {error_promedio_f2:.3f}%")
print()

print(f"FASE 3 (Material no óhmico):")
print(f"  - Resistencia promedio: {resistencia_promedio_f3:.1f} Ω")
print(f"  - R²: {r3**2:.4f}")
print()

# Crear gráfica comparativa completa
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Fase 1: V vs I (Material óhmico)
ax1.scatter(df1['Corriente_A'], df1['Voltaje_V'], color='blue', s=50, alpha=0.7, label='Datos experimentales')
corriente_teorica = np.linspace(df1['Corriente_A'].min(), df1['Corriente_A'].max(), 100)
voltaje_teorico = slope1 * corriente_teorica + intercept1
ax1.plot(corriente_teorica, voltaje_teorico, 'r--', linewidth=2, 
         label=f'Regresión: V = {slope1:.1f}I + {intercept1:.1f}')
ax1.set_xlabel('Corriente (A)')
ax1.set_ylabel('Voltaje (V)')
ax1.set_title('Fase 1: Material Óhmico\n(Resistencia nominal: 60 Ω)')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Fase 2: I vs R
ax2.scatter(df2['Resistencia_Ohm'], df2['Corriente_medida_A'], color='green', s=50, alpha=0.7, 
           label='Corriente medida')
ax2.scatter(df2['Resistencia_Ohm'], df2['Corriente_teorica_A'], color='red', s=50, alpha=0.7, 
           label='Corriente teórica')
resistencia_teorica = np.linspace(df2['Resistencia_Ohm'].min(), df2['Resistencia_Ohm'].max(), 100)
corriente_teorica = voltaje_constante / resistencia_teorica
ax2.plot(resistencia_teorica, corriente_teorica, 'r--', linewidth=2, 
         label=f'Ley de Ohm: I = {voltaje_constante}/R')
ax2.set_xlabel('Resistencia (Ω)')
ax2.set_ylabel('Corriente (A)')
ax2.set_title('Fase 2: I vs R (V = 40V)')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Fase 3: V vs I (Material no óhmico)
ax3.scatter(df3['Corriente_A'], df3['Voltaje_V'], color='red', s=50, alpha=0.7, label='Datos experimentales')
corriente_teorica = np.linspace(df3['Corriente_A'].min(), df3['Corriente_A'].max(), 100)
voltaje_teorico = slope3 * corriente_teorica + intercept3
ax3.plot(corriente_teorica, voltaje_teorico, 'b--', linewidth=2, 
         label=f'Regresión: V = {slope3:.1f}I + {intercept3:.1f}')
ax3.set_xlabel('Corriente (A)')
ax3.set_ylabel('Voltaje (V)')
ax3.set_title('Fase 3: Material No Óhmico\n(Bombillo incandescente)')
ax3.grid(True, alpha=0.3)
ax3.legend()

# Comparación directa V vs I
ax4.scatter(df1['Corriente_A'], df1['Voltaje_V'], color='blue', s=50, alpha=0.7, 
           label='Material óhmico')
ax4.scatter(df3['Corriente_A'], df3['Voltaje_V'], color='red', s=50, alpha=0.7, 
           label='Material no óhmico')

# Líneas de regresión
corriente_comp = np.linspace(0.1, 1.0, 100)
voltaje_ohmico = slope1 * corriente_comp + intercept1
voltaje_no_ohmico = slope3 * corriente_comp + intercept3
ax4.plot(corriente_comp, voltaje_ohmico, 'b-', linewidth=2, alpha=0.7)
ax4.plot(corriente_comp, voltaje_no_ohmico, 'r-', linewidth=2, alpha=0.7)

ax4.set_xlabel('Corriente (A)')
ax4.set_ylabel('Voltaje (V)')
ax4.set_title('Comparación: Óhmico vs No Óhmico')
ax4.grid(True, alpha=0.3)
ax4.legend()

plt.tight_layout()
plt.savefig('../graficas/analisis_completo_laboratorio.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear gráfica de resistencias vs voltaje
plt.figure(figsize=(12, 6))

# Resistencia constante para material óhmico
voltaje_ohmico = np.linspace(0, 60, 100)
resistencia_constante = np.full_like(voltaje_ohmico, resistencia_nominal)

plt.plot(voltaje_ohmico, resistencia_constante, 'b-', linewidth=3, 
         label=f'Material óhmico (R = {resistencia_nominal} Ω)')
plt.scatter(df3['Voltaje_V'], df3['Resistencia_Ohm'], color='red', s=50, alpha=0.7, 
           label='Material no óhmico (bombillo)')

plt.xlabel('Voltaje (V)', fontsize=12)
plt.ylabel('Resistencia (Ω)', fontsize=12)
plt.title('Comportamiento de la Resistencia vs Voltaje\nComparación entre Materiales Óhmicos y No Óhmicos', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig('../graficas/resistencia_vs_voltaje_comparacion.png', dpi=300, bbox_inches='tight')
plt.show()

print("=== VERIFICACIÓN DE LA LEY DE OHM ===")
print(f"✓ Fase 1: Material óhmico cumple V = RI con R = {resistencia_promedio_f1:.2f} Ω")
print(f"✓ Fase 2: Relación I = V/R se verifica con V = {voltaje_constante} V")
print(f"✗ Fase 3: Material no óhmico NO cumple la Ley de Ohm (R varía con V)")
print()
print("=== CONCLUSIONES PRINCIPALES ===")
print("1. Los materiales óhmicos siguen una relación lineal V = RI")
print("2. Los materiales no óhmicos presentan resistencia variable")
print("3. La Ley de Ohm es válida solo para ciertos materiales")
print("4. El bombillo incandescente muestra dependencia térmica de la resistencia")
