# -*- coding: utf-8 -*-
"""
Crear todas las graficas del laboratorio
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Configuracion
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Datos
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

df1 = pd.DataFrame(datos_fase1)
df2 = pd.DataFrame(datos_fase2)
df3 = pd.DataFrame(datos_fase3)

# Grafica 1: V vs I Material Ohmico
print("Creando grafica 1...")
df1['Resistencia_Ohm'] = df1['Voltaje_V'] / df1['Corriente_A']
slope1, intercept1, r1, _, _ = stats.linregress(df1['Corriente_A'], df1['Voltaje_V'])

plt.figure(figsize=(10, 6))
plt.scatter(df1['Corriente_A'], df1['Voltaje_V'], color='blue', s=50, alpha=0.7, label='Datos experimentales')
corriente_teorica = np.linspace(df1['Corriente_A'].min(), df1['Corriente_A'].max(), 100)
voltaje_teorico = slope1 * corriente_teorica + intercept1
plt.plot(corriente_teorica, voltaje_teorico, 'r--', linewidth=2, 
         label=f'Regresion: V = {slope1:.2f}I + {intercept1:.2f}')
plt.xlabel('Corriente (A)')
plt.ylabel('Voltaje (V)')
plt.title('Voltaje vs Corriente - Material Ohmico')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('../graficas/voltaje_vs_corriente_ohmico.png', dpi=300, bbox_inches='tight')
plt.close()

# Grafica 2: I vs R
print("Creando grafica 2...")
voltaje_constante = 40.0
df2['Corriente_teorica_A'] = voltaje_constante / df2['Resistencia_Ohm']

plt.figure(figsize=(10, 6))
plt.scatter(df2['Resistencia_Ohm'], df2['Corriente_medida_A'], color='blue', s=50, alpha=0.7, 
           label='Corriente medida')
plt.scatter(df2['Resistencia_Ohm'], df2['Corriente_teorica_A'], color='red', s=50, alpha=0.7, 
           label='Corriente teorica')
resistencia_teorica = np.linspace(df2['Resistencia_Ohm'].min(), df2['Resistencia_Ohm'].max(), 100)
corriente_teorica = voltaje_constante / resistencia_teorica
plt.plot(resistencia_teorica, corriente_teorica, 'r--', linewidth=2, 
         label=f'I = {voltaje_constante}/R')
plt.xlabel('Resistencia (Ohm)')
plt.ylabel('Corriente (A)')
plt.title('Corriente vs Resistencia - V = 40V')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('../graficas/corriente_vs_resistencia.png', dpi=300, bbox_inches='tight')
plt.close()

# Grafica 3: V vs I Material No Ohmico
print("Creando grafica 3...")
df3['Resistencia_Ohm'] = df3['Voltaje_V'] / df3['Corriente_A']
slope3, intercept3, r3, _, _ = stats.linregress(df3['Corriente_A'], df3['Voltaje_V'])

plt.figure(figsize=(10, 6))
plt.scatter(df3['Corriente_A'], df3['Voltaje_V'], color='red', s=50, alpha=0.7, label='Datos experimentales')
corriente_teorica = np.linspace(df3['Corriente_A'].min(), df3['Corriente_A'].max(), 100)
voltaje_teorico = slope3 * corriente_teorica + intercept3
plt.plot(corriente_teorica, voltaje_teorico, 'b--', linewidth=2, 
         label=f'Regresion: V = {slope3:.1f}I + {intercept3:.1f}')
plt.xlabel('Corriente (A)')
plt.ylabel('Voltaje (V)')
plt.title('Voltaje vs Corriente - Material No Ohmico')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('../graficas/voltaje_vs_corriente_no_ohmico.png', dpi=300, bbox_inches='tight')
plt.close()

# Grafica 4: Comparacion
print("Creando grafica 4...")
plt.figure(figsize=(12, 6))
plt.scatter(df1['Corriente_A'], df1['Voltaje_V'], color='blue', s=50, alpha=0.7, 
           label='Material ohmico')
plt.scatter(df3['Corriente_A'], df3['Voltaje_V'], color='red', s=50, alpha=0.7, 
           label='Material no ohmico')
corriente_comp = np.linspace(0.1, 1.0, 100)
voltaje_ohmico = slope1 * corriente_comp + intercept1
voltaje_no_ohmico = slope3 * corriente_comp + intercept3
plt.plot(corriente_comp, voltaje_ohmico, 'b-', linewidth=2, alpha=0.7)
plt.plot(corriente_comp, voltaje_no_ohmico, 'r-', linewidth=2, alpha=0.7)
plt.xlabel('Corriente (A)')
plt.ylabel('Voltaje (V)')
plt.title('Comparacion: Ohmico vs No Ohmico')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('../graficas/comparacion_ohmico_vs_no_ohmico.png', dpi=300, bbox_inches='tight')
plt.close()

# Grafica 5: Resistencia vs Voltaje
print("Creando grafica 5...")
plt.figure(figsize=(12, 6))
voltaje_ohmico = np.linspace(0, 60, 100)
resistencia_constante = np.full_like(voltaje_ohmico, 60.0)
plt.plot(voltaje_ohmico, resistencia_constante, 'b-', linewidth=3, 
         label='Material ohmico (R = 60 Ohm)')
plt.scatter(df3['Voltaje_V'], df3['Resistencia_Ohm'], color='red', s=50, alpha=0.7, 
           label='Material no ohmico')
plt.xlabel('Voltaje (V)')
plt.ylabel('Resistencia (Ohm)')
plt.title('Resistencia vs Voltaje')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('../graficas/resistencia_vs_voltaje.png', dpi=300, bbox_inches='tight')
plt.close()

print("Todas las graficas creadas exitosamente!")
print(f"Resistencia promedio ohmico: {df1['Resistencia_Ohm'].mean():.2f} Ohm")
print(f"Resistencia promedio no ohmico: {df3['Resistencia_Ohm'].mean():.1f} Ohm")
print(f"R2 ohmico: {r1**2:.4f}")
print(f"R2 no ohmico: {r3**2:.4f}")
