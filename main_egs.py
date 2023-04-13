from functions import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# electron fluence
path = '/Users/yun/Documents/MC_Npl/EGSdata/'
n_bins = 80
n_files = 360
e_min = '0.001058'
bfields = [-1.5, -1, -0.5, -0.35, -0.2, 0, 0.2, 0.35, 0.5, 1, 1.5]

j = bfields.index(0)
scintillator = ['water', 'ej204_08Pb', 'ej204']
scint_label = ['water', 'Medscint', 'EJ-204']
dose = np.zeros([len(scintillator), len(bfields), 3])
en = np.zeros([len(scintillator), len(bfields), 80])
f_e = np.zeros([len(scintillator), len(bfields), 80])
s_f_e = np.zeros([len(scintillator), len(bfields), 80])
# filename = path + basename_files + '1.egslog'
bfields_char = ['-15', '-1', '-05', '-035', '-02', '0', '02', '035', '05', '1', '15']
bfields_char2 = ['-15', '0', '15']
colors = ['tomato', 'deepskyblue', 'mediumseagreen', 'purple', 'grey', 'darkorange', 'plum', 'black', ]


for s in range(len(scintillator)):
    for b in range(len(bfields)):
        if s == 2 and bfields_char[b] not in bfields_char2:
            continue
        else:
            basename_files = "Perp_" + scintillator[s] + "_7cm_" + bfields_char[b] + "T_w"
            e_raw, f_e_raw, mistakes = read_files(n_files, path, basename_files, n_bins, e_min)
            en[s, b, :], f_e[s, b, :], s_f_e[s, b, :] = recombine_electron_fluence(e_raw, f_e_raw, mistakes, n_bins,
                                                                                   n_files)
            dose[s, b, :] = recombine_dose(path, basename_files, n_files)

        if s==1:
            plt.errorbar(en[s, b, :], f_e[s, b, :], s_f_e[s, b, :],  label= scintillator[s] + ', ' + str(bfields[b]) + 'T')

print(dose)

plt.xscale('log')
plt.legend(framealpha=1, frameon=True, loc='best')
plt.show()

figure(figsize=(11, 7))
for s in range(len(scintillator)):
    plt.errorbar(np.abs(bfields[:j + 1]), dose[s, :j + 1, 0] / dose[s, j, 0],
                 yerr=np.sqrt(dose[s, :j + 1, 2] ** 2 + dose[s, j, 2] ** 2), fmt='-o', color=colors[s],
                 label=scint_label[s] + ' e- \u2192 stem')
    plt.errorbar(np.abs(bfields[j:]), dose[s, j:, 0] / dose[s, j, 0],
                 yerr=np.sqrt(dose[s, j:, 2] ** 2 + dose[s, j, 2] ** 2), fmt=':o', color=colors[s],
                 label=scint_label[s] + ' e- \u2192 tip')

# plt.plot(bfields, dose[:, 0]/dose[1, 0])

plt.legend(framealpha=1, frameon=True, loc='upper center')
plt.xlabel('Magnetic field [T]')
plt.ylabel('D/D(0 T)')
plt.ylim(0.985, 1.01)
plt.legend(loc='best', bbox_to_anchor=(1.2, 0.5))
plt.tight_layout()
plt.show()

# Dose
