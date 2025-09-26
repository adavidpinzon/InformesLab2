# -*- coding: utf-8 -*-
"""
Analisis de Corriente vs Resistencia - Fase 2
Laboratorio de Ley de Ohm
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuracion de matplotlib para espanol
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Datos experimentales de la Fase 2 (Voltaje constante = 40V)
datos_fase2 = {
    'Corriente_medida_A': [0.660, 0.640, 0.620, 0.610, 0.600, 0.580, 0.560, 0.530, 0.510, 0.500],
    'Resistencia_Ohm': [60.0, 62.5, 64.0, 65.0, 67.0, 68.0, 70.0, 75.0, 77.5, 80.0]
}

# Crear DataFrame
df = pd.DataFrame(datos_fase2)

# Calcular corriente teórica usando I = V/R
voltaje_constante = 40.0  # V
df['Corriente_teorica_A'] = voltaje_constante / df['Resistencia_Ohm']

# Calcular error porcentual
df['Error_Porcentual'] = np.abs(df['Corriente_medida_A'] - df['Corriente_teorica_A']) / df['Corriente_teorica_A'] * 100

# Calcular estadísticas
corriente_promedio = df['Corriente_medida_A'].mean()
desviacion_std = df['Corriente_medida_A'].std()
incertidumbre = desviacion_std / np.sqrt(len(df))
error_promedio = df['Error_Porcentual'].mean()

print("=== ANÁLISIS CORRIENTE vs RESISTENCIA (FASE 2) ===")
print(f"Voltaje constante: {voltaje_constante} V")
print(f"Corriente promedio medida: {corriente_promedio:.3f} ± {incertidumbre:.3f} A")
print(f"Desviación estándar: {desviacion_std:.3f} A")
print(f"Error promedio: {error_promedio:.3f}%")
print()

# Regresión lineal I vs 1/R (verificación de la Ley de Ohm)
df['Inverso_Resistencia'] = 1 / df['Resistencia_Ohm']
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Inverso_Resistencia'], df['Corriente_medida_A'])

print(f"Pendiente de la regresión I vs 1/R: {slope:.3f} A·Ω")
print(f"Valor esperado de la pendiente (V): {voltaje_constante:.1f} V")
print(f"Error en la pendiente: {abs(slope - voltaje_constante):.3f} V")
print(f"Coeficiente de correlación (R²): {r_value**2:.4f}")
print()

# Crear gráfica I vs R
plt.figure(figsize=(10, 6))
plt.scatter(df['Resistencia_Ohm'], df['Corriente_medida_A'], color='blue', s=50, alpha=0.7, 
           label='Corriente medida')
plt.scatter(df['Resistencia_Ohm'], df['Corriente_teorica_A'], color='red', s=50, alpha=0.7, 
           label='Corriente teórica (I = V/R)')

# Línea teórica
resistencia_teorica = np.linspace(df['Resistencia_Ohm'].min(), df['Resistencia_Ohm'].max(), 100)
corriente_teorica = voltaje_constante / resistencia_teorica
plt.plot(resistencia_teorica, corriente_teorica, 'r--', linewidth=2, 
         label=f'Ley de Ohm: I = {voltaje_constante}/R')

plt.xlabel('Resistencia (Ω)', fontsize=12)
plt.ylabel('Corriente (A)', fontsize=12)
plt.title('Corriente vs Resistencia - Voltaje Constante (40V)\nVerificación de la Ley de Ohm', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Guardar gráfica
plt.savefig('../graficas/corriente_vs_resistencia.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear gráfica I vs 1/R (debería ser lineal)
plt.figure(figsize=(10, 6))
plt.scatter(df['Inverso_Resistencia'], df['Corriente_medida_A'], color='blue', s=50, alpha=0.7, 
           label='Datos experimentales')

# Línea de regresión
inverso_r_teorico = np.linspace(df['Inverso_Resistencia'].min(), df['Inverso_Resistencia'].max(), 100)
corriente_regresion = slope * inverso_r_teorico + intercept
plt.plot(inverso_r_teorico, corriente_regresion, 'r--', linewidth=2, 
         label=f'Regresión: I = {slope:.2f}(1/R) + {intercept:.3f}')

plt.xlabel('1/Resistencia (1/Ω)', fontsize=12)
plt.ylabel('Corriente (A)', fontsize=12)
plt.title('Corriente vs 1/Resistencia\nVerificación de la relación I = V/R', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Guardar gráfica
plt.savefig('../graficas/corriente_vs_inverso_resistencia.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear gráfica de error porcentual
plt.figure(figsize=(10, 6))
plt.scatter(df['Resistencia_Ohm'], df['Error_Porcentual'], color='green', s=50, alpha=0.7)
plt.axhline(y=error_promedio, color='red', linestyle='--', linewidth=2, 
           label=f'Error promedio: {error_promedio:.2f}%')

plt.xlabel('Resistencia (Ω)', fontsize=12)
plt.ylabel('Error Porcentual (%)', fontsize=12)
plt.title('Error Porcentual vs Resistencia\nComparación entre corriente medida y teórica', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Guardar gráfica
plt.savefig('../graficas/error_porcentual_vs_resistencia.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear tabla de resultados
print("=== TABLA DE RESULTADOS DETALLADOS ===")
df_display = df.copy()
df_display['Inverso_Resistencia'] = df_display['Inverso_Resistencia'].round(4)
df_display['Error_Porcentual'] = df_display['Error_Porcentual'].round(2)
print(df_display.round(3).to_string(index=False))

print(f"\n=== VERIFICACIÓN DE LA LEY DE OHM ===")
print(f"La relación I = V/R se verifica con V = {voltaje_constante} V")
print(f"La pendiente de la regresión I vs 1/R es {slope:.3f} A·Ω (esperado: {voltaje_constante} V)")
print(f"El error en la pendiente es {abs(slope - voltaje_constante):.3f} V")
print(f"El coeficiente de correlación R² = {r_value**2:.4f} confirma la relación lineal")
