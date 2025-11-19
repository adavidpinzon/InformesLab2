# -*- coding: utf-8 -*-
"""
Generador de graficas para el laboratorio de Inducción Electromagnética y Ley de Faraday
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuracion de matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11

# Datos experimentales - Fase 1: Voltaje vs Velocidad
datos_fase1 = {
    'Altura_cm': [10, 20, 30, 40, 50],
    'Velocidad_ms': [1.40, 1.98, 2.43, 2.80, 3.13],
    'Voltaje_mV': [8.20, 12.30, 15.80, 18.50, 21.20]
}

# Datos experimentales - Fase 2: Voltaje vs Numero de espiras
datos_fase2 = {
    'Espiras': [200, 400, 600],
    'Voltaje_mV': [15.83, 31.25, 47.05],
    'Incertidumbre_mV': [0.10, 0.12, 0.13]
}

# Crear DataFrames
df1 = pd.DataFrame(datos_fase1)
df2 = pd.DataFrame(datos_fase2)

# GRAFICA 1: Voltaje vs Velocidad
slope1, intercept1, r1, p_value1, std_err1 = stats.linregress(df1['Velocidad_ms'], df1['Voltaje_mV'])
r2_1 = r1**2

plt.figure(figsize=(10, 6))
plt.scatter(df1['Velocidad_ms'], df1['Voltaje_mV'], color='blue', s=80, alpha=0.7, 
           label='Datos experimentales', zorder=3)

velocidad_teorica = np.linspace(df1['Velocidad_ms'].min(), df1['Velocidad_ms'].max(), 100)
voltaje_teorico = slope1 * velocidad_teorica + intercept1
plt.plot(velocidad_teorica, voltaje_teorico, 'r--', linewidth=2, 
         label=f'Regresión lineal: V = {slope1:.2f}v + {intercept1:.2f}\n($R^2$ = {r2_1:.4f})')

plt.xlabel('Velocidad del imán (m/s)', fontsize=12)
plt.ylabel('Voltaje inducido (mV)', fontsize=12)
plt.title('Voltaje Inducido vs Velocidad del Imán\nBobina 1 (N = 200 espiras)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='best', fontsize=10)
plt.tight_layout()
plt.savefig('graficas/voltaje_vs_velocidad.png', dpi=300, bbox_inches='tight')
plt.close()

# GRAFICA 2: Voltaje vs Numero de Espiras
slope2, intercept2, r2, p_value2, std_err2 = stats.linregress(df2['Espiras'], df2['Voltaje_mV'])
r2_2 = r2**2

plt.figure(figsize=(10, 6))
plt.errorbar(df2['Espiras'], df2['Voltaje_mV'], yerr=df2['Incertidumbre_mV'], 
            fmt='o', color='green', markersize=8, capsize=5, capthick=2,
            label='Datos experimentales', zorder=3, alpha=0.7)

espiras_teorica = np.linspace(df2['Espiras'].min(), df2['Espiras'].max(), 100)
voltaje_teorico2 = slope2 * espiras_teorica + intercept2
plt.plot(espiras_teorica, voltaje_teorico2, 'r--', linewidth=2, 
         label=f'Regresión lineal: V = {slope2:.4f}N + {intercept2:.2f}\n($R^2$ = {r2_2:.4f})')

plt.xlabel('Número de espiras', fontsize=12)
plt.ylabel('Voltaje inducido (mV)', fontsize=12)
plt.title('Voltaje Inducido vs Número de Espiras\n(h = 30 cm constante)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='best', fontsize=10)
plt.tight_layout()
plt.savefig('graficas/voltaje_vs_espiras.png', dpi=300, bbox_inches='tight')
plt.close()

# GRAFICA 3: Comparacion Teorica vs Experimental
# Valores teoricos estimados (usando modelo simplificado)
B_estimado = 0.2  # T (campo magnetico del iman)
A_bobina = np.pi * (0.015)**2  # m^2 (area de la bobina, radio 1.5 cm)
L_bobina = 0.05  # m (longitud de la bobina)
v_promedio = 2.43  # m/s (velocidad promedio)
dt_estimado = L_bobina / v_promedio  # s

# Calcular voltaje teorico para cada bobina
voltaje_teorico_200 = 200 * B_estimado * A_bobina / dt_estimado * 1000  # mV
voltaje_teorico_400 = 400 * B_estimado * A_bobina / dt_estimado * 1000  # mV
voltaje_teorico_600 = 600 * B_estimado * A_bobina / dt_estimado * 1000  # mV

voltajes_teoricos = [voltaje_teorico_200, voltaje_teorico_400, voltaje_teorico_600]

plt.figure(figsize=(10, 6))
x_pos = np.arange(len(df2['Espiras']))
width = 0.35

bars1 = plt.bar(x_pos - width/2, df2['Voltaje_mV'], width, yerr=df2['Incertidumbre_mV'],
                label='Experimental', color='blue', alpha=0.7, capsize=5)
bars2 = plt.bar(x_pos + width/2, voltajes_teoricos, width,
                label='Teórico (estimado)', color='red', alpha=0.7)

plt.xlabel('Número de espiras', fontsize=12)
plt.ylabel('Voltaje inducido (mV)', fontsize=12)
plt.title('Comparación: Valores Experimentales vs Teóricos\n(Estimación basada en Ley de Faraday)', 
          fontsize=14, fontweight='bold')
plt.xticks(x_pos, df2['Espiras'])
plt.legend(loc='best', fontsize=10)
plt.grid(True, alpha=0.3, linestyle='--', axis='y')
plt.tight_layout()
plt.savefig('graficas/comparacion_teorica_experimental.png', dpi=300, bbox_inches='tight')
plt.close()

# GRAFICA 4: Analisis de Incertidumbres
plt.figure(figsize=(12, 6))

# Subplot 1: Voltaje con barras de error (Fase 1)
plt.subplot(1, 2, 1)
incertidumbres_fase1 = [0.08, 0.10, 0.12, 0.14, 0.16]  # Valores estimados basados en desviaciones estándar
plt.errorbar(df1['Velocidad_ms'], df1['Voltaje_mV'], yerr=incertidumbres_fase1, 
            fmt='o', color='blue', markersize=8, capsize=5, capthick=2, 
            alpha=0.7, label='Datos con incertidumbre')
plt.xlabel('Velocidad del imán (m/s)', fontsize=11)
plt.ylabel('Voltaje inducido (mV)', fontsize=11)
plt.title('Voltaje Inducido con Barras de Error\n(Fase 1: Variación de velocidad)', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='best', fontsize=9)

# Subplot 2: Voltaje con barras de error (Fase 2)
plt.subplot(1, 2, 2)
plt.errorbar(df2['Espiras'], df2['Voltaje_mV'], yerr=df2['Incertidumbre_mV'], 
            fmt='s', color='green', markersize=8, capsize=5, capthick=2, 
            alpha=0.7, label='Datos con incertidumbre')
plt.xlabel('Número de espiras', fontsize=11)
plt.ylabel('Voltaje inducido (mV)', fontsize=11)
plt.title('Voltaje Inducido con Barras de Error\n(Fase 2: Variación de espiras)', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='best', fontsize=9)

plt.tight_layout()
plt.savefig('graficas/analisis_incertidumbres.png', dpi=300, bbox_inches='tight')
plt.close()

# GRAFICA 5: Relacion V/N constante
V_N_200 = df2['Voltaje_mV'].iloc[0] / df2['Espiras'].iloc[0]
V_N_400 = df2['Voltaje_mV'].iloc[1] / df2['Espiras'].iloc[1]
V_N_600 = df2['Voltaje_mV'].iloc[2] / df2['Espiras'].iloc[2]

V_N_promedio = np.mean([V_N_200, V_N_400, V_N_600])
V_N_std = np.std([V_N_200, V_N_400, V_N_600])

plt.figure(figsize=(10, 6))
plt.bar(['200 espiras', '400 espiras', '600 espiras'], 
        [V_N_200, V_N_400, V_N_600], 
        color=['blue', 'green', 'red'], alpha=0.7)
plt.axhline(y=V_N_promedio, color='black', linestyle='--', linewidth=2, 
           label=f'Promedio: {V_N_promedio:.4f} ± {V_N_std:.4f} mV/espira')
plt.xlabel('Configuración de bobina', fontsize=12)
plt.ylabel('V/N (mV/espira)', fontsize=12)
plt.title('Verificación de Proporcionalidad: V/N Constante\n(Confirma V ∝ N)', 
          fontsize=14, fontweight='bold')
plt.legend(loc='best', fontsize=10)
plt.grid(True, alpha=0.3, linestyle='--', axis='y')
plt.tight_layout()
plt.savefig('graficas/verificacion_proporcionalidad.png', dpi=300, bbox_inches='tight')
plt.close()

print("="*60)
print("Gráficas generadas exitosamente!")
print("="*60)
print(f"\nFase 1 - Voltaje vs Velocidad:")
print(f"  Pendiente: {slope1:.2f} ± {std_err1:.2f} mV·s/m")
print(f"  Coeficiente de determinación R²: {r2_1:.4f}")
print(f"\nFase 2 - Voltaje vs Espiras:")
print(f"  Pendiente: {slope2:.4f} ± {std_err2:.4f} mV/espira")
print(f"  Coeficiente de determinación R²: {r2_2:.4f}")
print(f"\nProporcionalidad V/N:")
print(f"  Valor promedio: {V_N_promedio:.4f} ± {V_N_std:.4f} mV/espira")
print("="*60)

