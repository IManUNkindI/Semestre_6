% Constantes
g = 9.806; %m/s^2
Patm = 101293; %Pa

Pv1 = 0.26 * 6894.76; %Pa
Pv2 = 11.52 * 6894.76; %Pa

n = 1170 / 60;

u1 = 0.001138; %Kg/m^3
u2 = 0.000305; %Kg/m^3

q1 = 999.1; %Kg/m^3
q2 = 962.5; %Kg/m^3

Y1 = q1 * g; %Nm^3 (densidad por gravedad)
Y2 = q2 * g; %Nm^3 (densidad por gravedad)

SG1 = 1 * Y1;
SG2 = 0.9635 * Y2;

hl = 6 / 3.281; %m

% Inicializar vectores para almacenar los resultados

Q_= [0 4 8 12 16 20 24]; % Almacenar valores de Q galones por minuto
Pump_= [500 480 475 450 425 380 330];
NPSH_= [20 20 21 22 25 29 37];
Qc_= zeros(1, 7); % Almacenar valores de Q metros cubicos por segundo
P1_= zeros(1, 7);
P2_= zeros(1, 7);
z_= [21 18 15 12 9 6 3];


NPSHrm1_= zeros(1, 7); % Almacenar valores de NPSHr en metros
NPSHrf1_= zeros(1, 7); % Almacenar valores de NPSHr en pies

NPSHrm2_= zeros(1, 7); % Almacenar valores de NPSHr en metros
NPSHrf2_= zeros(1, 7); % Almacenar valores de NPSHr en pies

for i = 1:7
    % Conversion GPM a m3/s
    Qc_(i) = (Q_(i)*1000) * (6.309 * 10^-5); 

    P1_(i) = Patm + (z_(i) * Y1) - (hl * Y1);
    P2_(i) = Patm + (z_(i) * Y2) - (hl * Y2);

        % Calcular NPSHr
    NPSHr1 = ((Patm-Pv1)/Y1) + z_(i) - hl;
    NPSHrm1_(i) = NPSHr1;
    NPSHrf1_(i) = NPSHr1 * 3.281;

        % Calcular NPSHr
    NPSHr2 = ((Patm-Pv2)/Y2) + z_(i) - hl;
    NPSHrm2_(i) = NPSHr2;
    NPSHrf2_(i) = NPSHr2 * 3.281;
end

z1 = (37 / 3.281)  - ((Patm - Pv1) / Y1) + (hl);
z2 = (37 / 3.281) - ((Patm - Pv2) / Y2) + (hl);

disp((z1 * 3.281) + " Altura (ft) requerida para supuesto 1 de 60°F");
disp((z2 * 3.281) + " Altura (ft) requerida para supuesto 2 de 200°F");

disp(z1 + " Altura (m) requerida para supuesto 1 de 60°F");
disp(z2 + " Altura (m) requerida para supuesto 2 de 200°F");

% Gráfico de 60°F
figure('Name', 'Gráfico', 'Position', [100, 100, 800, 600]);
yyaxis left;
plot(Q_, NPSHrf1_, 'o-', 'DisplayName', 'NPSHr (pies)', 'Color', [0.500 0.200 0.600]);
ylabel('NPSH requerido (NPSHr) [pies]');
hold on;

yyaxis right;
plot(Q_, NPSH_, 'o-', 'DisplayName', 'NPSH (pies)', 'Color', [0.250 0.100 0.100]);
ylabel('NPSH [pies]');
hold on;

xlabel('Tasa de flujo (Q) [gal/min] x 1000');
title('NPSHr [feet] vs Tasa de flujo (Q) Para fluido a 60°F');
legend('Location', 'best');
grid on;

figure('Name', 'Gráfico', 'Position', [100, 100, 800, 600]);
plot(Q_, Pump_, 'o-', 'DisplayName', 'Pump (pies)', 'Color', [0.929 0.500 0.125]);
xlabel('Tasa de flujo (Q) [gal/min]');
ylabel('Presión en la salida (P2) [pies]');
title('Head in feet vs Tasa de flujo (Q)');
grid on;

% Gráfico de 200°F
figure('Name', 'Gráfico', 'Position', [100, 100, 800, 600]);
yyaxis left;
plot(Q_, NPSHrf2_, 'o-', 'DisplayName', 'NPSHr (pies)', 'Color', [0.500 0.200 0.600]);
ylabel('NPSH requerido (NPSHr) [pies]');
hold on;

yyaxis right;
plot(Q_, NPSH_, 'o-', 'DisplayName', 'NPSH (pies)', 'Color', [0.250 0.100 0.100]);
ylabel('NPSH [pies]');
hold on;

xlabel('Tasa de flujo (Q) [gal/min] x 1000');
title('NPSHr [feet] vs Tasa de flujo (Q) Para fluido a 200°F');
legend('Location', 'best');
grid on;