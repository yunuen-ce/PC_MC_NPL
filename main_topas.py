from topas_functions import *
import matplotlib.pyplot as plt
from nomalization import *
from functions import *

# EGS
path = '/Users/yun/Documents/MC_Npl/EGSdata/'
#path = '/Users/yun/Documents/MC_electron_fluence/MC_topas/Cerenkov_simulations/NPL_simulations/Electron_fluence_phsp_sim/Data_cluster/'
#basename_files = "Perp_water_7cm_0T_w"
n_bins = 80
n_files = 360
e_min = '0.001058'
bfields = [0] #[-1.5, -1, -0.5, -0.35, -0.2,  0, 0.2, 0.35, 0.5,  1,  1.5]
j = bfields.index(0)
bfields_char = ['0'] #['-15', '-1', '-05', '-035', '-02', '0', '02', '035', '05', '1', '15']
# water, ej-204-
scintillator = ['water', 'ej204_08Pb']
dose = np.zeros([2, len(bfields), 3])
en = np.zeros([len(scintillator), len(bfields), 80])
f_e = np.zeros([len(scintillator), len(bfields), 80])
s_f_e = np.zeros([len(scintillator), len(bfields), 80])
# TOPAS
path_topas = '/Users/yun/Documents/MC_Npl/TOPASdata/'
n_bins = 5999
basename_topasfile = 'EF_Scintillator_0T_'

e_0, f_0, s_f_0 = recombine_files_2(path_topas, basename_topasfile, n_bins, e_min=0.001, e_max=6, n_files=31,
                                    histories=100000000, skiplines=7)
n_e_0, n_f_0, n_s_f_0 = normalization_1keV(e_0, f_0, s_f_0, n_bins)

n_bins = 80
basename_topasfile = 'EF_Scintillator_log_0T_'

e_0_l, f_0_l, s_f_0_l = recombine_files_log(path_topas, basename_topasfile, n_bins, e_min=0.001, e_max=6, n_files=36,
                                            histories=100000000, skiplines=7)
n_e_0_l, n_f_0_l, n_s_f_0_l = normalization(e_0_l, f_0_l, s_f_0_l, n_bins)

plt.figure(1, figsize=(9, 7.5))
plt.plot(n_e_0, n_f_0, ls=':', label="Topas 0 T ")
plt.plot(n_e_0_l, n_f_0_l, ls=':', label="Topas log ")
plt.xlabel('Energy [MeV]')
#plt.xlim([0.01, 6])
#plt.yscale("log")
plt.show()

for s in range(len(scintillator)):
    for b in range(len(bfields_char)):

        basename_files = "Perp_" + scintillator[s] + "_7cm_" + bfields_char[b] + "T_w"
        e_raw, f_e_raw, mistakes = read_files(n_files, path, basename_files, n_bins, e_min)
        en[s, b, :], f_e[s, b, :], s_f_e[s, b, :] = recombine_electron_fluence(e_raw, f_e_raw, mistakes, n_bins, n_files)
        dose[s, b, :] = recombine_dose(path, basename_files, n_files)
        n_en[s, b, :], n_f_e[s, b, :], n_s_f_e[s, b, :] = normalization(n[s, b, :], f_e[s, b, :], s_f_e[s, b, :], 80)

        plt.errorbar(en[s, b, :], f_e[s, b, :], s_f_e[s, b, :],  label= scintillator[s] + ', ' + str(bfields[b]) + 'T')
        plt.plot(e_0, f_0, ls=':', label="Topas 0 T ")
        plt.plot(e_0_l, f_0_l, ls=':', label="Topas log ")
plt.xscale('log')
plt.legend(framealpha=1, frameon=True, loc='best')
plt.show()