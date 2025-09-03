import tkinter as tk
from tkinter import ttk
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import os
import subprocess  # Para abrir el PDF

# Cálculos hidráulicos y selección del diámetro óptimo
def calcular_datos():
    g = 32.2  # ft/s^2
    rho = 62.4  # lb/ft³
    nu = 1.40e-5  # ft²/s
    L = 4374 # longitud de la tubería en pies
    H_static = 150  # altura estática en pies
    Q_gpm = (1000000 / 8) / 60  # flujo en galones por minuto
    D_options = [2, 3, 4, 5, 6, 7, 8]  # diámetros posibles en pulgadas
    eta_bomba = 0.657  # eficiencia de la bomba
    eta_motor = 0.9  # eficiencia del motor
    costo_tuberia_por_pie = {2: 203252, 3: 203252, 4: 203252, 5: 203252, 6: 203252, 7: 203252, 8:203252 }  # COP/ft
    
    Q_cfs = (Q_gpm * 0.002228) / 2  # flujo en ft³/s, considerando 2 tuberías
    K_total = ((2*0.75) + 0.2 + 1.0) * 2  # Pérdidas por codos y accesorios
    
    resultados = []
    for D in D_options:
        D_ft = D / 12  # Diámetro en pies
        A = math.pi * (D_ft / 2) ** 2  # Área transversal en ft²
        v = Q_cfs / A  # Velocidad en ft/s
        Re = (v * D_ft) / nu  # Número de Reynolds
        
        # Fricción usando Colebrook-White
        f = 0.02  # Suposición inicial
        for _ in range(10):
            f = 0.25 / (math.log10((0.0002 / D_ft) / 3.7 + 5.74 / Re ** 0.9)) ** 2
        
        hf_tuberia = f * (L / D_ft) * (v ** 2) / (2 * g)  # Pérdidas en ft
        hf_codos = K_total * (v ** 2) / (2 * g)  # Pérdidas por codos
        hf_total = hf_tuberia + hf_codos
        H_total = H_static + hf_total
        P_bomba = (rho * g * Q_cfs * (H_total)) / (550 * eta_bomba * eta_motor)  # HP
        P_bomba_kw = P_bomba * 0.7457  # Conversión a kW
        costo_tuberia = costo_tuberia_por_pie[D] * L
        costo_operativo_diario = P_bomba_kw * 12 * 400  # COP por día
        costo_mensual = costo_operativo_diario * 30  # COP por mes
        costo_total_anual = costo_tuberia + (costo_operativo_diario * 365)
        
        resultados.append({
            "diametro": D,
            "h_f_total": hf_total,
            "H_total": H_total,
            "P_bomba": P_bomba,
            "P_bomba_kw": P_bomba_kw,
            "velocidad": v,
            "costo_tuberia": costo_tuberia,
            "costo_mensual": costo_mensual,
            "costo_total_anual": costo_total_anual
        })
    
    resultado_optimo = min(resultados, key=lambda x: x["costo_total_anual"])
    return resultados, resultado_optimo

# Función para abrir un archivo PDF
def abrir_pdf():
    ruta_pdf = os.path.join(os.getcwd(), "PipeFlow.pdf")  # Ruta del archivo PDF junto al ejecutable
    try:
        subprocess.Popen([ruta_pdf], shell=True)  # Abre el PDF en el visor predeterminado
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

# Interfaz gráfica con Tkinter
def crear_interfaz():
    resultados, optimo = calcular_datos()
    
    root = tk.Tk()
    root.title("Selección de Tuberías y Bombas")
    root.state('zoomed')  # Maximiza la ventana al abrir
    root.configure(bg="#f4f4f9")  # Fondo gris suave
    
    # Frame para la tabla de resultados
    frame_tabla = tk.Frame(root, bg="#ffffff", bd=2, relief="sunken")
    frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(frame_tabla, columns=("diametro", "h_f_total", "H_total", "P_bomba", "P_bomba_kw", "velocidad", "costo_tuberia", "costo_mensual", "costo_total_anual"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Encabezados de la tabla
    encabezados = [
        "Diámetro (in)", "Pérdidas por fricción (ft)", "Pérdidas totales (ft)", "Potencia (HP)",
        "Potencia (kW)", "Velocidad (ft/s)", "Costo Tubería (COP)",
        "Costo Mensual (COP)", "Costo Total Anual (COP)"
    ]
    for col, head in zip(tree["columns"], encabezados):
        tree.heading(col, text=head)
        tree.column(col, width=160, anchor=tk.CENTER)  # Ajusto el ancho de las columnas para visibilidad
    
    for res in resultados:
        tree.insert("", tk.END, values=(
            res["diametro"], f"{res['h_f_total']:.2f}", f"{res['H_total']:.2f}", 
            f"{res['P_bomba']:.2f}", f"{res['P_bomba_kw']:.2f}", 
            f"{res['velocidad']:.2f}", f"{res['costo_tuberia']:.2f}", 
            f"{res['costo_mensual']:.2f}", f"{res['costo_total_anual']:.2f}"
        ))
    
    # Frame para la visualización del resultado óptimo
    frame_optimo = tk.Frame(root, bg="#ffffff", bd=2, relief="sunken")
    frame_optimo.pack(fill=tk.X, padx=10, pady=10)
    
    etiqueta_optimo = tk.Label(frame_optimo, text=(
        f"Selección Óptima: Diámetro {optimo['diametro']} in, Potencia {optimo['P_bomba_kw']:.2f} kW, "
        f"Costo Mensual ${optimo['costo_mensual']:.2f}, Costo Total Anual ${optimo['costo_total_anual']:.2f}"
    ), font=("Arial", 14, "bold"), fg="blue", bg="#ffffff")
    etiqueta_optimo.pack(pady=10)
    
    # Botón para abrir PDF
    boton_pdf = tk.Button(frame_optimo, text="Abrir Informe PipeFlow", command=abrir_pdf, bg="#007ACC", fg="white", font=("Arial", 12, "bold"))
    boton_pdf.pack(pady=10)
    
    # Frame para la gráfica
    frame_grafica = tk.Frame(root, bg="#ffffff", bd=2, relief="sunken")
    frame_grafica.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    diametros = [res["diametro"] for res in resultados]
    perdidas_totales = [res["h_f_total"] for res in resultados]
    
    figura = Figure(figsize=(8, 4), dpi=100)
    grafica = figura.add_subplot(111)
    puntos = grafica.plot(diametros, perdidas_totales, marker="o", linestyle="-", color="blue", label="Pérdidas Totales")
    grafica.set_title("Pérdidas por fricción vs Diámetro")
    grafica.set_xlabel("Diámetro de Tubería (in)")
    grafica.set_ylabel("Pérdidas por fricción (ft)")  # Cambié el título del eje Y
    grafica.grid(True)
    grafica.legend()
    
    cursor = mplcursors.cursor(puntos[0], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"Diámetro: {sel.target[0]:.0f} in\nPérdidas: {sel.target[1]:.2f} ft"
    ))
    
    canvas = FigureCanvasTkAgg(figura, frame_grafica)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas.draw()
    
    root.mainloop()

crear_interfaz()
