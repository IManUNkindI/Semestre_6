% Datos experimentales
fuerza = [100000 200000 300000 400000 500000 600000 700000 800000]; % en N
desplazamiento = [0.10 0.17 0.27 0.35 0.39 0.42 0.43 0.44]; % en m

% Visualizar los datos
plot(desplazamiento, fuerza, 'o');
xlabel('Desplazamiento (m)');
ylabel('Fuerza (x10^5 N)');
title('Fuerza vs. Desplazamiento');

% Identificar la región lineal
region_lineal = 1:4;

% Regresión lineal en la región lineal
p = polyfit(desplazamiento(region_lineal), fuerza(region_lineal), 1);
k = p(1); % Constante elástica
fprintf('La constante elástica k es: %.2f N/m\n', k);

% Graficar la recta de regresión lineal
hold on;
x_fit = linspace(min(desplazamiento(region_lineal)), max(desplazamiento(region_lineal)));
y_fit = polyval(p, x_fit);
plot(x_fit, y_fit, '-');

% Calcular el porcentaje de error en la región lineal
fuerza_pred_lineal = polyval(p, desplazamiento(region_lineal));
error_lineal = abs((fuerza(region_lineal) - fuerza_pred_lineal) ./ fuerza(region_lineal)) * 100;
disp('Porcentaje de error en la región lineal:');
disp(error_lineal);

% Calcular el promedio de error en la región lineal
promedio_error_lineal = mean(error_lineal);
fprintf('Promedio de error en la región lineal: %.2f%%\n', promedio_error_lineal);

% Limitar el ajuste no lineal desde 400000 N
indice_inicio = find(fuerza >= 400000, 1); % Encuentra el índice del primer punto donde la fuerza es >= 400000 N

% Ajustar una curva no lineal (polinomio de grado 2) desde 400000 N
p2 = polyfit(desplazamiento(indice_inicio:end), fuerza(indice_inicio:end), 2);
x_fit2 = linspace(min(desplazamiento(indice_inicio:end)), max(desplazamiento(indice_inicio:end)));
y_fit2 = polyval(p2, x_fit2);
plot(x_fit2, y_fit2, '--');

% Calcular el porcentaje de error en la región no lineal
fuerza_pred_nolineal = polyval(p2, desplazamiento(indice_inicio:end));
error_nolineal = abs((fuerza(indice_inicio:end) - fuerza_pred_nolineal) ./ fuerza(indice_inicio:end)) * 100;
disp('Porcentaje de error en la región no lineal:');
disp(error_nolineal);

% Calcular el promedio de error en la región no lineal
promedio_error_nolineal = mean(error_nolineal);
fprintf('Promedio de error en la región no lineal: %.2f%%\n', promedio_error_nolineal);

legend('Datos experimentales', 'Regresión lineal', 'Ajuste no lineal desde 400000 N');
hold off;
