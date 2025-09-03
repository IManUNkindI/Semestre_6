% Parcial 2 Modelos Punto 1 Sistema Termico
clc, clear

syms s R1 R2 C1 C2

% Matrices d.▼el sistema
A = [ -1/(R1*C1) 1/(C1*R2) ; 1/(C2*R2) -1/(C2*R2)];
B = [ 1/(R1*C1) ; 0 ];
C = [ 1 0];

% Cálculo de la función de transferencia
ft = collect(simplify(C*inv((eye(2)*s)-A)*B));

% Visualización de la función de transferencia en fracción y en un recuadro
disp('La función de transferencia es: ')
pretty(ft) % Muestra en formato de fracción
