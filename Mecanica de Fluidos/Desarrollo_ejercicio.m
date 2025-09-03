% Constantes

Pv = 3169; %Pa
Patm = 101293; %Pa
D = 0.1016; %m
L = 3.2; %m
u = 0.000891; %Kg/m^3
k = 7.4;
z = 1.2192; %m
e = 0.00508; %m
q = 997; %Kg/m^3
g = 9.806; %m/s^2
Y = q * g; %Nm^3 (densidad por gravedad)
A = (pi/4)*(D^2);
E = e/D;

% Inicializar vectores para almacenar los resultados

Q_= [0 100 200 300 400 500 600 700 800]; % Almacenar valores de Q galones por minuto
Pump_= [60 60 59 58 57 55 48 38 30];
Pumpf_= [0 3 3.2 4 4.2 5.6 6.1 7.3 8];
Qc_= zeros(1, 9); % Almacenar valores de Q metros cubicos por segundo
v_= zeros(1, 9); % Almacenar valores de v
Re_= zeros(1, 9); %Reynolds
f_= zeros(1, 9); % Almacenar el valor de f
hs_= zeros(1, 9); % Almacenar valores de hs
hf_= zeros(1, 9); % Almacenar valores de hf

hlm_= zeros(1, 9); % Almacenar valores de hl en metros
hlf_= zeros(1, 9); % Almacenar valores de hl en pies

P2m_= zeros(1, 9); % Almacenar valores de P2 en metros
P2f_= zeros(1, 9); % Almacenar valores de P2 en pies

NPSHrm_= zeros(1, 9); % Almacenar valores de NPSHr en metros
NPSHrf_= zeros(1, 9); % Almacenar valores de NPSHr en pies



for i = 1:9
    % Conversion GPM a m3/s
    Qc_(i) = Q_(i) * (6.309 * 10^-5); 

    % Calcular velocidad v
    v_(i)= Qc_(i)/A;

    % Calcular Reynolds
    Re_(i)= (q*v_(i)*D)/u;

    % Calcular factor de friccion
    term1 = E/3.7;
    term2 = 5.74 / (Re_(i)^0.9);
    f_(i) = 0.25 / (log(term1 + term2))^2;

    % Calcular perdidas menores y por friccion
    hf_(i) = f_(i) * (L/D) * ((v_(i)^2) / (2 * g));
    hs_(i) = k * ((v_(i)^2) / (2*g));

    % Calcular hl
    hlm_(i) = (hf_(i) + hs_(i));
    hlf_(i) = hlm_(i) * 3.281;

    % Calcular P2
    P2 = z - hlm_(i);
    P2m_(i)= P2;
    P2f_(i)= P2 * 3.281;

    % Calcular NPSHr
    NPSHr = ((Patm-Pv)/Y) + z - hlm_(i);
    NPSHrm_(i) = NPSHr;
    NPSHrf_(i) = NPSHr * 3.281;

end

% Crear tabla para la primera serie de datos (SISTEMA INTERNACIONAL)
table1_data = [Q_.', v_.' hlm_.' NPSHrm_.' P2m_.'];
table1_column_names = {'Q (Galones/min)', 'v (m/s)', 'hl (m)', 'NPSHr (m)', 'P2 (m)'};
table1 = uitable('Data', table1_data, 'ColumnName', table1_column_names, 'Position', [50 30 442 165]);

% Crear tabla para la segunda serie de datos (SISTEMA INGLÉS)
table2_data = [Q_.', v_.' hlf_.' NPSHrf_.' P2f_.'];
table2_column_names = {'Q (Galones/min)', 'v (m/s)', 'hl (ft)', 'NPSHr (ft)', 'P2 (ft)'};
table2 = uitable('Data', table2_data, 'ColumnName', table2_column_names, 'Position', [50 230 442 165]);

% Establecer título para la primera tabla (SISTEMA INTERNACIONAL)
table1_title = uicontrol('Style', 'text', 'String', 'SISTEMA INTERNACIONAL', 'Position', [50 200 200 20], 'FontSize', 12);

% Establecer título para la segunda tabla (SISTEMA INGLÉS)
table2_title = uicontrol('Style', 'text', 'String', 'SISTEMA INGLÉS', 'Position', [50 400 200 20], 'FontSize', 12);

% Gráfico de NPSHr, P2 y Qc vs Q
figure('Name', 'Gráfico', 'Position', [100, 100, 800, 600]);
plot(Q_, NPSHrf_, 'o-', 'DisplayName', 'NPSHr (pies)', 'Color', [0.494 0.184 0.556]);
ylabel('NPSH requerido (NPSHr) [pies]');
hold on;
xlabel('Tasa de flujo (Q) [gal/min]');
plot(Q_, Pumpf_, 'o-', 'DisplayName', 'Pump (pies)', 'Color', [0.929 0.500 0.125]);
title('NPSHr [feet] vs Tasa de flujo (Q)');
legend('Location', 'best');
grid on;

figure('Name', 'Gráfico', 'Position', [100, 100, 800, 600]);
plot(Q_, Pump_, 'o-', 'DisplayName', 'NPSHr (pies)', 'Color', [0.494 0.184 0.556]);
xlabel('Tasa de flujo (Q) [gal/min]');
ylabel('Presión en la salida (P2) [pies]');
title('Head in feet vs Tasa de flujo (Q)');
grid on;