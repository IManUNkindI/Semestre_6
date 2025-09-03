% Dimensiones ajustables del mecanismo
L1 = 0.145; % Longitud de la barra inferior (m)
L2 = 0.135; % Longitud de la barra superior (m)
d_base = 0.04325; % Distancia entre los orificios en la base (m)
theta_max = pi/3; % Ángulo máximo de desplazamiento (60 grados)

% Parámetros del ciclo
T_cycle = 10; % Duración total del ciclo (s)
T_half = T_cycle / 2; % Duración de ida o vuelta (s)
t = linspace(0, T_cycle, 1000); % Vector de tiempo (s)
omega1 = theta_max / T_half; % Velocidad angular constante (rad/s)

% Calcular el ángulo de la barra inferior \theta_1
theta1 = zeros(size(t));
for i = 1:length(t)
    if t(i) <= T_half
        theta1(i) = omega1 * t(i); % Ida
    else
        theta1(i) = theta_max - omega1 * (t(i) - T_half); % Vuelta
    end
end

% Inicializar variables para almacenar resultados
x = zeros(size(theta1));
y = zeros(size(theta1));
omega2 = zeros(size(theta1));
alpha2 = zeros(size(theta1));

% Rango de búsqueda para phi y opciones de fsolve
phi_guess = 0; % Suposición inicial para phi
options = optimset('Display', 'off', 'TolFun', 1e-8);

% Loop para cálculos de posición y velocidad angular
for i = 1:length(theta1)
    % Posición del pasador de la barra inferior
    x1 = d_base / 2;
    y1 = 0;

    % Coordenadas de la barra inferior
    x2 = x1 + L1 * cos(theta1(i));
    y2 = y1 + L1 * sin(theta1(i));

    % Resolver posición del pasador de la barra superior
    f_phi = @(phi) (x2 - (d_base / 2 + L2 * cos(phi)))^2 + ...
                   (y2 - (L2 * sin(phi)))^2; % Igualar movimiento en X y Y
    phi = fsolve(f_phi, phi_guess, options);
    phi_guess = phi; % Actualizar suposición inicial

    % Coordenadas de la barra superior (restricción de simetría)
    x(i) = x2;
    y(i) = L2 * sin(phi);

    % Velocidad angular
    dtheta1_dt = omega1 * (t(i) <= T_half) - omega1 * (t(i) > T_half);
    J = -L2 * sin(phi); % Jacobiano inverso
    omega2(i) = J * dtheta1_dt;

    % Aceleración angular
    ddtheta1_dt2 = 0; % Suponemos aceleración angular constante
    alpha2(i) = J * ddtheta1_dt2 + (L2 * cos(phi) * omega2(i)^2);
end

% Cálculo de la magnitud del desplazamiento
delta_x = max(x) - min(x); % Diferencia entre posición inicial y final en x
delta_y = max(y) - min(y); % Diferencia entre posición inicial y final en y

% Mostrar los desplazamientos calculados
disp(['Desplazamiento en X: ', num2str(delta_x, '%.4f'), ' m']);
disp(['Desplazamiento en Y: ', num2str(delta_y, '%.4f'), ' m']);

% Gráficas de resultados
figure;
subplot(5, 1, 1);
plot(t, theta1, 'LineWidth', 1.5);
xlabel('Tiempo (s)');
ylabel('\theta_1 (rad)');
title('Ángulo \theta_1 vs Tiempo');

subplot(5, 1, 2);
plot(t, x, 'LineWidth', 1.5);
xlabel('Tiempo (s)');
ylabel('Distancia en X (m)');
title('Desplazamiento en X vs Tiempo');

subplot(5, 1, 3);
plot(t, y, 'LineWidth', 1.5);
xlabel('Tiempo (s)');
ylabel('Distancia en Y (m)');
title('Desplazamiento en Y vs Tiempo');

subplot(5, 1, 4);
plot(t, omega2, 'LineWidth', 1.5);
xlabel('Tiempo (s)');
ylabel('\omega_2 (rad/s)');
title('Velocidad angular \omega_2 vs Tiempo');

subplot(5, 1, 5);
plot(t, alpha2, 'LineWidth', 1.5);
xlabel('Tiempo (s)');
ylabel('\alpha_2 (rad/s^2)');
title('Aceleración angular \alpha_2 vs Tiempo');