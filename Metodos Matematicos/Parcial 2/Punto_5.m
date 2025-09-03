% Datos de la distancia y el ancho de la pista
distancia = [2.4, 1.5, 2.4, 1.8, 1.8, 2.9, 1.2, 3, 1];
ancho_pista = [2.9, 2.1, 2.3, 2.1, 1.8, 2.7, 1.5, 2.9, 1];

% 5.1) Graficar los datos
scatter(distancia, ancho_pista, 'filled');
xlabel('Distancia (m)');
ylabel('Ancho de la pista (m)');
title('Relación entre distancia y ancho de pista');
grid on;

% 5.2) Ajuste una línea recta a los datos con regresión lineal
p = polyfit(distancia, ancho_pista, 1); % Ajuste lineal
x_fit = linspace(min(distancia), max(distancia), 100);
y_fit = polyval(p, x_fit);

hold on;
plot(x_fit, y_fit, 'r-', 'LineWidth', 2);
legend('Datos', 'Ajuste lineal');

% 5.3) Determinar el ancho de pista mínimo para una distancia de 2 m
ancho_minimo = polyval(p, 2);
disp(['El ancho de pista mínimo para una distancia de 2 m es: ', num2str(ancho_minimo), ' m']);

% Calcular los valores predichos para las distancias originales
y_pred = polyval(p, distancia);

% Calcular el error absoluto y el porcentaje de error
error_absoluto = abs(ancho_pista - y_pred);
porcentaje_error = (error_absoluto ./ ancho_pista) * 100;

% Mostrar los errores calculados
disp('Errores absolutos para cada punto:');
disp(error_absoluto);

disp('Porcentaje de error para cada punto:');
disp(porcentaje_error);

% Promedio del porcentaje de error
promedio_error = mean(porcentaje_error);
disp(['El porcentaje de error promedio es: ', num2str(promedio_error), '%']);
