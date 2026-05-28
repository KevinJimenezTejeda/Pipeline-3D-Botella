# Pipeline de Gráficos 3D por Software - Modelo 
---
### ⚠️ Requisito de Modelo Geométrico
Debido al peso del archivo geométrico (`botella.obj` de 119 MB), este archivo no se encuentra alojado en el repositorio. Por favor, **descargue el archivo .obj proporcionado en la plataforma de entrega** y colóquelo en la carpeta raíz del proyecto junto a los scripts `.py` antes de ejecutar el programa.
---

Este proyecto implementa un pipeline de renderizado tridimensional completo desde cero utilizando Python, NumPy y Matplotlib. El sistema carga un modelo geométrico complejo, aplica transformaciones lineales interactivas en tiempo real y realiza el procesamiento de proyección y rasterizado por software sin depender de APIs gráficas externas (como OpenGL o DirectX).

---

## 📊 Reporte Visual del Proceso

El pipeline procesa la información en tres etapas fundamentales, mapeando la geometría desde el mundo real hasta los pixeles discretos de la pantalla:

### 1. Objeto Real de Referencia
Fotografía del contenedor físico bidimensional y el planteamiento del espacio tridimensional utilizado como base para el diseño, las proporciones y la escala inicial:

![Botella Real](1_botella_real.png)

### 2. Malla Geométrica Original (.OBJ)
Visualización de la nube de puntos y conectividad de caras del archivo Wavefront `.obj` original, demostrando la densidad masiva de polígonos antes de ser optimizada y filtrada por nuestro pipeline para su ejecución fluida:

![Malla OBJ](2_modelo_obj.png)

### 3. Renderizado Sólido Final (Nuestro Programa)
Resultado final del renderizado interactivo en nuestra interfaz. Muestra la botella con una estructura de malla sólida bien definida, volumen corregido mediante el Algoritmo del Pintor (Z-Sorting) e iluminación plana (Flat Shading) reaccionando de manera fluida a los sliders de transformación:

![Resultado Programa](3_resultado_programa.png)

---

## 🛠️ Especificaciones Técnicas del Pipeline

El flujo de datos matemáticos implementado en los módulos sigue la arquitectura clásica del pipeline de gráficos, integrando las siguientes etapas:

* **Espacio de Objeto a Mundo (Mundo TRS):** Multiplicación de matrices homogéneas de $4 \times 4$ para transformaciones compuestas de Escala ($S$), Rotación ($R$) en ángulos de Euler e hilos de Traslación ($T$).
  
  $$M_{world} = T(t_x, t_y, t_z) \cdot R_x(\theta_x) \cdot R_y(\theta_y) \cdot R_z(\theta_z) \cdot S(s_x, s_y, s_z)$$

* **Espacio de Vista (Cámara):** Transformación de cámara fija mediante una matriz de traslación inversa para posicionar el ojo del observador en la escena (fijado en la coordenada $Z = -5$).

* **Proyección Perspectiva:** Cálculo de distorsión cónica basada en el Campo de Visión ($FOV$), la Relación de Aspecto ($Aspect\ Ratio$), y los planos de corte cercano ($near$) y lejano ($far$), mapeando el cono de visión a un volumen cúbico canónico.

* **División de Perspectiva:** Normalización de coordenadas espaciales mediante la división homogénea entre la componente $W$, pasando del espacio proyectivo de 4D a Coordenadas de Dispositivo Normalizadas (NDC) de 3D.

  $$\begin{bmatrix} X_{ndc} \\ Y_{ndc} \\ Z_{ndc} \end{bmatrix} = \begin{bmatrix} X / W \\ Y / W \\ Z / W \end{bmatrix}$$

* **Mapeo de Viewport:** Conversión lineal de las escalas NDC $[-1, 1]$ a las dimensiones reales en pixeles discretos configurados para la ventana de visualización ($width \times height$).

* **Rasterizado y Sombreado (Flat Shading):** Ordenamiento de caras ocultas mediante la profundidad promedio de los vértices (Algoritmo del Pintor) para evitar solapamientos caóticos. El cálculo de iluminación se resuelve por software mediante el producto punto entre el vector normal de cada cara ($\hat{n}$) y el vector direccional de la luz ($\hat{l}$):

  $$Intensidad = \max(\hat{n} \cdot \hat{l},\ 0.3)$$

---

## 🚀 Guía de Ejecución (Mac / Windows)

Para ejecutar este entorno interactivo en cualquier sistema operativo (incluyendo macOS), siga estos pasos desde la terminal:

1. **Instalar las dependencias de cómputo numérico y graficación:**
   
   pip install numpy matplotlib
2 **Ejecutar el módulo principal de la aplicación:**
   python Botella.py
Controles: Utilice los sliders inferiores de la interfaz gráfica de Matplotlib para manipular los ángulos de rotación y la escala del modelo en tiempo real.
---
### ⚠️ Requisito de Modelo Geométrico
Debido al peso del archivo geométrico (`botella.obj` de 119 MB), este archivo no se encuentra alojado en el repositorio. Por favor, **descargue el archivo .obj proporcionado en la plataforma de entrega** y colóquelo en la carpeta raíz del proyecto junto a los scripts `.py` antes de ejecutar el programa.
---