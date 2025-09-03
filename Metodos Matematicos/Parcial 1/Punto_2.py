import math

# Constantes
q = 2e-5  # Carga q en Coulombs
Q = 2e-5  # Carga Q en Coulombs
a = 0.9   # Radio del anillo en metros
epsilon = 8.854e-12  # Permitividad del vacío en C^2/(N·m^2)
F_target = 1.25  # Fuerza deseada en Newtons

# Función que describe la fuerza en función de z
def fuerza(z):
    return (1 / (4 * math.pi * epsilon)) * (q * Q * z) / ((z**2 + a**2)**(3/2))

# Método de regula falsi
def regula_falsi(f, a, b, tol=1e-6, max_iter=1000):
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        raise ValueError("El método de regula falsi requiere que f(a) y f(b) tengan signos opuestos")
    
    for i in range(max_iter):
        c = b - fb * (b - a) / (fb - fa)  # Punto de intersección
        fc = f(c)
        
        if abs(fc) < tol:
            return c
        
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    raise ValueError("El método no convergió")

# Búsqueda de un intervalo inicial donde la función cambia de signo
def encontrar_intervalo(f, z1, z2, pasos=100):
    z_values = [z1 + i * (z2 - z1) / pasos for i in range(pasos + 1)]
    for i in range(pasos):
        if f(z_values[i]) * f(z_values[i+1]) < 0:
            return z_values[i], z_values[i+1]
    raise ValueError("No se encontró un intervalo adecuado")

# Ampliar la búsqueda del intervalo adecuado
z1 = 0.01  # Extremo inferior de la búsqueda
z2 = 10.0  # Extremo superior de la búsqueda
z1, z2 = encontrar_intervalo(lambda z: fuerza(z) - F_target, z1, z2, pasos=10000)

# Encontrar el valor de z
try:
    z_sol = regula_falsi(lambda z: fuerza(z) - F_target, z1, z2)
    print(f"La distancia z donde la fuerza es de 1.25 N es: {z_sol:.6f} m")
except ValueError as e:
    print(e)
