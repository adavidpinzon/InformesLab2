#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de gráficas para el análisis de transformadores
Taller 3: Estudio de diferentes configuraciones de transformadores
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Configuración de matplotlib para español
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.titlesize'] = 16

# Datos experimentales
# Transformador elevador (Ns=500, Np=250)
elevador_data = {
    'Vs': [4.786, 12.37, 19.60, 26.18, 39.42],
    'Vp': [2.578, 6.53, 10.24, 13.62, 20.38],
    'k_teorico': 2.0,
    'etiqueta': 'Elevador (Ns=500, Np=250)'
}

# Transformador reductor (Ns=250, Np=500)  
reductor_data = {
    'Vs': [6.69, 10.43, 17.26, 21.96, 28.40],
    'Vp': [14.00, 21.62, 35.46, 44.86, 57.96],
    'k_teorico': 0.5,
    'etiqueta': 'Reductor (Ns=250, Np=500)'
}

# Datos de potencia (configuración reductora)
potencia_data = {
    'casos': ['3 Lámparas\nen serie', '2 Lámparas\nen serie', '1 Lámpara', 
              '2 Lámparas\nen paralelo', '3 Lámparas\nen paralelo'],
    'Vp': [60.00, 60.00, 60.00, 60.00, 60.39],
    'Ip': [0.117, 0.119, 0.163, 0.239, 0.416],
    'Pp': [7.02, 7.14, 9.78, 14.34, 25.12],
    'Vs': [29.20, 29.08, 28.90, 28.38, 26.50],
    'Is': [0.135, 0.140, 0.235, 0.390, 0.796],
    'Ps': [3.94, 4.07, 6.79, 11.08, 21.09]
}

def crear_carpeta_graficas():
    """Crear carpeta graficas si no existe"""
    graficas_dir = Path('graficas')
    graficas_dir.mkdir(exist_ok=True)
    return graficas_dir

def grafica_relacion_voltajes():
    """Gráfica 1: Relación Vs/Vp vs Vp para elevador y reductor"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Elevador
    k_elevador = np.array(elevador_data['Vs']) / np.array(elevador_data['Vp'])
    ax1.plot(elevador_data['Vp'], k_elevador, 'bo-', linewidth=2, markersize=8, label='Datos experimentales')
    ax1.axhline(y=elevador_data['k_teorico'], color='r', linestyle='--', linewidth=2, label=f'Teórico k={elevador_data["k_teorico"]}')
    ax1.set_xlabel('Voltaje primario Vp [V]')
    ax1.set_ylabel('Relación k = Vs/Vp')
    ax1.set_title('Transformador Elevador\n(Ns=500, Np=250)')
    ax1.set_xlim(0, 25)  # Fijar límites del eje X
    ax1.set_ylim(1.8, 2.1)  # Fijar límites del eje Y
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Reductor
    k_reductor = np.array(reductor_data['Vs']) / np.array(reductor_data['Vp'])
    ax2.plot(reductor_data['Vp'], k_reductor, 'go-', linewidth=2, markersize=8, label='Datos experimentales')
    ax2.axhline(y=reductor_data['k_teorico'], color='r', linestyle='--', linewidth=2, label=f'Teórico k={reductor_data["k_teorico"]}')
    ax2.set_xlabel('Voltaje primario Vp [V]')
    ax2.set_ylabel('Relación k = Vs/Vp')
    ax2.set_title('Transformador Reductor\n(Ns=250, Np=500)')
    ax2.set_xlim(0, 65)  # Fijar límites del eje X
    ax2.set_ylim(0.47, 0.50)  # Fijar límites del eje Y
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('graficas/relacion_voltajes.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("[OK] Grafica guardada: graficas/relacion_voltajes.png")

def grafica_eficiencia_potencia():
    """Gráfica 2: Eficiencia y potencias por tipo de carga"""
    # Calcular eficiencia
    eficiencia = np.array(potencia_data['Ps']) / np.array(potencia_data['Pp']) * 100
    perdidas = np.array(potencia_data['Pp']) - np.array(potencia_data['Ps'])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Gráfica de potencias
    x_pos = np.arange(len(potencia_data['casos']))
    width = 0.35
    
    bars1 = ax1.bar(x_pos - width/2, potencia_data['Pp'], width, label='Potencia primario (Pp)', color='skyblue', alpha=0.8)
    bars2 = ax1.bar(x_pos + width/2, potencia_data['Ps'], width, label='Potencia secundario (Ps)', color='lightcoral', alpha=0.8)
    
    ax1.set_xlabel('Tipo de carga')
    ax1.set_ylabel('Potencia [W]')
    ax1.set_title('Potencias del Transformador por Tipo de Carga')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(potencia_data['casos'], rotation=15, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Agregar valores sobre las barras
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom')
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}', ha='center', va='bottom')
    
    # Gráfica de eficiencia
    bars3 = ax2.bar(x_pos, eficiencia, color='green', alpha=0.7, label='Eficiencia')
    ax2.set_xlabel('Tipo de carga')
    ax2.set_ylabel('Eficiencia [%]')
    ax2.set_title('Eficiencia del Transformador por Tipo de Carga')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(potencia_data['casos'], rotation=15, ha='right')
    ax2.grid(True, alpha=0.3)
    
    # Agregar valores sobre las barras
    for bar in bars3:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('graficas/eficiencia_potencia.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("[OK] Grafica guardada: graficas/eficiencia_potencia.png")

def grafica_vs_vp_comparacion():
    """Gráfica 3: Comparación directa Vs vs Vp para ambas configuraciones"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Líneas teóricas
    vp_range = np.linspace(0, 60, 100)
    vs_elevador_teorico = vp_range * elevador_data['k_teorico']
    vs_reductor_teorico = vp_range * reductor_data['k_teorico']
    
    # Datos experimentales
    ax.plot(elevador_data['Vp'], elevador_data['Vs'], 'bo', markersize=10, label='Elevador (experimental)')
    ax.plot(reductor_data['Vp'], reductor_data['Vs'], 'go', markersize=10, label='Reductor (experimental)')
    
    # Líneas teóricas
    ax.plot(vp_range, vs_elevador_teorico, 'b--', linewidth=2, alpha=0.7, label='Elevador (teórico k=2.0)')
    ax.plot(vp_range, vs_reductor_teorico, 'g--', linewidth=2, alpha=0.7, label='Reductor (teórico k=0.5)')
    
    ax.set_xlabel('Voltaje primario Vp [V]')
    ax.set_ylabel('Voltaje secundario Vs [V]')
    ax.set_title('Comparación de Relaciones de Transformación\nElevador vs Reductor')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Agregar línea de referencia y=x
    max_val = max(max(elevador_data['Vs']), max(reductor_data['Vp']))
    ax.plot([0, max_val], [0, max_val], 'k:', alpha=0.5, label='Vs = Vp (k=1)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('graficas/vs_vp_comparacion.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("[OK] Grafica guardada: graficas/vs_vp_comparacion.png")

def grafica_corriente_potencia():
    """Gráfica 4: Relación entre corriente y potencia"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Corriente vs Potencia en primario
    ax1.plot(potencia_data['Ip'], potencia_data['Pp'], 'ro-', linewidth=2, markersize=8)
    ax1.set_xlabel('Corriente primario Ip [A]')
    ax1.set_ylabel('Potencia primario Pp [W]')
    ax1.set_title('Potencia vs Corriente en Primario')
    ax1.grid(True, alpha=0.3)
    
    # Agregar etiquetas para cada punto
    for i, caso in enumerate(potencia_data['casos']):
        ax1.annotate(caso.replace('\n', ' '), 
                    (potencia_data['Ip'][i], potencia_data['Pp'][i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    # Corriente vs Potencia en secundario
    ax2.plot(potencia_data['Is'], potencia_data['Ps'], 'bo-', linewidth=2, markersize=8)
    ax2.set_xlabel('Corriente secundario Is [A]')
    ax2.set_ylabel('Potencia secundario Ps [W]')
    ax2.set_title('Potencia vs Corriente en Secundario')
    ax2.grid(True, alpha=0.3)
    
    # Agregar etiquetas para cada punto
    for i, caso in enumerate(potencia_data['casos']):
        ax2.annotate(caso.replace('\n', ' '), 
                    (potencia_data['Is'][i], potencia_data['Ps'][i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('graficas/corriente_potencia.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("[OK] Grafica guardada: graficas/corriente_potencia.png")

def resumen_estadistico():
    """Imprimir resumen estadístico de los datos"""
    print("\n" + "="*60)
    print("RESUMEN ESTADÍSTICO DE LOS DATOS")
    print("="*60)
    
    # Estadísticas elevador
    k_elevador = np.array(elevador_data['Vs']) / np.array(elevador_data['Vp'])
    print(f"\nTransformador Elevador:")
    print(f"  k promedio: {np.mean(k_elevador):.3f}")
    print(f"  k teórico: {elevador_data['k_teorico']:.3f}")
    print(f"  Error relativo: {abs(np.mean(k_elevador) - elevador_data['k_teorico'])/elevador_data['k_teorico']*100:.1f}%")
    print(f"  Desviación estándar: {np.std(k_elevador, ddof=1):.4f}")
    
    # Estadísticas reductor
    k_reductor = np.array(reductor_data['Vs']) / np.array(reductor_data['Vp'])
    print(f"\nTransformador Reductor:")
    print(f"  k promedio: {np.mean(k_reductor):.3f}")
    print(f"  k teórico: {reductor_data['k_teorico']:.3f}")
    print(f"  Error relativo: {abs(np.mean(k_reductor) - reductor_data['k_teorico'])/reductor_data['k_teorico']*100:.1f}%")
    print(f"  Desviación estándar: {np.std(k_reductor, ddof=1):.4f}")
    
    # Estadísticas de eficiencia
    eficiencia = np.array(potencia_data['Ps']) / np.array(potencia_data['Pp']) * 100
    print(f"\nEficiencia del Transformador:")
    print(f"  Eficiencia promedio: {np.mean(eficiencia):.1f}%")
    print(f"  Eficiencia máxima: {np.max(eficiencia):.1f}% ({potencia_data['casos'][np.argmax(eficiencia)]})")
    print(f"  Eficiencia mínima: {np.min(eficiencia):.1f}% ({potencia_data['casos'][np.argmin(eficiencia)]})")
    
    print("\n" + "="*60)

def main():
    """Función principal para generar todas las gráficas"""
    print("Generando gráficas para el análisis de transformadores...")
    print("="*60)
    
    # Crear carpeta de gráficas
    graficas_dir = crear_carpeta_graficas()
    print(f"[OK] Carpeta de graficas creada: {graficas_dir}")
    
    # Generar todas las gráficas
    try:
        grafica_relacion_voltajes()
        grafica_eficiencia_potencia()
        grafica_vs_vp_comparacion()
        grafica_corriente_potencia()
        
        # Mostrar resumen estadístico
        resumen_estadistico()
        
        print("\n" + "="*60)
        print("[OK] TODAS LAS GRAFICAS GENERADAS EXITOSAMENTE")
        print("  - graficas/relacion_voltajes.png")
        print("  - graficas/eficiencia_potencia.png")
        print("  - graficas/vs_vp_comparacion.png")
        print("  - graficas/corriente_potencia.png")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] Error al generar graficas: {e}")

if __name__ == "__main__":
    main()
