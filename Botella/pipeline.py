import numpy as np
import transformations as transform

def load_obj(filename):
    """
    Cargador de archivos Wavefront .obj optimizado para memoria.
    Lee vértices geométricos y reconstruye las caras triangulares del modelo.
    """
    vertices = []
    faces = []
    
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):  # Líneas que definen un Vértice (X, Y, Z)
                vertices.append([float(x) for x in line.split()[1:4]])
            elif line.startswith('f '):  # Líneas que definen una Cara (Conectividad de puntos)
                # Extraemos solo el índice del vértice, ignorando normales o texturas (mapeo '/')
                face = [int(x.split('/')[0]) - 1 for x in line.split()[1:]]
                if len(face) == 3:  # Triángulo estándar
                    faces.append(face)
                elif len(face) == 4:  # Cuadrilátero: se divide dinámicamente en dos triángulos
                    faces.append([face[0], face[1], face[2]])
                    faces.append([face[0], face[2], face[3]])

    v_np = np.array(vertices, dtype=np.float32)
    
    # --- AUTO-ESCALA Y CENTRADO GEOMÉTRICO ---
    # Encuentra los límites de la caja contenedora del objeto (Bounding Box)
    min_coords = np.min(v_np, axis=0)
    max_coords = np.max(v_np, axis=0)
    centro = (min_coords + max_coords) / 2.0
    v_np = v_np - centro  # Centra el objeto exactamente en el origen (0,0,0)
    
    # Normaliza el tamaño para que quepa perfectamente en el viewport de Matplotlib
    escala_maxima = np.max(max_coords - min_coords)
    if escala_maxima != 0:
        v_np = v_np / (escala_maxima / 2.3) 

    # --- REGULADOR DE DENSIDAD DE LA MALLA ---
    # Selecciona una de cada 40 caras del archivo masivo original. Esto mantiene 
    # la silueta completa y genera una rejilla texturizada óptima para tiempo real.
    caras_optimizadas = faces[::40] 

    # Conversión a coordenadas homogéneas agregando una columna de 1s al final
    ones = np.ones((v_np.shape[0], 1), dtype=np.float32)
    vertices_homogeneos = np.hstack((v_np, ones))
    
    return vertices_homogeneos, caras_optimizadas

def run_pipeline(vertices, tx, ty, tz, rx, ry, rz, sx, sy, sz, width, height):
    """
    Ejecuta el pipeline de gráficos completo (Matriz Mundo -> Vista -> Proyección -> División W).
    """
    # 1. Matriz de Espacio de Mundo (TRS): Aplica Escala, Rotación y Traslación en orden matemático
    M_world = transform.get_translation_matrix(tx, ty, tz) @ transform.get_rotation_matrix(rx, ry, rz) @ transform.get_scale_matrix(sx, sy, sz)
    world_vertices = (M_world @ vertices.T).T

    # 2. Matriz de Espacio de Vista: Coloca la cámara fija en la coordenada Z = -5
    M_view = transform.get_translation_matrix(0, 0, -5) 
    camera_vertices = (M_view @ world_vertices.T).T

    # 3. Matriz de Proyección Perspectiva: Aplica distorsión cónica (ángulo de visión de 60°)
    M_proj = transform.get_perspective_matrix(60, width/height, 0.1, 100.0)
    projected_vertices = (M_proj @ camera_vertices.T).T

    # 4. División de Perspectiva (Normalización W): Pasa de 4D a Coordenadas de Dispositivo Normalizadas (NDC)
    w = projected_vertices[:, 3:4].copy()
    w[np.abs(w) < 1e-5] = 1.0  # Control matemático para evitar divisiones entre cero
    ndc = projected_vertices / w
    ndc = np.nan_to_num(ndc, nan=0.0, posinf=1.0, neginf=-1.0) # Limpieza de errores numéricos indeterminados

    # 5. Transformación de Viewport: Mapea las coordenadas numéricas a pixeles reales en pantalla
    x_screen = ((ndc[:, 0] + 1.0) * width / 2.0).astype(np.int32)
    y_screen = ((1.0 - ndc[:, 1]) * height / 2.0).astype(np.int32)
    z_screen = ndc[:, 2] # Mantiene la información de profundidad para el algoritmo del pintor

    screen_vertices = np.stack((x_screen, y_screen, z_screen), axis=1)
    return screen_vertices, camera_vertices[:, :3]