import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pipeline
import rasterizer

def create_interface(obj_path):
    vertices, faces = pipeline.load_obj(obj_path)
    width, height = 500, 500

    fig, ax = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(bottom=0.35) # Espacio para los sliders abajo

    def update(val):
        tx, ty, tz = s_tx.val, s_ty.val, s_tz.val
        rx, ry, rz = s_rx.val, s_ry.val, s_rz.val
        sx, sy, sz = s_sx.val, s_sy.val, s_sz.val
        
        screen_vertices, camera_vertices = pipeline.run_pipeline(vertices, tx, ty, tz, rx, ry, rz, sx, sy, sz, width, height)
        rasterizer.render_flat_shading(screen_vertices, camera_vertices, faces, width, height, ax)
        fig.canvas.draw_idle()

    # Definir posiciones de los Sliders (X, Y, Ancho, Alto)
    ax_tx = plt.axes([0.15, 0.25, 0.25, 0.03])
    ax_ty = plt.axes([0.15, 0.20, 0.25, 0.03])
    ax_tz = plt.axes([0.15, 0.15, 0.25, 0.03])
    
    ax_rx = plt.axes([0.55, 0.25, 0.25, 0.03])
    ax_ry = plt.axes([0.55, 0.20, 0.25, 0.03])
    ax_rz = plt.axes([0.55, 0.15, 0.25, 0.03])

    s_tx = Slider(ax_tx, 'Tx', -2.0, 2.0, valinit=0.0)
    s_ty = Slider(ax_ty, 'Ty', -2.0, 2.0, valinit=0.0)
    s_tz = Slider(ax_tz, 'Tz', -3.0, 3.0, valinit=0.0)
    
    s_rx = Slider(ax_rx, 'Rx°', -180.0, 180.0, valinit=20.0)
    s_ry = Slider(ax_ry, 'Ry°', -180.0, 180.0, valinit=30.0)
    s_rz = Slider(ax_rz, 'Rz°', -180.0, 180.0, valinit=0.0)

    # Sliders de Escala abajo
    ax_sx = plt.axes([0.35, 0.08, 0.35, 0.03])
    s_sx = Slider(ax_sx, 'Escala', 0.2, 3.0, valinit=1.0)
    s_sy = s_sz = s_sx # Vinculamos las escalas para que conserve proporciones al moverlo

    s_tx.on_changed(update)
    s_ty.on_changed(update)
    s_tz.on_changed(update)
    s_rx.on_changed(update)
    s_ry.on_changed(update)
    s_rz.on_changed(update)
    s_sx.on_changed(update)

    # Render inicial
    update(None)
