% Datos experimentales
gamma_dot = [50 70 90 110 130]; % Tasa de deformación
tau = [6.01 7.48 8.59 9.19 10.21]; % Esfuerzo cortante

% Función a ajustar
modelfun = @(params, gamma_dot) params(1) .* gamma_dot .^ params(2);

% Condiciones iniciales para los parámetros
params0 = [2, 1]; % Valores iniciales para m y n

% Ajuste de la curva
params = lsqcurvefit(modelfun, params0, gamma_dot, tau);

% Valores de los parámetros ajustados
m = params(1);
n = params(2);

% Valores ajustados
tau_fit = modelfun(params, gamma_dot);

% Cálculo del porcentaje de error
percent_error = abs(tau - tau_fit) ./ abs(tau) * 100;

% Cálculo del promedio de error
average_error = mean(percent_error);

% Mostrar los resultados
fprintf('El valor de m es: %.4f\n', m);
fprintf('El valor de n es: %.4f\n', n);

% Mostrar el porcentaje de error para cada punto
for i = 1:length(tau)
    fprintf('Porcentaje de error para gamma_dot = %.1f: %.2f%%\n', gamma_dot(i), percent_error(i));
end

% Mostrar el promedio de error
fprintf('El promedio de error porcentual es: %.2f%%\n', average_error);

% Graficar los datos y la curva ajustada
figure;
plot(gamma_dot, tau, 'o', 'MarkerSize', 8, 'DisplayName', 'Datos experimentales');
hold on;
plot(gamma_dot, tau_fit, '-', 'LineWidth', 2, 'DisplayName', 'Curva ajustada');
xlabel('Tasa de deformación (1/s)');
ylabel('Esfuerzo cortante (N/m^2)');
title('Ajuste de Curva de Esfuerzo Cortante vs Tasa de Deformación');
legend('show');
grid on;
