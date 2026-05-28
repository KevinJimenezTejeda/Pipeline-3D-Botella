import numpy as np

def get_translation_matrix(tx, ty, tz):
    """
    Genera una matriz de transformación homogénea de 4x4 para Traslación.
    Mueve el objeto en los ejes X, Y y Z.
    """
    return np.array([
        [1, 0, 0, tx],  # Fila 1: Afecta la posición en X
        [0, 1, 0, ty],  # Fila 2: Afecta la posición en Y
        [0, 0, 1, tz],  # Fila 3: Afecta la posición en Z
        [0, 0, 0,  1]   # Fila 4: Coordenada homogénea para mantener la escala
    ], dtype=np.float32)

def get_scale_matrix(sx, sy, sz):
    """
    Genera una matriz homogénea de 4x4 para Escalación.
    Modifica el tamaño del objeto de forma independiente en cada eje.
    """
    return np.array([
        [sx,  0,  0, 0],  # Multiplica los valores de X por el factor sx
        [ 0, sy,  0, 0],  # Multiplica los valores de Y por el factor sy
        [ 0,  0, sz, 0],  # Multiplica los valores de Z por el factor sz
        [ 0,  0,  0, 1]   # Coordenada homogénea estable
    ], dtype=np.float32)

def get_rotation_matrix(rx_deg, ry_deg, rz_deg):
    """
    Genera la matriz de rotación compuesta en 3D (Ángulos de Euler).
    Convierte los grados de los sliders a radianes y multiplica las matrices en orden (X * Y * Z).
    """
    # Conversión matemática de grados a radianes
    rad_x = np.radians(rx_deg)
    rad_y = np.radians(ry_deg)
    rad_z = np.radians(rz_deg)
    
    # Matriz de rotación sobre el eje X (Cabeceo / Pitch)
    Rx = np.array([
        [1,         0,          0, 0],
        [0, np.cos(rad_x), -np.sin(rad_x), 0],
        [0, np.sin(rad_x),  np.cos(rad_x), 0],
        [0,         0,          0, 1]
    ], dtype=np.float32)
    
    # Matriz de rotación sobre el eje Y (Guiñada / Yaw)
    Ry = np.array([
        [ np.cos(rad_y), 0, np.sin(rad_y), 0],
        [         0, 1,         0, 0],
        [-np.sin(rad_y), 0, np.cos(rad_y), 0],
        [         0, 0,         0, 1]
    ], dtype=np.float32)
    
    # Matriz de rotación sobre el eje Z (Alabeo / Roll)
    Rz = np.array([
        [np.cos(rad_z), -np.sin(rad_z), 0, 0],
        [np.sin(rad_z),  np.cos(rad_z), 0, 0],
        [        0,          0, 1, 0],
        [        0,          0, 0, 1]
    ], dtype=np.float32)
    
    # Multiplicación matricial compuesta: primero se aplica Z, luego Y, al final X
    return Rx @ Ry @ Rz

def get_perspective_matrix(fov_deg, aspect_ratio, near, far):
    """
    Genera la matriz de Proyección Perspectiva matemática de 4x4.
    Simula el comportamiento del ojo humano o una cámara real (los objetos lejanos se ven más chicos).
    """
    f = 1.0 / np.tan(np.radians(fov_deg) / 2.0) # Distancia focal basada en el campo de visión (FOV)
    
    return np.array([
        [f / aspect_ratio, 0,                   0,                                     0], # Escala X por aspecto de pantalla
        [0,                f,                   0,                                     0], # Escala Y
        [0,                0, (far+near)/(near-far), (2.0 * far * near) / (near-far)], # Mapeo no lineal de profundidad en Z
        [0,                0,                  -1,                                     0]  # Guarda la profundidad original en la coordenada W
    ], dtype=np.float32)