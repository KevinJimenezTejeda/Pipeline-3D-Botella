import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), 'interface'))
import gui

if __name__ == "__main__":
    nombre_archivo_obj = "botella.obj" 
    print("Cargando y procesando objeto ... Por favor espera un momento.")
    
    # Crea la ventana gráfica e interactiva
    gui.create_interface(nombre_archivo_obj)
    
    # EL CANDADO: Obliga a Windows a mantener abierta la ventana hasta que tú le des a la X
    print("¡Procesamiento completo! Abriendo interfaz gráfica...")
    plt.show()