% Parcial 2 Modelos Punto 1 Sistema Termico
clc, clear

syms s R1 R2 Ct Cm

% Matrices del sistema
A = [ -1/(R1*Ct) 1/(Ct*R1) ; 1/(Cm*R1) -1/(Cm*R1)-1/(R2*Cm)];
B = [ 1/Ct ; 0 ];
C = [ 0 1];

% Cálculo de la función de transferencia
ft = collect(simplify(C*inv((eye(2)*s)-A)*B));

% Visualización de la función de transferencia en fracción y en un recuadro
disp('La función de transferencia es: ')
pretty(ft) % Muestra en formato de fracción

