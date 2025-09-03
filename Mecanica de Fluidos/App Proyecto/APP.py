import math
import os
import PIL.Image
from PIL import ImageTk  # Asegúrate de importar Image y ImageTk correctamente
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BombaR = 0
KP = 0
KA = 0
KV = 0
KC = 0
KT = 0

ajustePump = 0
ajusteK = 0

def PDF():
        datos = {
        "Cantidad de niveles": nivel_entry.get(),
        "Cantidad de apartamentos por nivel": apartamentos_entry.get(),
        "Numero de baños": baño_var.get(),
        "Consumo sanitario": sanitarios_var.get(),
        "Tipo de cocina": cocina_var.get(),
        "Tipo de lavadero": lavanderia_var.get(),
        "Cantidad de personas por apartamento": personas_entry.get(),
        "Cantidad de sotanos": sotanos_entry.get(),
        "Cantidad de cuartos de baño": basura_entry.get(),
        "Bomba recomendada": bomba_entry.get(),
        "Eficiencia de la bomba": bomba_ef_entry.get() + "%",
        "Capacidad del tanque (L)": tanque_entry.get(),
        "Eficiencia del tanque": th_ef_entry.get() + "%",
        "Diametro de la tuberia principal": tubmn_entry.get(),
        "Materiual de la tuberia principal": tubmn_material_entry.get(),
        "Diametro de la tuberia en apartamentos": tubapt_entry.get(),
        "Material de la tuberia en apartamentos": tubapt_material_entry.get(),
        "Valvulas de regulacion": valve_reg_entry.get(),
        "Valvulas de presion": valve_pre_entry.get(),
        "Caudal Requerido (L/s)": Q_entry.get(),
        "Factor K tuberia principal": KP_entry.get(),
        "Factor K tuberia en apartamento": KA_entry.get(),
        "Factor K codos": KC_entry.get(),
        "Factor K conexion T": KT_entry.get(),
        "Factor K valvulas": KV_entry.get(),
        
        }

        # Crea un objeto canvas
        c = canvas.Canvas("Informe de red hidraulica.pdf", pagesize=letter)
        ancho, alto = letter

        # Escribe un título en el PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, alto - 50, "Informe de red hidraulica")

         # Escribe los datos de las variables en el PDF
        c.setFont("Helvetica", 12)
        y = alto - 100
        for clave, valor in datos.items():
                c.drawString(100, y, f"{clave}: {valor}")
                y -= 20

        # Finaliza el PDF
        c.save()

def leer_bombas(Pumps):
        bombas = []
        with open(Pumps, 'r') as f:
            for linea in f:
                partes = linea.strip().split(';')
                bombas.append(partes)
        return bombas
def eficiencia():
        seleccion = opcion.get()
        global ajustePump
        if(seleccion=="No"):
                th_ef_entry.config(state="readonly")
                bomba_ef_entry.config(state="readonly")
                ajustePump = 0
        elif(seleccion=="Si"):
                th_ef_entry.config(state="normal")
                bomba_ef_entry.config(state="normal")
                ajustePump = 1
def factorK():
        seleccion1 = opcion2.get()
        global ajusteK
        if(seleccion1=="Fabricante"):
                ajusteK = 0
                KP_entry.config(state="readonly")
                KA_entry.config(state="readonly")
                KV_entry.config(state="readonly")
                KC_entry.config(state="readonly")
                KT_entry.config(state="readonly")
        elif(seleccion1=="Personalizado"):
                ajusteK = 1
                KP_entry.config(state="normal")
                KA_entry.config(state="normal")
                KV_entry.config(state="normal")
                KC_entry.config(state="normal")
                KT_entry.config(state="normal")
 
def salir():
        ventana.destroy()
        
        
def actualizar():
        # Aquí podrías realizar tus cálculos
        cabezas = personas_entry.get()
        aptos_pn = apartamentos_entry.get()
        niveles = nivel_entry.get()

        presionmReq = 172000

        baño = baño_var.get()
        caudalReq = 0
        if baño == 2:
                caudalReq = 1.2
        elif baño == 2.5:
                caudalReq = 1.6
        elif baño == 3:
                caudalReq = 1.8

        consumo_ps = sanitarios_var.get()
        consumoL = 0
        if consumo_ps == "bajo":
                consumoL = float(baño) * 20
                caudalReq = caudalReq * 0.8
        elif consumo_ps == "medio":
                consumoL = float(baño) * 30
                caudalReq = caudalReq * 1
        elif consumo_ps == "alto":
                consumoL = float(baño) * 40
                caudalReq = caudalReq * 1.2
            
        cocina = cocina_var.get()
        cocinaL = 0
        if cocina == "lavaplatos, maquina lavavajillas, nevera":
                cocinaL = 30
                caudalReq = caudalReq + 0.2 + 4 + 0.2
        elif cocina == "lavaplatos, nevera":
                cocinaL = 40
                caudalReq = cuadalReq + 0.2 + 0.2
            
        lavanderia = lavanderia_var.get()
        lavanderiaL = 0
        if lavanderia == "lavadora, lavadero":
                lavanderiaL = 20
                caudalReq = caudalReq + 0.15 + 0.1
        elif lavandera == "lavadero":
                lavanderiaL = 30
                caudalReq = caudalReq + 0.1

        caudalApt = caudalReq
        caudalReq = caudalReq * (int(aptos_pn)*int(niveles))
        caudalReq = round(caudalReq, 3)
        sotanos = sotanos_entry.get()
        sotanosL = int(sotanos) * 60
        
        basura = basura_entry.get()
        basuraL = int(basura) * 20

        tanque = ((int(cabezas)*int(aptos_pn)*int(niveles))*(int(consumoL)) + (int(aptos_pn)*int(niveles))*(int(cocinaL)+int(lavanderiaL)) + (basuraL + sotanosL))*3

        hidro = (caudalReq * 86400) / presionmReq
        tubmnD = ((math.sqrt((4 * (caudalReq/1000))/(2.4 * math.pi))) * 39.37) / 4
        tubmnM = tuberia_var_main.get()
        if(tubmnM=="PVC"):
                tubmnP = 12
        elif(tubmnM=="Cobre"):
                tubmnP = 40
        elif(tubmnM=="Hierro"):
                tubmnP = 20

        tubaptD = ((math.sqrt((4 * (caudalApt/1000))/(2 * math.pi))) * 39.37) / 2
        tubaptM = tuberia_var_apart.get()
        if(tubaptM=="PVC"):
                tubaptP = 8
        elif(tubaptM=="Cobre"):
                tubaptP = 20
        elif(tubaptM=="Hierro"):
                tubaptP = 12
        

        valveR = int(niveles)
        valveP = int(niveles) * 2


        bombas = leer_bombas('Pumps.txt')
        
        Diametro = math.ceil(tubmnD) * 0.0254
        QRec = (2.45 * (math.pi/4) * (Diametro**2)) * 1000
        Eficiencia = 0
        HP = 0
        EficienciaTH = 0
        global BombaR
        
        global KP
        global KA
        global KV
        global KC
        global KT

        global ajustePump
        global ajusteK
        
        #Bomba1[0] ; FPS[1] ; A2.5 X 2-6[2] ; 13[3]Caudal min ; 20[4]Caudal max ; 66[5]Eficiencia ; 40[6]Carga m ; 15[7]potencia HP
        if(ajustePump == 0):
                EficienciaTH = 50
                for i in range(18):
                        if(float(bombas[i][3]) <= QRec <= float(bombas[i][4])):
                                BombaR = bombas[i][2]
                                if(int(Eficiencia) < int(bombas[i][5])):
                                        Eficiencia = bombas[i][5]
                                        if(int(HP) > int(bombas[i][7])):
                                                HP = bombas[i][7]
        elif(ajustePump == 1):
                BombaR = bomba_entry.get()
                Eficiencia = bomba_ef_entry.get()
                EficienciaTH = th_ef_entry.get()


        if(ajusteK == 0):
                KP = 0.011
                KA = 0.0095
                KV = 2.9
                KC = 0.35
                KT = 2.4
        elif(ajusteK == 1):
                KP = KP_entry.get()
                KA = KA_entry.get()
                KV = KV_entry.get()
                KC = KC_entry.get()
                KT = KT_entry.get()
                

        
        

        
        # Actualizar tanque de almacenamiento
        tanque_entry.configure(state="normal")
        tanque_entry.delete(0, tk.END) # Borra cualquier contenido previo
        tanque_entry.insert(0, str(tanque)) # Inserta el resultado como una cadena
        tanque_entry.configure(state="readonly")

        # Actualizar tanque hidroneumatico
        hidro_entry.configure(state="normal")
        hidro_entry.delete(0, tk.END) # Borra cualquier contenido previo
        hidro_entry.insert(0, str(round(hidro, 3))) # Inserta el resultado como una cadena
        hidro_entry.configure(state="readonly")

        # Actualizar diametro tuberia principal
        tubmn_entry.configure(state="normal")
        tubmn_entry.delete(0, tk.END) # Borra cualquier contenido previo
        tubmn_entry.insert(0, str(math.ceil(tubmnD)) + "¨") # Inserta el resultado como una cadena
        tubmn_entry.configure(state="readonly")

        # Actualizar material tuberia principal
        tubmn_material_entry.configure(state="normal")
        tubmn_material_entry.delete(0, tk.END) # Borra cualquier contenido previo
        tubmn_material_entry.insert(0, str(tubmnM)) # Inserta el resultado como una cadena
        tubmn_material_entry.configure(state="readonly")

        # Actualizar presion max tuberia principal
        tubmn_presion_entry.configure(state="normal")
        tubmn_presion_entry.delete(0, tk.END) # Borra cualquier contenido previo
        tubmn_presion_entry.insert(0, str(tubmnP)) # Inserta el resultado como una cadena
        tubmn_presion_entry.configure(state="readonly")
    
        # Actualizar diametro tuberia en apartamentos
        tubapt_entry.configure(state="normal")
        tubapt_entry.delete(0, tk.END) # Borra cualquier contenido previo
        tubapt_entry.insert(0, str(math.ceil(tubaptD)) + "¨") # Inserta el resultado como una cadena
        tubapt_entry.configure(state="readonly")

        # Actualizar tanque hidroneumatico
        tubapt_material_entry.configure(state="normal")
        tubapt_material_entry.delete(0, tk.END) # Borra cualquier contenido previo
        tubapt_material_entry.insert(0, str(tubaptM)) # Inserta el resultado como una cadena
        tubapt_material_entry.configure(state="readonly")

        # Actualizar tanque hidroneumatico
        tubapt_presion_entry.configure(state="normal")
        tubapt_presion_entry.delete(0, tk.END) # Borra cualquier contenido previo
        tubapt_presion_entry.insert(0, str(tubaptP)) # Inserta el resultado como una cadena
        tubapt_presion_entry.configure(state="readonly")

        # Actualizar valvula de regulacion
        valve_reg_entry.configure(state="normal")
        valve_reg_entry.delete(0, tk.END) # Borra cualquier contenido previo
        valve_reg_entry.insert(0, str(math.ceil(valveR))) # Inserta el resultado como una cadena
        valve_reg_entry.configure(state="readonly")

        # Actualizar valvula de regulacion
        valve_pre_entry.configure(state="normal")
        valve_pre_entry.delete(0, tk.END) # Borra cualquier contenido previo
        valve_pre_entry.insert(0, str(valveP)) # Inserta el resultado como una cadena
        valve_pre_entry.configure(state="readonly")

        # Actualizar bomba recomendada
        bomba_entry.configure(state="normal")
        bomba_entry.delete(0, tk.END) # Borra cualquier contenido previo
        bomba_entry.insert(0, str(BombaR)) # Inserta el resultado como una cadena
        bomba_entry.configure(state="readonly")

        # Actualizar bomba recomendada
        bomba_ef_entry.configure(state="normal")
        bomba_ef_entry.delete(0, tk.END) # Borra cualquier contenido previo
        bomba_ef_entry.insert(0, str(Eficiencia)) # Inserta el resultado como una cadena
        bomba_ef_entry.configure(state="readonly")
        
        # Caudal Requerido
        Q_entry.configure(state="normal")
        Q_entry.delete(0, tk.END) # Borra cualquier contenido previo
        Q_entry.insert(0, str(round(QRec,3))) # Inserta el resultado como una cadena
        Q_entry.configure(state="readonly")

        # Actualizar eficiencia tanque
        th_ef_entry.configure(state="normal")
        th_ef_entry.delete(0, tk.END) # Borra cualquier contenido previo
        th_ef_entry.insert(0, str(EficienciaTH)) # Inserta el resultado como una cadena
        th_ef_entry.configure(state="readonly")

        # Actualizar Factor K
        KP_entry.configure(state="normal")
        KP_entry.delete(0, tk.END) # Borra cualquier contenido previo
        KP_entry.insert(0, str(KP)) # Inserta el resultado como una cadena
        KP_entry.configure(state="readonly")

        KA_entry.configure(state="normal")
        KA_entry.delete(0, tk.END) # Borra cualquier contenido previo
        KA_entry.insert(0, str(KA)) # Inserta el resultado como una cadena
        KA_entry.configure(state="readonly")

        KV_entry.configure(state="normal")
        KV_entry.delete(0, tk.END) # Borra cualquier contenido previo
        KV_entry.insert(0, str(KV)) # Inserta el resultado como una cadena
        KV_entry.configure(state="readonly")

        KC_entry.configure(state="normal")
        KC_entry.delete(0, tk.END) # Borra cualquier contenido previo
        KC_entry.insert(0, str(KC)) # Inserta el resultado como una cadena
        KC_entry.configure(state="readonly")

        KT_entry.configure(state="normal")
        KT_entry.delete(0, tk.END) # Borra cualquier contenido previo
        KT_entry.insert(0, str(KT)) # Inserta el resultado como una cadena
        KT_entry.configure(state="readonly")
        
        eficiencia()
        factorK()

def center_window(ventana):
        ventana.update_idletasks()
        # Obtener el tamaño de la pantalla
        frame_width = entrada_frame.winfo_width()
        frame_height = (80 + entrada_frame.winfo_height()+ pump_frame.winfo_height()+ salidas_frame.winfo_height()+ button_frame.winfo_height())
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
    
        # Calcular las coordenadas para centrar la ventana
        x = (screen_width - frame_width) // 2
        y = (screen_height - frame_height) // 2

        # Configurar la posición de la ventana
        ventana.geometry('{}x{}+{}+{}'.format(frame_width, frame_height, x, y))
        ventana.overrideredirect(True)

def show_warning_popup(ventana):
        response = messagebox.askyesno("Advertencia", "Advertencia, este programa supone un tanque ubicado en el sotano inferior bajo el nivel del piso y el cuarto de bombas encima del nivel de piso (succion negativa). ¿Desea continuar?")
        if not response:
                ventana.destroy()  # Cerrar la aplicación si el usuario elige no continuar

# Crea la ventana
ventana = Tk()
ventana.title("Sistema de Agua Potable para Edificio de Apartamentos")
ventana.geometry("1300x720")  # Tamaño fijo de la ventana
ventana.iconbitmap("Kirby.ico")
ventana.resizable(False, False)  # No se puede redimensionar


# Sección de entrada de datos
entrada_frame = tk.Frame(ventana, bd=2, relief=tk.GROOVE, height=300)
entrada_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

# Numero de niveles de apartamentos
nivel_label = tk.Label(entrada_frame, text="Numero de niveles de apartamentos:")
nivel_label.grid(row=0, column=0, sticky="e", pady=(10, 10))
nivel_entry = ttk.Entry(entrada_frame, justify=tk.CENTER)
nivel_entry.grid(row=0, column=1, pady=(10, 10))

# Numero de apartamentos por nivel
apartamentos_label = tk.Label(entrada_frame, text="Numero de apartamentos por nivel:")
apartamentos_label.grid(row=1, column=0, sticky="e", pady=(0, 10))
apartamentos_entry = ttk.Entry(entrada_frame, justify=tk.CENTER)
apartamentos_entry.grid(row=1, column=1, pady=(0, 10))

# Numero de unidades de baño por apartamento
baño_label = tk.Label(entrada_frame, text="Numero de unidades de baño por apartamento:")
baño_label.grid(row=2, column=0, sticky="e", pady=(0, 10))
baño_options = ["2", "2.5", "3"]
baño_var = tk.StringVar()
baño_var.set(baño_options[1])  # Valor predeterminado
baño_dropdown = tk.OptionMenu(entrada_frame, baño_var, *baño_options)
baño_dropdown.config(width=10)
baño_dropdown.grid(row=2, column=1, pady=(0, 10))

# Tipo de aparatos sanitarios
sanitarios_label = tk.Label(entrada_frame, text="Tipo de aparatos sanitarios:")
sanitarios_label.grid(row=3, column=0, sticky="e", pady=(0, 10))
sanitarios_options = ["bajo", "medio", "alto"]
sanitarios_var = tk.StringVar()
sanitarios_var.set(sanitarios_options[0])  # Valor predeterminado
sanitarios_dropdown = tk.OptionMenu(entrada_frame, sanitarios_var, *sanitarios_options)
sanitarios_dropdown.config(width=10)
sanitarios_dropdown.grid(row=3, column=1, pady=(0, 10))

# Tipo de cocina
cocina_label = tk.Label(entrada_frame, text="Tipo de cocina:")
cocina_label.grid(row=4, column=0, sticky="e", pady=(0, 10))
cocina_options = ["lavaplatos, maquina lavavajillas, nevera", "lavaplatos, nevera"]
cocina_var = tk.StringVar()
cocina_var.set(cocina_options[0])  # Valor predeterminado
cocina_dropdown = tk.OptionMenu(entrada_frame, cocina_var, *cocina_options)
cocina_dropdown.config(width=35)
cocina_dropdown.grid(row=4, column=1, pady=(0, 10))

# Tipo de lavanderia
lavanderia_label = tk.Label(entrada_frame, text="Tipo de lavanderia:")
lavanderia_label.grid(row=5, column=0, sticky="e", pady=(0, 10))
lavanderia_options = ["lavadora, lavadero", "lavadero"]
lavanderia_var = tk.StringVar()
lavanderia_var.set(lavanderia_options[0])  # Valor predeterminado
lavanderia_dropdown = tk.OptionMenu(entrada_frame, lavanderia_var, *lavanderia_options)
lavanderia_dropdown.config(width=18)
lavanderia_dropdown.grid(row=5, column=1, pady=(0, 10))

# Numero de personas por apartamento
personas_label = tk.Label(entrada_frame, text="Numero de personas aproximadas por apartamento:")
personas_label.grid(row=0, column=2, sticky="e", pady=(10, 10))
personas_entry = ttk.Entry(entrada_frame, justify=tk.CENTER)
personas_entry.grid(row=0, column=3, pady=(10, 10))

# Numero de sotanos y puntos de conexion por nivel
sotanos_label = tk.Label(entrada_frame, text="Numero de sotanos:")
sotanos_label.grid(row=1, column=2, sticky="e", pady=(0, 10))
sotanos_entry = ttk.Entry(entrada_frame, justify=tk.CENTER)
sotanos_entry.grid(row=1, column=3, pady=(0, 10))
conexion_label = tk.Label(entrada_frame, text="3 puntos de conexion por nivel")
conexion_label.grid(row=1, column=4, pady=(0, 10))

# Cuartos de basura
basura_label = tk.Label(entrada_frame, text="Cuartos de basura:")
basura_label.grid(row=2, column=2, sticky="e", pady=(0, 10))
basura_entry = ttk.Entry(entrada_frame, justify=tk.CENTER)
basura_entry.grid(row=2, column=3, pady=(0, 10))

# Seleccion de material de las tuberias
tuberia_label = tk.Label(entrada_frame, text="Seleccion de material de las tuberias:")
tuberia_label.grid(row=3, column=2, sticky="e", pady=(0, 10))
tuberia_options = ["Cobre", "PVC", "Hierro"]
tuberia_var_main = tk.StringVar()
tuberia_var_main.set(tuberia_options[0])  # Valor predeterminado
tuberia_dropdown_main = tk.OptionMenu(entrada_frame, tuberia_var_main, *tuberia_options)
tuberia_dropdown_main.config(width=8)
tuberia_dropdown_main.grid(row=4, column=3, pady=(0, 10))
tuberia_var_apart = tk.StringVar()
tuberia_var_apart.set(tuberia_options[1])  # Valor predeterminado
tuberia_dropdown_apart = tk.OptionMenu(entrada_frame, tuberia_var_apart, *tuberia_options)
tuberia_dropdown_apart.config(width=8)
tuberia_dropdown_apart.grid(row=5, column=3, pady=(0, 10))
tuberia_label0 = tk.Label(entrada_frame, text="Tuberia Principal:")
tuberia_label0.grid(row=4, column=2, sticky="e", pady=(0, 10))
tuberia_label1 = tk.Label(entrada_frame, text="Tuberia en apartamento:")
tuberia_label1.grid(row=5, column=2, sticky="e", pady=(0, 10))

# Sección de salida de información
salidas_frame = tk.Frame(ventana, bd=2, relief=tk.GROOVE, height=300)
salidas_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

# Capacidad del Tanque de almacenamiento
tanque_label = tk.Label(salidas_frame, text="Cap. del tanque de almacenamiento (L):")
tanque_label.grid(row=0, column=0, sticky="e", pady=(10, 10))
tanque_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
tanque_entry.grid(row=0, column=1, pady=(10, 10))

# Capacidad del Tanque hidroneumatico
hidro_label = tk.Label(salidas_frame, text="Cap. del tanque hidroneumatico (L):")
hidro_label.grid(row=1, column=0, sticky="e", pady=(10, 10))
hidro_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
hidro_entry.grid(row=1, column=1, pady=(10, 10))

# Diametros de las tuberias
# Principal
tubmn_label = tk.Label(salidas_frame, text="Diametro de la tuberia principal (in):")
tubmn_label.grid(row=0, column=2, sticky="e", pady=(10, 10))
tubmn_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
tubmn_entry.grid(row=0, column=3, pady=(10, 10))
tubmn_material_label = tk.Label(salidas_frame, text="Material:")
tubmn_material_label.grid(row=0, column=4, sticky="e", pady=(10, 10))
tubmn_material_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
tubmn_material_entry.grid(row=0, column=5, pady=(10, 10))
tubmn_presion_label = tk.Label(salidas_frame, text="Presion Max. (bar):")
tubmn_presion_label.grid(row=0, column=6, sticky="e", pady=(10, 10))
tubmn_presion_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
tubmn_presion_entry.grid(row=0, column=7, pady=(10, 10))

# En apartamentos
tubapt_label = tk.Label(salidas_frame, text="Diametro de la tuberia en cada apartamento (in):")
tubapt_label.grid(row=1, column=2, sticky="e", pady=(10, 10))
tubapt_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
tubapt_entry.grid(row=1, column=3, pady=(10, 10))
tubapt_material_label = tk.Label(salidas_frame, text="Material:")
tubapt_material_label.grid(row=1, column=4, sticky="e", pady=(10, 10))
tubapt_material_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
tubapt_material_entry.grid(row=1, column=5, pady=(10, 10))
tubapt_presion_label = tk.Label(salidas_frame, text="Presion Max. (bar):")
tubapt_presion_label.grid(row=1, column=6, sticky="e", pady=(10, 10))
tubapt_presion_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
tubapt_presion_entry.grid(row=1, column=7, pady=(10, 10))
    
# Valvulas
valve_label = tk.Label(salidas_frame, text="Valvulas recomendadas:")
valve_label.grid(row=4, column=1, sticky="e", pady=(10, 10))

valve_reg_label = tk.Label(salidas_frame, text="Valvulas de regulacion:")
valve_reg_label.grid(row=4, column=2, sticky="e", pady=(10, 10))
valve_reg_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
valve_reg_entry.grid(row=4, column=3, pady=(10, 10))

valve_pre_label = tk.Label(salidas_frame, text="Valvulas de presion:")
valve_pre_label.grid(row=4, column=4, sticky="e", pady=(10, 10))
valve_pre_entry = ttk.Entry(salidas_frame, state="readonly", justify=tk.CENTER)
valve_pre_entry.grid(row=4, column=5, pady=(10, 10))

# Sección de selección y ajustes de bomba y otros
pump_frame = tk.Frame(ventana, bd=2, relief=tk.GROOVE)
pump_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

# Bomba recomendada
bomba_label = tk.Label(pump_frame, text="Bomba Hidraulica recomendada:")
bomba_label.grid(row=0, column=0, sticky="e", pady=(10, 10))
bomba_entry = ttk.Entry(pump_frame, state="readonly", justify=tk.CENTER)
bomba_entry.grid(row=0, column=1, pady=(10, 10))

# Caudal Requerido
Q_label = tk.Label(pump_frame, text="Caudal Requerido (L/s):")
Q_label.grid(row=0, column=2, sticky="e", pady=(10, 10))
Q_entry = ttk.Entry(pump_frame, state="readonly", justify=tk.CENTER)
Q_entry.grid(row=0, column=3, pady=(10, 10))

# Eficiencia recomendada
bomba_ef_label = tk.Label(pump_frame, text="Eficiencia de la bomba hidraulica (%):")
bomba_ef_label.grid(row=1, column=0, sticky="e", pady=(10, 10))
bomba_ef_entry = ttk.Entry(pump_frame, justify=tk.CENTER)
bomba_ef_entry.grid(row=1, column=1, pady=(10, 10))

ajuste_label = tk.Label(pump_frame, text="Ajustar eficiencia:")
ajuste_label.grid(row=1, column=4, sticky="e", pady=(10, 10))
opcion = tk.StringVar(value="No")
radio_si = tk.Radiobutton(pump_frame, text="Si", variable=opcion, value="Si", command=eficiencia)
radio_si.grid(row=1, column=5, pady=(10, 10))
radio_no = tk.Radiobutton(pump_frame, text="No", variable=opcion, value="No", command=eficiencia)
radio_no.grid(row=1, column=6, pady=(10, 10))

th_ef_label = tk.Label(pump_frame, text="Eficiencia del tanque hidroneumatico (%):")
th_ef_label.grid(row=1, column=2, sticky="e", pady=(10, 10))
th_ef_entry = ttk.Entry(pump_frame, justify=tk.CENTER)
th_ef_entry.grid(row=1, column=3, pady=(10, 10))


# Factor K
K_label = tk.Label(pump_frame, text="Factor K:")
K_label.grid(row=2, column=0, sticky="e", pady=(10, 10))

opcion2 = tk.StringVar(value="Fabricante")
radio_si = tk.Radiobutton(pump_frame, text="Fabricante", variable=opcion2, value="Fabricante", command=factorK)
radio_si.grid(row=2, column=1, pady=(10, 10))
radio_no = tk.Radiobutton(pump_frame, text="Personalizado", variable=opcion2, value="Personalizado", command=factorK)
radio_no.grid(row=2, column=2, pady=(10, 10))

KP_label = tk.Label(pump_frame, text="Tuberia Principal:")
KP_label.grid(row=3, column=0, sticky="e", pady=(10, 10))
KP_entry = tk.Entry(pump_frame, justify=tk.CENTER)
KP_entry.grid(row=3, column=1, sticky="e", pady=(10, 10))
KA_label = tk.Label(pump_frame, text="Tuberia en Apartamento:")
KA_label.grid(row=3, column=2, sticky="e", pady=(10, 10))
KA_entry = tk.Entry(pump_frame, justify=tk.CENTER)
KA_entry.grid(row=3, column=3, sticky="e", pady=(10, 10))
KV_label = tk.Label(pump_frame, text="Valvulas:")
KV_label.grid(row=3, column=4, sticky="e", pady=(10, 10))
KV_entry = tk.Entry(pump_frame, justify=tk.CENTER)
KV_entry.grid(row=3, column=5, sticky="e", pady=(10, 10))
KC_label = tk.Label(pump_frame, text="Codos:")
KC_label.grid(row=4, column=0, sticky="e", pady=(10, 10))
KC_entry = tk.Entry(pump_frame, justify=tk.CENTER)
KC_entry.grid(row=4, column=1, sticky="e", pady=(10, 10))
KT_label = tk.Label(pump_frame, text="Union T:")
KT_label.grid(row=4, column=2, sticky="e", pady=(10, 10))
KT_entry = tk.Entry(pump_frame, justify=tk.CENTER)
KT_entry.grid(row=4, column=3, sticky="e", pady=(10, 10))


# Aquí puedes agregar widgets para que el usuario ajuste la bomba y otras configuraciones
# Frame del boton
button_frame = tk.Frame(ventana, bd=2, relief=tk.GROOVE)
button_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

# Botones
boton_calcular = tk.Button(button_frame, text="Actualizar", command=actualizar)
boton_calcular.grid(row=0, column=0, padx=10, pady=10)

boton_salir = tk.Button(button_frame, text="Salir", command=salir)
boton_salir.grid(row=0, column=6, padx=10, pady=10)

boton_exp = tk.Button(button_frame, text="Generar PDF", command=PDF)
boton_exp.grid(row=0, column=1, padx=10, pady=10)

center_window(ventana)
eficiencia()
factorK()
show_warning_popup(ventana)
ventana.mainloop()
