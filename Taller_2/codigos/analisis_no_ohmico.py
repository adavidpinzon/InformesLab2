"""
Análisis de Material No Óhmico - Fase 3
Laboratorio de Ley de Ohm
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuración de matplotlib para español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Datos experimentales de la Fase 3 (Material no óhmico - Bombillo incandescente)
datos_fase3 = {
    'Voltaje_V': [45, 50, 55, 60, 65, 75, 80, 85, 90, 95],
    'Corriente_A': [0.55, 0.58, 0.61, 0.67, 0.66, 0.713, 0.74, 0.76, 0.79, 0.80],
    'Resistencia_medida_Ohm': [81, 86, 90, 89, 98, 105, 108, 111, 113, 118]
}

# Crear DataFrame
df = pd.DataFrame(datos_fase3)

# Calcular resistencia según Ley de Ohm clásica
df['Resistencia_Ohm_clasica'] = df['Voltaje_V'] / df['Corriente_A']

# Calcular diferencia entre resistencia medida y calculada
df['Diferencia_Resistencia'] = np.abs(df['Resistencia_medida_Ohm'] - df['Resistencia_Ohm_clasica'])
df['Error_Porcentual'] = df['Diferencia_Resistencia'] / df['Resistencia_Ohm_clasica'] * 100

# Calcular estadísticas
resistencia_promedio_medida = df['Resistencia_medida_Ohm'].mean()
resistencia_promedio_calculada = df['Resistencia_Ohm_clasica'].mean()
error_promedio = df['Error_Porcentual'].mean()

print("=== ANÁLISIS DE MATERIAL NO ÓHMICO (FASE 3) ===")
print("Bombillo incandescente")
print(f"Resistencia promedio medida: {resistencia_promedio_medida:.1f} Ω")
print(f"Resistencia promedio calculada (V/I): {resistencia_promedio_calculada:.1f} Ω")
print(f"Error promedio: {error_promedio:.1f}%")
print()

# Análisis de la relación V vs I
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Corriente_A'], df['Voltaje_V'])
resistencia_aparente = slope

print(f"Resistencia aparente (pendiente V vs I): {resistencia_aparente:.1f} Ω")
print(f"Coeficiente de correlación (R²): {r_value**2:.4f}")
print()

# Crear gráfica V vs I (comportamiento no lineal)
plt.figure(figsize=(12, 8))

# Subplot 1: V vs I
plt.subplot(2, 2, 1)
plt.scatter(df['Corriente_A'], df['Voltaje_V'], color='red', s=50, alpha=0.7, label='Datos experimentales')

# Línea de regresión lineal
corriente_teorica = np.linspace(df['Corriente_A'].min(), df['Corriente_A'].max(), 100)
voltaje_regresion = slope * corriente_teorica + intercept
plt.plot(corriente_teorica, voltaje_regresion, 'b--', linewidth=2, 
         label=f'Regresión lineal: V = {slope:.1f}I + {intercept:.1f}')

plt.xlabel('Corriente (A)', fontsize=10)
plt.ylabel('Voltaje (V)', fontsize=10)
plt.title('Voltaje vs Corriente - Material No Óhmico', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

# Subplot 2: Resistencia vs Voltaje
plt.subplot(2, 2, 2)
plt.scatter(df['Voltaje_V'], df['Resistencia_medida_Ohm'], color='green', s=50, alpha=0.7, 
           label='Resistencia medida')
plt.scatter(df['Voltaje_V'], df['Resistencia_Ohm_clasica'], color='blue', s=50, alpha=0.7, 
           label='Resistencia calculada (V/I)')

plt.xlabel('Voltaje (V)', fontsize=10)
plt.ylabel('Resistencia (Ω)', fontsize=10)
plt.title('Resistencia vs Voltaje', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

# Subplot 3: Resistencia vs Corriente
plt.subplot(2, 2, 3)
plt.scatter(df['Corriente_A'], df['Resistencia_medida_Ohm'], color='green', s=50, alpha=0.7, 
           label='Resistencia medida')
plt.scatter(df['Corriente_A'], df['Resistencia_Ohm_clasica'], color='blue', s=50, alpha=0.7, 
           label='Resistencia calculada (V/I)')

plt.xlabel('Corriente (A)', fontsize=10)
plt.ylabel('Resistencia (Ω)', fontsize=10)
plt.title('Resistencia vs Corriente', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

# Subplot 4: Error porcentual vs Voltaje
plt.subplot(2, 2, 4)
plt.scatter(df['Voltaje_V'], df['Error_Porcentual'], color='orange', s=50, alpha=0.7)
plt.axhline(y=error_promedio, color='red', linestyle='--', linewidth=2, 
           label=f'Error promedio: {error_promedio:.1f}%')

plt.xlabel('Voltaje (V)', fontsize=10)
plt.ylabel('Error Porcentual (%)', fontsize=10)
plt.title('Error vs Voltaje', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig('../graficas/analisis_material_no_ohmico.png', dpi=300, bbox_inches='tight')
plt.show()

# Crear gráfica comparativa con material óhmico
plt.figure(figsize=(12, 6))

# Simular comportamiento óhmico para comparación
resistencia_ohmica = 60  # Ω
corriente_ohmica = np.linspace(0.1, 1.0, 100)
voltaje_ohmico = resistencia_ohmica * corriente_ohmica

plt.plot(corriente_ohmica, voltaje_ohmico, 'b-', linewidth=2, label='Material óhmico (R = 60 Ω)')
plt.scatter(df['Corriente_A'], df['Voltaje_V'], color='red', s=50, alpha=0.7, 
           label='Material no óhmico (bombillo)')

plt.xlabel('Corriente (A)', fontsize=12)
plt.ylabel('Voltaje (V)', fontsize=12)
plt.title('Comparación: Material Óhmico vs No Óhmico', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig('../graficas/comparacion_ohmico_vs_no_ohmico.png', dpi=300, bbox_inches='tight')
plt.show()

# Análisis de la no linealidad
print("=== ANÁLISIS DE NO LINEALIDAD ===")
# Calcular la desviación de la linealidad
voltaje_teorico_lineal = slope * df['Corriente_A'] + intercept
desviacion_lineal = np.abs(df['Voltaje_V'] - voltaje_teorico_lineal)
desviacion_promedio = desviacion_lineal.mean()
desviacion_maxima = desviacion_lineal.max()

print(f"Desviación promedio de la linealidad: {desviacion_promedio:.2f} V")
print(f"Desviación máxima de la linealidad: {desviacion_maxima:.2f} V")
print(f"Porcentaje de desviación promedio: {desviacion_promedio/df['Voltaje_V'].mean()*100:.1f}%")

# Crear tabla de resultados
print("\n=== TABLA DE RESULTADOS DETALLADOS ===")
df_display = df.copy()
df_display['Error_Porcentual'] = df_display['Error_Porcentual'].round(1)
print(df_display.round(2).to_string(index=False))

print(f"\n=== CONCLUSIONES DEL MATERIAL NO ÓHMICO ===")
print(f"1. El bombillo incandescente NO sigue la Ley de Ohm")
print(f"2. La resistencia varía con el voltaje aplicado")
print(f"3. El coeficiente de correlación R² = {r_value**2:.4f} indica desviación de la linealidad")
print(f"4. El error promedio de {error_promedio:.1f}% confirma el comportamiento no óhmico")
print(f"5. La resistencia aumenta con el voltaje, típico de dispositivos con dependencia térmica")
