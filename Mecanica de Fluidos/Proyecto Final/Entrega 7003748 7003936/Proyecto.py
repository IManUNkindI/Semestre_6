import math

# Constantes
g = 32.2  # ft/s^2, aceleración gravitacional
g_m = 9.81  # m/s^2, aceleración gravitacional en SI
rho = 62.4  # lb/ft³, densidad del agua
rho_si = 999.70  # kg/m³, densidad del agua en SI
nu = 1.40e-5  # ft²/s, viscosidad cinemática del agua (10°C)

# Parámetros del problema
L = 4374  # longitud de la tubería en pies
H_static = 150  # altura estática en pies
Q_gpm = (1000000/8)/60  # flujo en galones por minuto
D_options = [2, 3, 4, 5, 6, 7, 8]  # diámetros posibles en pulgadas
eta_bomba = 0.657  # eficiencia de la bomba
eta_motor = 0.9  # eficiencia del motor
costo_tuberia_por_pie = {2: 203252, 3: 203252, 4: 203252, 5: 203252, 6: 203252, 7:203252, 8:203252}  # USD/ft para cada diámetro

# Conversión de flujo a ft³/s
Q_cfs = (Q_gpm * 0.002228)/2  # gal/min a ft³/s                Cantidad de tuberias : 2

# Pérdidas en codos
K_90 = 0.75  # Factor de pérdida en codo de 90° brida
K_valve = 0.2  # Factor de pérdida en valvula de compuerta completamente abierta
K_valveNR = 1.0 # Factor de pérdida en valvula antiretorno
K_filter = 3.0 # Factor de pérdida 
K_total = ((2*K_90) + K_valve + K_valveNR + K_filter)*2 # Pérdidas totales por codos        Cantidad de tuberias : 2

# Cálculo de pérdidas de carga y selección del diámetro óptimo
def calcular_perdidas(D, L, Q_cfs, nu):
    D_ft = D / 12  # Diámetro en pies
    A = math.pi * (D_ft / 2) ** 2  # Área transversal en ft²
    v = Q_cfs / A  # Velocidad en ft/s
    Re = (v * D_ft) / nu  # Número de Reynolds

    # Fricción usando ecuación de Colebrook-White (iterativa simplificada)
    f = 0.02  # suposición inicial
    for _ in range(10):
        f = 0.25 / (math.log10((0.0002 / D_ft) / 3.7 + 5.74 / Re ** 0.9)) ** 2

    hf_tuberia = f * (L / D_ft) * (v ** 2) / (2 * g)  # Pérdidas en ft
    hf_codos = K_total * (v ** 2) / (2 * g)  # Pérdidas por codos en ft
    hf_total = hf_tuberia + hf_codos
    return hf_total, v

# Calcular costos y optimizar
resultados = []
for D in D_options:
    hf_total, v = calcular_perdidas(D, L, Q_cfs, nu)
    H_total = H_static + hf_total
    P_bomba = (rho * g * Q_cfs * (H_total)) / (550 * eta_bomba * eta_motor)  # Potencia en HP        Cantidad de bombas por tuberias : 1
    # Costos de tubería
    costo_tuberia = costo_tuberia_por_pie[D] * L  # USD
    # Costo operativo diario
    P_bomba_kW = P_bomba * 0.7457  # HP a kW
    costo_operativo_diario = P_bomba_kW * 12 * 400  # COP
    # Costo operativo mensual
    costo_total_mensual = costo_operativo_diario * 30
    # Total anual (365 días)
    costo_total_anual = costo_tuberia + (costo_operativo_diario * 365)
    # Resultados
    resultados.append({
        "diametro": D,
        "h_f_total": hf_total,
        "H_total": H_total,
        "P_bomba": P_bomba,
        "P_bomba2": P_bomba_kW,
        "velocidad": v,
        "costo_tuberia": costo_tuberia,
        "costo_total_anual": costo_total_anual,
        "costo_total_mensual": costo_total_mensual
    })

# Seleccionar el tamaño óptimo de tubería
resultado_optimo = min(resultados, key=lambda x: x["costo_total_anual"])

# Mostrar resultados
print("Resultados para cada diámetro:")
print("Diámetro (pulg)  | h_f_total (ft) | H_total (ft) | Potencia (HP) | Velocidad (ft/s)| Costo Tubería (COP)   | Costo Total Anual (COP)")
for res in resultados:
    print(f"{res['diametro']:<16} | {res['h_f_total']:<14.2f} | {res['H_total']:<12.2f} | {res['P_bomba']:<13.2f} | {res['velocidad']:<15.2f} | {res['costo_tuberia']:<21.2f} | {res['costo_total_anual']:<21.2f}")

# Mostrar resultados en unidades internacionales
print("\nResultados para cada diámetro (unidades internacionales):")
print("Diámetro (mm) | h_f_total (m)| H_total (m)| Potencia (kW)|Velocidad (m/s)")

for res in resultados:
    diametro_mm = res['diametro'] * 25.4  # pulgadas a mm
    h_f_total_m = res['h_f_total'] * 0.3048  # ft a m
    H_total_m = res['H_total'] * 0.3048  # ft a m
    P_bomba_kW = res['P_bomba'] * 0.7457  # HP a kW
    velocidad_m_s = res['velocidad'] * 0.3048  # ft/s a m/s
    print(f"{diametro_mm:<13.2f} | {h_f_total_m:<12.2f} | {H_total_m:<10.2f} | {P_bomba_kW:<12.2f} | {velocidad_m_s:<13.2f} ")

print("\nSelección óptima:")
print(f"Diámetro económico: {resultado_optimo['diametro']} pulgadas")
print(f"Costo total anual: ${resultado_optimo['costo_total_anual']:.2f}")
print(f"Costo total mensual: ${resultado_optimo['costo_total_mensual']:.2f}")
print(f"Potencia de la bomba: {resultado_optimo['P_bomba']:.2f} HP")
print(f"Potencia de la bomba: {resultado_optimo['P_bomba2']:.2f} kW")
print(f"Velocidad del agua: {resultado_optimo['velocidad']:.2f} ft/s")

# Selección del tamaño y velocidad del impulsor de la bomba
velocidades_impulsor = [900, 1200, 1500, 1800]  # RPM disponibles
optimos_impulsores = []
for rpm in velocidades_impulsor:
    potencia_real = resultado_optimo['P_bomba'] * (rpm / 1200) ** 3  # Escalar por ley de semejanza
    optimos_impulsores.append((rpm, potencia_real))

print("\nOpciones de velocidad del impulsor de la bomba (RPM):")
for rpm, potencia in optimos_impulsores:
    print(f"RPM: {rpm}, Potencia requerida: {potencia:.2f} HP")
