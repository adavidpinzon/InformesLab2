#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

# Datos del Montaje 3: Disco-Barra (del documento main.tex)
disco_barra_izq = {
    'arco1': {'coords': [(-5,0), (-6,0), (-7,3), (-8,4), (-6,-2)], 'voltajes': [-0.8, -0.9, -0.91, -0.92, -0.95]},
    'arco2': {'coords': [(-3,0), (-4,-2), (-6,-4), (-8,-5), (-6,-4)], 'voltajes': [-0.51, -0.62, -0.71, -0.74, -0.6]}
}

disco_barra_der = {
    'recta1': {'coords': [(4,0), (4,2), (4,4), (4,-3), (4,-4)], 'voltajes': [0.29, 0.25, 0.22, 0.13, 0.18]},
    'recta2': {'coords': [(2,0), (2,2), (2,4), (2,-2), (2,-4)], 'voltajes': [0.11, 0.29, 0.35, 0.35, 0.38]}
}

def crear_mapeo_disco_barra():
    os.makedirs('Taller_1/graficas', exist_ok=True)

    fig, ax = plt.subplots(figsize=(15, 10))

    # Electrodos: disco (izq) y barra (der)
    disco_izq = Circle((-6, 0), 1, color='red', alpha=0.7, label='Electrodo Disco (izq)')
    ax.add_patch(disco_izq)
    barra_der = Rectangle((5.5, -1), 1, 2, color='blue', alpha=0.7, label='Electrodo Barra (der)')
    ax.add_patch(barra_der)

    # Lado izquierdo (arcos)
    for clave, datos in disco_barra_izq.items():
        coords = np.array(datos['coords'])
        voltajes = np.array(datos['voltajes'])
        sc = ax.scatter(coords[:,0], coords[:,1], c=voltajes, cmap='RdBu_r', s=100, alpha=0.85,
                        edgecolors='black', linewidth=0.8)
        for (x,y), v in zip(coords, voltajes):
            ax.annotate(f'{v:.2f}V', (x,y), xytext=(5,5), textcoords='offset points', fontsize=9)

    # Lado derecho (rectas)
    for clave, datos in disco_barra_der.items():
        coords = np.array(datos['coords'])
        voltajes = np.array(datos['voltajes'])
        sc = ax.scatter(coords[:,0], coords[:,1], c=voltajes, cmap='RdBu_r', s=100, alpha=0.85,
                        edgecolors='black', linewidth=0.8)
        for (x,y), v in zip(coords, voltajes):
            ax.annotate(f'{v:.2f}V', (x,y), xytext=(5,5), textcoords='offset points', fontsize=9)

    ax.set_xlabel('Coordenada X (cm)')
    ax.set_ylabel('Coordenada Y (cm)')
    ax.set_title('Mapeo de Superficies Equipotenciales: Configuración Disco-Barra')
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-8, 8)
    ax.grid(True, alpha=0.3)
    cbar = plt.colorbar(sc, ax=ax, shrink=0.8, aspect=20)
    cbar.set_label('Potencial (V)')
    ax.legend(loc='upper right')

    out_path = 'Taller_1/graficas/mapeo_disco_barra.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✓ Guardado {out_path}")

if __name__ == '__main__':
    crear_mapeo_disco_barra()
