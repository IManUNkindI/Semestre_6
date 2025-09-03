% Parámetros dados
k1 = 500000; % en g/s^2
k2 = 40; % en g/s^2
m = 90; % en g
g = 9.81; % en m/s^2
h = 0.45; % en m

% Ecuación de conservación de energía
f = @(d) (2*k2*d^(5/2)/5) + (k1*d^2/2) + m*g*d - m*g*h;

% Derivada de la ecuación para Newton-Raphson
df = @(d) k2*d^(3/2) + k1*d + m*g;

% Valor inicial de la deformación
d0 = 0.1; % Asume un valor inicial cercano a la solución

% Tolerancia y número máximo de iteraciones
tol = 1e-6;
max_iter = 100;

% Método de Newton-Raphson
d = d0;
for iter = 1:max_iter
    fd = f(d);
    dfd = df(d);
    
    % Actualizar el valor de d
    d_new = d - fd/dfd;
    
    % Verificar la convergencia
    if abs(d_new - d) < tol
        break;
    end
    
    d = d_new;
end

% Mostrar el resultado
if iter == max_iter
    disp('El método no convergió dentro del número máximo de iteraciones');
else
    fprintf('La deformación del resorte es d = %.6f m\n', d);
end

% Graficación de la función f(d)
d_values = linspace(0, 0.5, 1000); % Intervalo de deformaciones
f_values = arrayfun(f, d_values); % Evaluar f(d) en el intervalo

figure;
plot(d_values, f_values, 'b-', 'LineWidth', 2);
hold on;
plot(d, f(d), 'ro', 'MarkerSize', 10, 'LineWidth', 2); % Marcar el punto solución
xlabel('Deformación d (m)');
ylabel('f(d)');
title('Gráfica de la ecuación de conservación de energía');
grid on;

% Marcar el punto donde la función cruza el eje x
yline(0, '--k');
legend('f(d)', 'Solución aproximada');
hold off;
