% Performance Comparison: bsw07 vs PD-CP-ABE (Updated Data)

% Data for Setup
setup_avg = [0.041434, 0.010532];
setup_std = [0.000498, 0.000093];

% Data for Keygen
keygen_avg_5 = [0.025796, 0.029930];
keygen_std_5 = [0.000137, 0.000063];

keygen_avg_10 = [0.077731, 0.078379];
keygen_std_10 = [0.028465, 0.028437];

keygen_avg_20 = [0.103540, 0.128467];
keygen_std_20 = [0.005346, 0.047085];

keygen_avg_30 = [0.151705, 0.178180];
keygen_std_30 = [0.007741, 0.055502];

% Data for Encryption
encryption_avg_5 = [0.151322, 0.165196];
encryption_std_5 = [0.004748, 0.053204];

encryption_avg_10 = [0.249540, 0.316717];
encryption_std_10 = [0.002493, 0.056390];

encryption_avg_30 = [0.689024, 0.542301];
encryption_std_30 = [0.003680, 0.001850];

encryption_avg_50 = [1.306776, 0.729781];
encryption_std_50 = [0.114855, 0.005455];

encryption_avg_100 = [2.458105, 0.858643];
encryption_std_100 = [0.092807, 0.084340];

encryption_avg_160 = [3.672614, 0.857414];
encryption_std_160 = [0.023932, 0.005710];

encryption_avg_320 = [6.790536, 0.861576];
encryption_std_320 = [0.123901, 0.016801];

encryption_avg_640 = [13.253056, 0.887924];
encryption_std_640 = [0.108999, 0.084230];

encryption_avg_1280 = [26.905652, 0.892573];
encryption_std_1280 = [0.269045, 0.084457];

encryption_avg_1500 = [31.552992, 0.871881];
encryption_std_1500 = [0.199178, 0.016854];

% Data for Decryption
decryption_avg_5 = [0.039626, 0.035808];
decryption_std_5 = [0.002317, 0.000097];

decryption_avg_10 = [0.039665, 0.070226];
decryption_std_10 = [0.001077, 0.000217];

decryption_avg_30 = [0.098162, 0.129051];
decryption_std_30 = [0.002947, 0.001769];

decryption_avg_50 = [0.170649, 0.150873];
decryption_std_50 = [0.004676, 0.000244];

decryption_avg_100 = [0.354277, 0.181611];
decryption_std_100 = [0.010101, 0.000216];

decryption_avg_160 = [0.567469, 0.187640];
decryption_std_160 = [0.011939, 0.000217];

decryption_avg_320 = [1.108902, 0.189139];
decryption_std_320 = [0.024803, 0.000384];

decryption_avg_640 = [2.194026, 0.189400];
decryption_std_640 = [0.043844, 0.000239];

decryption_avg_1280 = [4.378460, 0.190331];
decryption_std_1280 = [0.093277, 0.000626];

decryption_avg_1500 = [5.111895, 0.190233];
decryption_std_1500 = [0.104495, 0.000253];

% Plot Setup
figure;
bar([1 2], setup_avg);
hold on;
errorbar([1 2], setup_avg, setup_std, '.k', 'LineWidth', 1.5);
set(gca, 'XTickLabel', {'bsw07', 'PD-CP-ABE'});
title('Setup Time Comparison');
ylabel('Execution Time (seconds)');
grid on;
saveas(gcf, 'setup_comparison.png');

% Plot Keygen
figure;
atoms = [5, 10, 20, 30];
bsw07_keygen_avg = [keygen_avg_5(1), keygen_avg_10(1), keygen_avg_20(1), keygen_avg_30(1)];
myabe_keygen_avg = [keygen_avg_5(2), keygen_avg_10(2), keygen_avg_20(2), keygen_avg_30(2)];
bsw07_keygen_std = [keygen_std_5(1), keygen_std_10(1), keygen_std_20(1), keygen_std_30(1)];
myabe_keygen_std = [keygen_std_5(2), keygen_std_10(2), keygen_std_20(2), keygen_std_30(2)];

errorbar(atoms, bsw07_keygen_avg, bsw07_keygen_std, '-ob', 'LineWidth', 1.5);
hold on;
errorbar(atoms, myabe_keygen_avg, myabe_keygen_std, '-or', 'LineWidth', 1.5);
title('Keygen Time Comparison');
xlabel('Number of Attributes/Atoms');
ylabel('Execution Time (seconds)');
legend('bsw07', 'PD-CP-ABE');
grid on;
saveas(gcf, 'keygen_comparison.png');

% Plot Encryption
figure;
atoms_encryption = [5, 10, 30, 50, 100, 160, 320, 640, 1280, 1500];
bsw07_encryption_avg = [encryption_avg_5(1), encryption_avg_10(1), encryption_avg_30(1), encryption_avg_50(1), encryption_avg_100(1), encryption_avg_160(1), encryption_avg_320(1), encryption_avg_640(1), encryption_avg_1280(1), encryption_avg_1500(1)];
myabe_encryption_avg = [encryption_avg_5(2), encryption_avg_10(2), encryption_avg_30(2), encryption_avg_50(2), encryption_avg_100(2), encryption_avg_160(2), encryption_avg_320(2), encryption_avg_640(2), encryption_avg_1280(2), encryption_avg_1500(2)];
bsw07_encryption_std = [encryption_std_5(1), encryption_std_10(1), encryption_std_30(1), encryption_std_50(1), encryption_std_100(1), encryption_std_160(1), encryption_std_320(1), encryption_std_640(1), encryption_std_1280(1), encryption_std_1500(1)];
myabe_encryption_std = [encryption_std_5(2), encryption_std_10(2), encryption_std_30(2), encryption_std_50(2), encryption_std_100(2), encryption_std_160(2), encryption_std_320(2), encryption_std_640(2), encryption_std_1280(2), encryption_std_1500(2)];

errorbar(atoms_encryption, bsw07_encryption_avg, bsw07_encryption_std, '-ob', 'LineWidth', 1.5);
hold on;
errorbar(atoms_encryption, myabe_encryption_avg, myabe_encryption_std, '-or', 'LineWidth', 1.5);
title('Encryption Time Comparison');
xlabel('Number of Attributes/Atoms');
ylabel('Execution Time (seconds)');
legend('bsw07', 'PD-CP-ABE');
grid on;
saveas(gcf, 'encryption_comparison.png');

% Plot Decryption
figure;
atoms_decryption = [5, 10, 30, 50, 100, 160, 320, 640, 1280, 1500];
bsw07_decryption_avg = [decryption_avg_5(1), decryption_avg_10(1), decryption_avg_30(1), decryption_avg_50(1), decryption_avg_100(1), decryption_avg_160(1), decryption_avg_320(1), decryption_avg_640(1), decryption_avg_1280(1), decryption_avg_1500(1)];
myabe_decryption_avg = [decryption_avg_5(2), decryption_avg_10(2), decryption_avg_30(2), decryption_avg_50(2), decryption_avg_100(2), decryption_avg_160(2), decryption_avg_320(2), decryption_avg_640(2), decryption_avg_1280(2), decryption_avg_1500(2)];
bsw07_decryption_std = [decryption_std_5(1), decryption_std_10(1), decryption_std_30(1), decryption_std_50(1), decryption_std_100(1), decryption_std_160(1), decryption_std_320(1), decryption_std_640(1), decryption_std_1280(1), decryption_std_1500(1)];
myabe_decryption_std = [decryption_std_5(2), decryption_std_10(2), decryption_std_30(2), decryption_std_50(2), decryption_std_100(2), decryption_std_160(2), decryption_std_320(2), decryption_std_640(2), decryption_std_1280(2), decryption_std_1500(2)];

errorbar(atoms_decryption, bsw07_decryption_avg, bsw07_decryption_std, '-ob', 'LineWidth', 1.5);
hold on;
errorbar(atoms_decryption, myabe_decryption_avg, myabe_decryption_std, '-or', 'LineWidth', 1.5);
title('Decryption Time Comparison');
xlabel('Number of Attributes/Atoms');
ylabel('Execution Time (seconds)');
legend('bsw07', 'PD-CP-ABE');
grid on;
saveas(gcf, 'decryption_comparison.png');
