import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

def render_flat_shading(screen_vertices, camera_vertices, faces, width, height, ax):
    """
    Dibuja los polígonos sólidos en pantalla aplicando iluminación por software
    y ordenamiento de caras ocultas (Z-Buffer / Algoritmo del Pintor).
    """
    ax.clear() # Limpia el cuadro anterior para refrescar el renderizado
    
    if len(faces) == 0:
        return
        
    faces_np = np.array(faces, dtype=np.int32)
    
    # ==========================================================
    # 1. ALGORITMO DEL PINTOR (MANEJO DE CARAS OCULTAS)
    # Calcula la profundidad promedio en Z de los tres vértices que forman cada cara.
    # ==========================================================
    z_centers = np.mean(camera_vertices[faces_np, 2], axis=1)
    
    # Ordena de mayor a menor profundidad (de atrás hacia adelante).
    # Así, lo que está al frente dibuja encima y tapa físicamente el fondo.
    order = np.argsort(z_centers)
    faces_sorted = faces_np[order]
    
    # ==========================================================
    # 2. CÁLCULO DE ILUMINACIÓN SÓLIDA (FLAT SHADING)
    # Extrae vectores de las caras para calcular su vector normal geométrico.
    # ==========================================================
    p0_c = camera_vertices[faces_sorted[:, 0]]
    p1_c = camera_vertices[faces_sorted[:, 1]]
    p2_c = camera_vertices[faces_sorted[:, 2]]
    
    # Producto cruz para encontrar la normal de la superficie
    normales = np.cross(p1_c - p0_c, p2_c - p0_c)
    normas = np.linalg.norm(normales, axis=1, keepdims=True)
    normas[normas == 0] = 1.0  # Evita división entre cero en polígonos degenerados
    normales = normales / normas
    
    # Definición del vector de luz (proviene desde arriba y al frente del observador)
    luz = np.array([0.2, 0.2, 1.0])
    luz = luz / np.linalg.norm(luz) # Normaliza vector de luz
    
    # Producto punto para calcular la intensidad luminosa según la inclinación de la cara
    intensidad = np.sum(normales * luz, axis=1)
    intensidad = np.clip(intensidad, 0.3, 1.0) # Restringe límites para evitar zonas negras completas
    
    # Genera la paleta de color gris metalizado/plástico degradado según la luz
    face_colors = np.zeros((len(faces_sorted), 3))
    face_colors[:, 0] = 0.50 * intensidad  # Canal Rojo
    face_colors[:, 1] = 0.55 * intensidad  # Canal Verde
    face_colors[:, 2] = 0.60 * intensidad  # Canal Azul
    
    # ==========================================================
    # 3. CONSTRUCCIÓN DE POLÍGONOS DE PANTALLA
    # Extrae las posiciones X, Y reales escaladas en la pantalla gráfica.
    # ==========================================================
    p0_s = screen_vertices[faces_sorted[:, 0], :2]
    p1_s = screen_vertices[faces_sorted[:, 1], :2]
    p2_s = screen_vertices[faces_sorted[:, 2], :2]
    poligonos = np.stack((p0_s, p1_s, p2_s), axis=1)
    
    # ==========================================================
    # 4. CONFIGURACIÓN DEL LIENZO Y DIBUJO VECTORIAL
    # Sincroniza los colores del fondo para unificar la interfaz oscura.
    # ==========================================================
    fondo_oscuro = '#0f1319'
    ax.set_facecolor(fondo_oscuro)
    fig = ax.get_figure()
    fig.patch.set_facecolor(fondo_oscuro)
    
    # Dibuja la colección masiva de polígonos rellenos opacos con bordes claros
    collection = PolyCollection(
        poligonos, 
        facecolors=face_colors,   # Color con iluminación calculada
        edgecolors='#cbd5e1',    # Color gris claro para resaltar las aristas de la malla
        linewidths=0.2,          # Grosor fino para mantener la estética "pixeleada pero bonita"
        alpha=1.0                # Opacidad total para bloquear las transparencias caóticas
    )
    ax.add_collection(collection)

    # Forzar límites estables del viewport e invertir el eje Y para coordenadas estándar de pantalla
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.axis('off') # Oculta los ejes numéricos de Matplotlib para dar apariencia limpia de motor 3D