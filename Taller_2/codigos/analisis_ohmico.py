"""
Análisis de Material Óhmico - Fase 1
Laboratorio de Ley de Ohm
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuración de matplotlib para español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Datos experimentales de la Fase 1 (Material óhmico)
# Resistencia nominal: 60 Ω
datos_fase1 = {
    'Voltaje_V': [7.41, 11.86, 17.84, 21.57, 27.02, 32.15, 40.60, 46.31, 51.02, 55.34],
    'Corriente_A': [0.120, 0.190, 0.290, 0.350, 0.440, 0.530, 0.672, 0.761, 0.824, 0.918]
}

# Crear DataFrame
df = pd.DataFrame(datos_fase1)

# Calcular resistencia experimental para cada punto
df['Resistencia_Ohm'] = df['Voltaje_V'] / df['Corriente_A']

# Calcular estadísticas
resistencia_nominal = 60.0  # Ω
resistencia_promedio = df['Resistencia_Ohm'].mean()
desviacion_std = df['Resistencia_Ohm'].std()
incertidumbre = desviacion_std / np.sqrt(len(df))

# Calcular porcentaje de error
df['Error_Porcentual'] = np.abs(df['Resistencia_Ohm'] - resistencia_nominal) / resistencia_nominal * 100
error_promedio = df['Error_Porcentual'].mean()

print("=== ANÁLISIS DE MATERIAL ÓHMICO (FASE 1) ===")
print(f"Resistencia nominal: {resistencia_nominal} Ω")
print(f"Resistencia promedio experimental: {resistencia_promedio:.2f} ± {incertidumbre:.2f} Ω")
print(f"Desviación estándar: {desviacion_std:.2f} Ω")
print(f"Error promedio: {error_promedio:.2f}%")
print()

# Regresión lineal V vs I
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Corriente_A'], df['Voltaje_V'])
resistencia_regresion = slope
print(f"Resistencia por regresión lineal: {resistencia_regresion:.2f} Ω")
print(f"Coeficiente de correlación (R²): {r_value**2:.4f}")
print()

# Crear gráfica V vs I
plt.figure(figsize=(10, 6))
plt.scatter(df['Corriente_A'], df['Voltaje_V'], color='blue', s=50, alpha=0.7, label='Datos experimentales')

# Línea de regresión
corriente_teorica = np.linspace(df['Corriente_A'].min(), df['Corriente_A'].max(), 100)
voltaje_teorico = slope * corriente_teorica + intercept
plt.plot(corriente_teorica, voltaje_teorico, 'r--', linewidth=2, 
         label=f'Regresión lineal: V = {slope:.2f}I + {intercept:.2f}')

plt.xlabel('Corriente (A)', fontsize=12)
plt.ylabel('Voltaje (V)', fontsize=12)
plt.title('Relación Voltaje vs Corriente - Material Óhmico\n(Resistencia nominal: 60 Ω)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Guardar gráfica
plt.savefig('../graficas/voltaje_vs_corriente_ohmico.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear gráfica de resistencia vs punto de medición
plt.figure(figsize=(10, 6))
puntos = range(1, len(df) + 1)
plt.scatter(puntos, df['Resistencia_Ohm'], color='green', s=50, alpha=0.7, label='Resistencia experimental')
plt.axhline(y=resistencia_nominal, color='red', linestyle='--', linewidth=2, label=f'Resistencia nominal ({resistencia_nominal} Ω)')
plt.axhline(y=resistencia_promedio, color='blue', linestyle='-', linewidth=2, 
           label=f'Resistencia promedio ({resistencia_promedio:.2f} Ω)')

plt.xlabel('Punto de medición', fontsize=12)
plt.ylabel('Resistencia (Ω)', fontsize=12)
plt.title('Resistencia Experimental vs Punto de Medición\nMaterial Óhmico', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

# Guardar gráfica
plt.savefig('../graficas/resistencia_vs_punto_ohmico.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear tabla de resultados
print("=== TABLA DE RESULTADOS DETALLADOS ===")
print(df.round(3).to_string(index=False))

# Verificar la Ley de Ohm
print(f"\n=== VERIFICACIÓN DE LA LEY DE OHM ===")
print(f"La relación V = RI se cumple con R = {resistencia_promedio:.2f} ± {incertidumbre:.2f} Ω")
print(f"El coeficiente de correlación R² = {r_value**2:.4f} indica una relación lineal muy fuerte")
print(f"El error promedio de {error_promedio:.2f}% es aceptable para un material óhmico")
