#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis de Superficies Equipotenciales - Gráficas para LaTeX

Este script genera las gráficas necesarias para la sección de Análisis de Resultados 
y Conclusiones del informe LaTeX sobre el estudio experimental de superficies equipotenciales.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Circle, Rectangle
import os

# Configurar estilo de las gráficas
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# Configurar para español
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def main():
    print("Generando gráficas para el análisis de superficies equipotenciales...")
    # Asegurar carpeta de salida
    output_dir = 'graficas'
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Datos del Experimento
    print("Organizando datos del experimento...")
    
    # Datos del Montaje 1: Disco-Disco
    disco_disco_izq = {
        'arco1': {'coords': [(-5,0), (-7,3), (-8,4), (-5,2), (-8,-4)], 'voltajes': [-0.17, -0.24, -0.19, -0.18, -0.22], 'promedio': -0.2, 'std': 0.03, 'incertidumbre': 0.01},
        'arco2': {'coords': [(-4,0), (-4,2), (-6,5), (-6,-3), (-8,-5)], 'voltajes': [-0.17, -0.16, -0.15, -0.17, -0.16], 'promedio': -0.16, 'std': 0.008, 'incertidumbre': 0.003},
        'arco3': {'coords': [(-3,0), (-4,3), (-6,6), (-8,7), (-4,-4)], 'voltajes': [-0.14, -0.17, -0.15, -0.13, -0.19], 'promedio': -0.15, 'std': 0.02, 'incertidumbre': 0.01}
    }

    disco_disco_der = {
        'arco1': {'coords': [(8,-4), (7,-3), (6,-2), (5,-1), (5,0)], 'voltajes': [0.5, 0.53, 0.52, 0.426, 0.44], 'promedio': 0.48, 'std': 0.04, 'incertidumbre': 0.02},
        'arco2': {'coords': [(4,0), (5,2), (6,3), (7,4), (5,-2)], 'voltajes': [0.28, 0.39, 0.43, 0.43, 0.534], 'promedio': 0.41, 'std': 0.09, 'incertidumbre': 0.04},
        'arco3': {'coords': [(3,0), (3,2), (4,3), (5,4), (6,5)], 'voltajes': [0.48, 0.43, 0.25, 0.31, 0.32], 'promedio': 0.35, 'std': 0.09, 'incertidumbre': 0.04}
    }

    # Datos del Montaje 2: Barra-Barra
    barra_barra_izq = {
        'recta1': {'coords': [(-3,0), (-3,2), (-3,4), (-3,-3), (-3,-4)], 'voltajes': [-0.36, -0.36, -0.38, -0.35, -0.34], 'promedio': -0.35, 'std': 0.01, 'incertidumbre': 0.006},
        'recta2': {'coords': [(-4,0), (-4,4), (-4,-2), (-4,-4), (-4,-5)], 'voltajes': [-0.42, -0.40, -0.40, -0.40, -0.38], 'promedio': -0.4, 'std': 0.01, 'incertidumbre': 0.006}
    }

    barra_barra_der = {
        'recta1': {'coords': [(3,0), (3,4), (3,-2), (3,-3), (3,-5)], 'voltajes': [0.3, 0.19, 0.22, 0.26, 0.18], 'promedio': 0.229, 'std': 0.04, 'incertidumbre': 0.02},
        'recta2': {'coords': [(4,0), (4,2), (4,4), (4,-2), (4,-4)], 'voltajes': [0.32, 0.44, 0.48, 0.62, 0.63], 'promedio': 0.49, 'std': 0.13, 'incertidumbre': 0.05}
    }

    # Datos del Montaje 3: Disco-Barra
    disco_barra_izq = {
        'arco1': {'coords': [(-5,0), (-6,0), (-7,3), (-8,4), (-6,-2)], 'voltajes': [-0.8, -0.9, -0.91, -0.92, -0.95], 'promedio': -0.89, 'std': 0.05, 'incertidumbre': 0.02},
        'arco2': {'coords': [(-3,0), (-4,-2), (-6,-4), (-8,-5), (-6,-4)], 'voltajes': [-0.51, -0.62, -0.71, -0.74, -0.6], 'promedio': -0.63, 'std': 0.09, 'incertidumbre': 0.04}
    }

    disco_barra_der = {
        'recta1': {'coords': [(4,0), (4,2), (4,4), (4,-3), (4,-4)], 'voltajes': [0.29, 0.25, 0.22, 0.13, 0.18], 'promedio': 0.21, 'std': 0.06, 'incertidumbre': 0.02},
        'recta2': {'coords': [(2,0), (2,2), (2,4), (2,-2), (2,-4)], 'voltajes': [0.11, 0.29, 0.35, 0.35, 0.38], 'promedio': 0.29, 'std': 0.1, 'incertidumbre': 0.04}
    }

    print("✓ Datos organizados correctamente")

    # 2. Gráfica 1: Comparación de Potenciales por Configuración
    print("Generando gráfica 1: Comparación de potenciales...")
    generar_comparacion_potenciales(disco_disco_izq, disco_disco_der, 
                                   barra_barra_izq, barra_barra_der,
                                   disco_barra_izq, disco_barra_der)

    # 3. Gráfica 2: Análisis de Incertidumbres
    print("Generando gráfica 2: Análisis de incertidumbres...")
    generar_analisis_incertidumbres(disco_disco_izq, disco_disco_der,
                                   barra_barra_izq, barra_barra_der,
                                   disco_barra_izq, disco_barra_der)

    # 4. Gráfica 3: Mapeo de Superficies Equipotenciales
    print("Generando gráfica 3: Mapeo de superficies equipotenciales...")
    generar_mapeo_equipotenciales(disco_disco_izq, disco_disco_der,
                                 barra_barra_izq, barra_barra_der,
                                 disco_barra_izq, disco_barra_der)

    # 5. Gráfica 4: Análisis de Campos Eléctricos
    print("Generando gráfica 4: Análisis de campos eléctricos...")
    generar_analisis_campos_electricos()

    # 6. Gráfica 5: Análisis de Precisión
    print("Generando gráfica 5: Análisis de precisión...")
    generar_analisis_precision(disco_disco_izq, disco_disco_der,
                              barra_barra_izq, barra_barra_der,
                              disco_barra_izq, disco_barra_der)

    print("\n✓ Todas las gráficas han sido generadas exitosamente!")
    verificar_archivos_generados()

def generar_comparacion_potenciales(disco_disco_izq, disco_disco_der, 
                                   barra_barra_izq, barra_barra_der,
                                   disco_barra_izq, disco_barra_der):
    """Genera la gráfica de comparación de potenciales por configuración"""
    
    configuraciones = ['Disco-Disco', 'Barra-Barra', 'Disco-Barra']
    
    # Valores promedio de potencial para cada configuración
    valores_izq = [
        np.mean([disco_disco_izq['arco1']['promedio'], disco_disco_izq['arco2']['promedio'], disco_disco_izq['arco3']['promedio']]),
        np.mean([barra_barra_izq['recta1']['promedio'], barra_barra_izq['recta2']['promedio']]),
        np.mean([disco_barra_izq['arco1']['promedio'], disco_barra_izq['arco2']['promedio']])
    ]

    valores_der = [
        np.mean([disco_disco_der['arco1']['promedio'], disco_disco_der['arco2']['promedio'], disco_disco_der['arco3']['promedio']]),
        np.mean([barra_barra_der['recta1']['promedio'], barra_barra_der['recta2']['promedio']]),
        np.mean([disco_barra_der['recta1']['promedio'], disco_barra_der['recta2']['promedio']])
    ]

    # Crear gráfica de barras
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(configuraciones))
    width = 0.35

    bars1 = ax.bar(x - width/2, valores_izq, width, label='Lado Izquierdo', 
                    color='#2E86AB', alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, valores_der, width, label='Lado Derecho', 
                    color='#A23B72', alpha=0.8, edgecolor='black', linewidth=1)

    # Personalizar gráfica
    ax.set_xlabel('Configuración de Electrodos', fontweight='bold')
    ax.set_ylabel('Potencial Promedio (V)', fontweight='bold')
    ax.set_title('Comparación de Potenciales por Configuración de Electrodos', fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(configuraciones)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    # Agregar valores en las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join('graficas', 'comparacion_potenciales.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Gráfica 1 guardada como 'comparacion_potenciales.png'")

def generar_analisis_incertidumbres(disco_disco_izq, disco_disco_der,
                                   barra_barra_izq, barra_barra_der,
                                   disco_barra_izq, disco_barra_der):
    """Genera la gráfica de análisis de incertidumbres"""
    
    # Recopilar todas las incertidumbres
    incertidumbres = []
    etiquetas = []
    configs = []

    # Disco-Disco Izquierdo
    for arco, datos in disco_disco_izq.items():
        incertidumbres.append(datos['incertidumbre'])
        etiquetas.append(f'DD-Izq-{arco}')
        configs.append('Disco-Disco')

    # Disco-Disco Derecho
    for arco, datos in disco_disco_der.items():
        incertidumbres.append(datos['incertidumbre'])
        etiquetas.append(f'DD-Der-{arco}')
        configs.append('Disco-Disco')

    # Barra-Barra Izquierdo
    for recta, datos in barra_barra_izq.items():
        incertidumbres.append(datos['incertidumbre'])
        etiquetas.append(f'BB-Izq-{recta}')
        configs.append('Barra-Barra')

    # Barra-Barra Derecho
    for recta, datos in barra_barra_der.items():
        incertidumbres.append(datos['incertidumbre'])
        etiquetas.append(f'BB-Der-{recta}')
        configs.append('Barra-Barra')

    # Disco-Barra Izquierdo
    for arco, datos in disco_barra_izq.items():
        incertidumbres.append(datos['incertidumbre'])
        etiquetas.append(f'DB-Izq-{arco}')
        configs.append('Disco-Barra')

    # Disco-Barra Derecho
    for recta, datos in disco_barra_der.items():
        incertidumbres.append(datos['incertidumbre'])
        etiquetas.append(f'DB-Der-{recta}')
        configs.append('Disco-Barra')

    # Crear gráfica de incertidumbres
    fig, ax = plt.subplots(figsize=(16, 8))

    # Colores por configuración
    colores = {'Disco-Disco': '#2E86AB', 'Barra-Barra': '#A23B72', 'Disco-Barra': '#F18F01'}

    for i, (inc, config) in enumerate(zip(incertidumbres, configs)):
        color = colores[config]
        ax.bar(i, inc, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)

    ax.set_xlabel('Mediciones', fontweight='bold')
    ax.set_ylabel('Incertidumbre (V)', fontweight='bold')
    ax.set_title('Análisis de Incertidumbres por Configuración', fontweight='bold', pad=20)
    ax.set_xticks(range(len(etiquetas)))
    ax.set_xticklabels(etiquetas, rotation=45, ha='right')
    ax.grid(True, alpha=0.3)

    # Agregar leyenda de colores
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.7, label=config) 
                       for config, color in colores.items()]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join('graficas', 'analisis_incertidumbres.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Gráfica 2 guardada como 'analisis_incertidumbres.png'")

def generar_mapeo_equipotenciales(disco_disco_izq, disco_disco_der,
                                 barra_barra_izq, barra_barra_der,
                                 disco_barra_izq, disco_barra_der):
    """Genera los mapeos de superficies equipotenciales para cada configuración"""
    
    # Crear mapeo para Disco-Disco
    crear_mapeo_individual('Disco-Disco', disco_disco_izq, disco_disco_der, 
                          'Mapeo de Superficies Equipotenciales: Configuración Disco-Disco',
                          'mapeo_disco_disco.png')
    
    # Crear mapeo para Barra-Barra
    crear_mapeo_individual('Barra-Barra', barra_barra_izq, barra_barra_der, 
                          'Mapeo de Superficies Equipotenciales: Configuración Barra-Barra',
                          'mapeo_barra_barra.png')
    
    # Crear mapeo para Disco-Barra
    crear_mapeo_individual('Disco-Barra', disco_barra_izq, disco_barra_der, 
                          'Mapeo de Superficies Equipotenciales: Configuración Disco-Barra',
                          'mapeo_disco_barra.png')

def crear_mapeo_individual(configuracion, datos_izq, datos_der, titulo, nombre_archivo):
    """Crea un mapeo de superficies equipotenciales para una configuración específica"""
    
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Dibujar electrodos
    if 'Disco' in configuracion:
        # Electrodo izquierdo (disco)
        disco_izq = Circle((-6, 0), 1, color='red', alpha=0.7, label='Electrodo Izquierdo')
        ax.add_patch(disco_izq)
    else:
        # Electrodo izquierdo (barra)
        barra_izq = Rectangle((-6.5, -1), 1, 2, color='red', alpha=0.7, label='Electrodo Izquierdo')
        ax.add_patch(barra_izq)
    
    if 'Disco' in configuracion:
        # Electrodo derecho (disco)
        disco_der = Circle((6, 0), 1, color='blue', alpha=0.7, label='Electrodo Derecho')
        ax.add_patch(disco_der)
    else:
        # Electrodo derecho (barra)
        barra_der = Rectangle((5.5, -1), 1, 2, color='blue', alpha=0.7, label='Electrodo Derecho')
        ax.add_patch(barra_der)
    
    # Graficar puntos equipotenciales del lado izquierdo
    for i, (clave, datos) in enumerate(datos_izq.items()):
        coords = np.array(datos['coords'])
        voltajes = np.array(datos['voltajes'])
        
        scatter = ax.scatter(coords[:, 0], coords[:, 1], c=voltajes, 
                            cmap='RdBu_r', s=100, alpha=0.8, edgecolors='black', linewidth=1)
        
        # Agregar etiquetas de voltaje
        for j, (coord, volt) in enumerate(zip(coords, voltajes)):
            ax.annotate(f'{volt:.2f}V', (coord[0], coord[1]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8, fontweight='bold')
    
    # Graficar puntos equipotenciales del lado derecho
    for i, (clave, datos) in enumerate(datos_der.items()):
        coords = np.array(datos['coords'])
        voltajes = np.array(datos['voltajes'])
        
        scatter = ax.scatter(coords[:, 0], coords[:, 1], c=voltajes, 
                            cmap='RdBu_r', s=100, alpha=0.8, edgecolors='black', linewidth=1)
        
        # Agregar etiquetas de voltaje
        for j, (coord, volt) in enumerate(zip(coords, voltajes)):
            ax.annotate(f'{volt:.2f}V', (coord[0], coord[1]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8, fontweight='bold')
    
    # Configurar gráfica
    ax.set_xlabel('Coordenada X (cm)', fontweight='bold')
    ax.set_ylabel('Coordenada Y (cm)', fontweight='bold')
    ax.set_title(titulo, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-8, 8)
    
    # Agregar barra de color
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8, aspect=20)
    cbar.set_label('Potencial (V)', fontweight='bold')
    
    # Agregar leyenda
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join('graficas', f'{nombre_archivo}'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Gráfica 3 guardada como '{nombre_archivo}'")

def generar_analisis_campos_electricos():
    """Genera la gráfica de análisis de campos eléctricos"""
    
    # Campos eléctricos calculados del documento
    campos_disco_disco = {
        'Izquierdo': [-2.5, -2.025, -1.95],  # Arcos 1, 2, 3
        'Derecho': [6.03, 5.17, 4.47]        # Arcos 1, 2, 3
    }

    campos_barra_barra = {
        'Izquierdo': [-4.475, -5.0],          # Rectas 1, 2
        'Derecho': [2.87, 6.22]               # Rectas 1, 2
    }

    campos_disco_barra = {
        'Izquierdo': [-11.2, -7.95],          # Arcos 1, 2
        'Derecho': [2.67, 3.69]               # Rectas 1, 2
    }

    # Crear gráfica de campos eléctricos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Gráfica 1: Campos por configuración
    configuraciones = ['Disco-Disco', 'Barra-Barra', 'Disco-Barra']
    campos_izq = [np.mean(campos_disco_disco['Izquierdo']), 
                   np.mean(campos_barra_barra['Izquierdo']), 
                   np.mean(campos_disco_barra['Izquierdo'])]
    campos_der = [np.mean(campos_disco_disco['Derecho']), 
                   np.mean(campos_barra_barra['Derecho']), 
                   np.mean(campos_disco_barra['Derecho'])]

    x = np.arange(len(configuraciones))
    width = 0.35

    bars1 = ax1.bar(x - width/2, campos_izq, width, label='Lado Izquierdo', 
                     color='#2E86AB', alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax1.bar(x + width/2, campos_der, width, label='Lado Derecho', 
                     color='#A23B72', alpha=0.8, edgecolor='black', linewidth=1)

    ax1.set_xlabel('Configuración de Electrodos', fontweight='bold')
    ax1.set_ylabel('Campo Eléctrico Promedio (V/m)', fontweight='bold')
    ax1.set_title('Campos Eléctricos por Configuración', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(configuraciones)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Agregar valores en las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.1f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Gráfica 2: Distribución de campos por lado
    lados = ['Izquierdo', 'Derecho']
    campos_todos_izq = campos_disco_disco['Izquierdo'] + campos_barra_barra['Izquierdo'] + campos_disco_barra['Izquierdo']
    campos_todos_der = campos_disco_disco['Derecho'] + campos_barra_barra['Derecho'] + campos_disco_barra['Derecho']

    ax2.hist([campos_todos_izq, campos_todos_der], bins=8, alpha=0.7, 
              label=lados, color=['#2E86AB', '#A23B72'], edgecolor='black')
    ax2.set_xlabel('Campo Eléctrico (V/m)', fontweight='bold')
    ax2.set_ylabel('Frecuencia', fontweight='bold')
    ax2.set_title('Distribución de Campos Eléctricos por Lado', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join('graficas', 'analisis_campos_electricos.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Gráfica 4 guardada como 'analisis_campos_electricos.png'")

def generar_analisis_precision(disco_disco_izq, disco_disco_der,
                              barra_barra_izq, barra_barra_der,
                              disco_barra_izq, disco_barra_der):
    """Genera la gráfica de análisis de precisión y reproducibilidad"""
    
    # Recopilar todas las desviaciones estándar
    desviaciones = []
    etiquetas_desv = []
    configs_desv = []

    # Disco-Disco
    for arco, datos in disco_disco_izq.items():
        desviaciones.append(datos['std'])
        etiquetas_desv.append(f'DD-Izq-{arco}')
        configs_desv.append('Disco-Disco')

    for arco, datos in disco_disco_der.items():
        desviaciones.append(datos['std'])
        etiquetas_desv.append(f'DD-Der-{arco}')
        configs_desv.append('Disco-Disco')

    # Barra-Barra
    for recta, datos in barra_barra_izq.items():
        desviaciones.append(datos['std'])
        etiquetas_desv.append(f'BB-Izq-{recta}')
        configs_desv.append('Barra-Barra')

    for recta, datos in barra_barra_der.items():
        desviaciones.append(datos['std'])
        etiquetas_desv.append(f'BB-Der-{recta}')
        configs_desv.append('Barra-Barra')

    # Disco-Barra
    for arco, datos in disco_barra_izq.items():
        desviaciones.append(datos['std'])
        etiquetas_desv.append(f'DB-Izq-{arco}')
        configs_desv.append('Disco-Barra')

    for recta, datos in disco_barra_der.items():
        desviaciones.append(datos['std'])
        etiquetas_desv.append(f'DB-Der-{recta}')
        configs_desv.append('Disco-Barra')

    # Crear gráfica de desviaciones estándar
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Gráfica 1: Desviaciones estándar por medición
    colores_desv = {'Disco-Disco': '#2E86AB', 'Barra-Barra': '#A23B72', 'Disco-Barra': '#F18F01'}

    for i, (desv, config) in enumerate(zip(desviaciones, configs_desv)):
        color = colores_desv[config]
        ax1.bar(i, desv, color=color, alpha=0.7, edgecolor='black', linewidth=0.5)

    ax1.set_xlabel('Mediciones', fontweight='bold')
    ax1.set_ylabel('Desviación Estándar (V)', fontweight='bold')
    ax1.set_title('Análisis de Precisión: Desviaciones Estándar', fontweight='bold')
    ax1.set_xticks(range(len(etiquetas_desv)))
    ax1.set_xticklabels(etiquetas_desv, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)

    # Agregar línea de referencia para precisión aceptable
    precision_aceptable = 0.05  # 50 mV
    ax1.axhline(y=precision_aceptable, color='red', linestyle='--', alpha=0.7, 
                 label=f'Precisión Aceptable ({precision_aceptable} V)')
    ax1.legend()

    # Gráfica 2: Box plot de desviaciones por configuración
    desv_por_config = {}
    for config in ['Disco-Disco', 'Barra-Barra', 'Disco-Barra']:
        desv_por_config[config] = [desv for desv, conf in zip(desviaciones, configs_desv) if conf == config]

    ax2.boxplot(desv_por_config.values(), labels=desv_por_config.keys(), patch_artist=True)
    ax2.set_xlabel('Configuración de Electrodos', fontweight='bold')
    ax2.set_ylabel('Desviación Estándar (V)', fontweight='bold')
    ax2.set_title('Distribución de Precisión por Configuración', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join('graficas', 'analisis_precision.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ Gráfica 5 guardada como 'analisis_precision.png'")

def verificar_archivos_generados():
    """Verifica que todas las gráficas se generaron correctamente"""
    
    archivos_graficas = [
        'graficas/comparacion_potenciales.png',
        'graficas/analisis_incertidumbres.png',
        'graficas/mapeo_disco_disco.png',
        'graficas/mapeo_barra_barra.png',
        'graficas/mapeo_disco_barra.png',
        'graficas/analisis_campos_electricos.png',
        'graficas/analisis_precision.png'
    ]

    print("\nVerificación de archivos generados:")
    for archivo in archivos_graficas:
        if os.path.exists(f'{archivo}'):
            print(f"✓ {archivo} - Generado correctamente")
        else:
            print(f"✗ {archivo} - No encontrado")

    print("\nResumen de gráficas generadas para el documento LaTeX:")
    print("1. comparacion_potenciales.png - Comparación de potenciales por configuración")
    print("2. analisis_incertidumbres.png - Análisis de incertidumbres por medición")
    print("3. mapeo_disco_disco.png - Mapeo de superficies equipotenciales para disco-disco")
    print("4. mapeo_barra_barra.png - Mapeo de superficies equipotenciales para barra-barra")
    print("5. mapeo_disco_barra.png - Mapeo de superficies equipotenciales para disco-barra")
    print("6. analisis_campos_electricos.png - Análisis de campos eléctricos")
    print("7. analisis_precision.png - Análisis de precisión y reproducibilidad")
    print("\nEstas gráficas están listas para ser incluidas en el documento LaTeX en la sección de Análisis de Resultados y Conclusiones.")

if __name__ == "__main__":
    main()
