import matplotlib.pyplot as plt
import numpy as np

# Load data
data = np.load('data_pdd.npz')
pdd_full_7cm = data['pdd_full_7cm']
pos_full = data['pos_full']
pdd_full_1cm = data['pdd_full_1cm']
pdd_EE = data['pdd_EE']
pos = data['pos']
pdd_water_7cm = data['pdd_water_7cm']
pdd_pvtpb_7cm = data['pdd_pvtpb_7cm']

bfields = [0, 0.5, 1, 1.5, -1.5]
bfields_char = ['0', '05', '1', '15', '-15']
scintillator = ['full', 'pvtpb', 'water']
bfields2 = [0, 0.35, 0.5, 1, 1.5, -1.5]
bfields_char2 = ['0', '035', '05', '1', '15', '-15']

# Figures
# Comparison Water and full model
b=0
plt.errorbar(pos, pdd_water_7cm[b, 0, :], yerr=pdd_water_7cm[b, 1, :], linestyle='--', label='water, ' + str(bfields[b]) + ' T')
plt.errorbar(pos_full, pdd_full_7cm[b, 0, :], yerr=pdd_full_7cm[b, 1, :],  linestyle='--',label='full, ' + str(bfields[b]) + ' T')
b=3
plt.errorbar(pos, pdd_water_7cm[b, 0, :], yerr=pdd_water_7cm[b, 1, :],  linestyle=':', label='water, ' + str(bfields[b]) + ' T')
plt.errorbar(pos_full, pdd_full_7cm[b, 0, :], yerr=pdd_full_7cm[b, 1, :],  linestyle=':',  label='full, ' + str(bfields[b]) + ' T')
plt.axvline(x=5, color='black', ls=':')
plt.xlabel('Position [cm]')
plt.ylabel('Dose per incident photon')
plt.legend()
plt.show()


# Dose and PDD in water
fig = plt.subplots(1, 2, figsize=(9, 4))
for b in range(len(bfields)):
    if b == len(bfields) - 1:
        continue
    else:
        plt.subplot(1, 2, 1)
        plt.errorbar(pos, pdd_water_7cm[b, 0, :], yerr=pdd_water_7cm[b, 1, :], label=str(bfields[b]) + 'T')
        plt.title('Water')
        plt.axvline(x=5, ls=':')
        plt.xlabel('Position [cm]')
        plt.ylabel('Dose per incident photon')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.errorbar(pos, pdd_water_7cm[b, 0, :] / max(pdd_water_7cm[b, 0, :]) * 100,
                     yerr=(pdd_water_7cm[b, 0, :] / max(pdd_water_7cm[b, 0, :]) * 100) *
                          np.sqrt(pdd_water_7cm[b, 1, :] ** 2 + (
                                      pdd_water_7cm[b, 1, np.argmax(pdd_water_7cm[b, 0, :])] ** 2)),
                     label=str(bfields[b]) + 'T')

        plt.title('Water')
        plt.axvline(x=5, ls=':')
        plt.xlabel('Position [cm]')
        plt.ylabel('PDD [%]')
        plt.legend()
plt.savefig('ppd_dose_water.eps')
plt.show()


# Dose and PDD in pvt +pb
fig = plt.subplots(1, 2, figsize=(9, 4))
for b in range(len(bfields)):
    if b == len(bfields) - 1:
        continue
    else:
        plt.subplot(1, 2, 1)
        plt.errorbar(pos, pdd_pvtpb_7cm[b, 0, :], yerr=pdd_pvtpb_7cm[b, 1, :], label=str(bfields[b]) + 'T')
        plt.title('pvtpb')
        plt.axvline(x=5, ls=':')
        plt.xlabel('Position [cm]')
        plt.ylabel('Dose per incident photon')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.errorbar(pos, pdd_pvtpb_7cm[b, 0, :] / max(pdd_pvtpb_7cm[b, 0, :]) * 100,
                     yerr=(pdd_pvtpb_7cm[b, 0, :] / max(pdd_pvtpb_7cm[b, 0, :]) * 100) *
                          np.sqrt(pdd_pvtpb_7cm[b, 1, :] ** 2 + (
                                      pdd_pvtpb_7cm[b, 1, np.argmax(pdd_pvtpb_7cm[b, 0, :])] ** 2)),
                     label=str(bfields[b]) + 'T')

        plt.title('pvtpb')
        plt.axvline(x=5, ls=':')
        plt.xlabel('Position [cm]')
        plt.ylabel('PDD [%]')
        plt.legend()
plt.savefig('ppd_dose_pvtpb.eps')
plt.show()

# Dose and PDD in full model
fig = plt.subplots(1, 2, figsize=(9, 4))
for b in range(len(bfields)):
    if b == len(bfields) - 1:
        continue
    else:
        plt.subplot(1, 2, 1)
        plt.errorbar(pos_full, pdd_full_7cm[b, 0, :], yerr=pdd_full_7cm[b, 1, :], label=str(bfields[b]) + 'T')
        plt.title('full')
        plt.axvline(x=5, ls=':')
        plt.xlabel('Position [cm]')
        plt.ylabel('Dose per incident photon')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.errorbar(pos_full, pdd_full_7cm[b, 0, :] / max(pdd_full_7cm[b, 0, :]) * 100,
                     yerr=(pdd_full_7cm[b, 0, :] / max(pdd_full_7cm[b, 0, :]) * 100) *
                          np.sqrt(pdd_full_7cm[b, 1, :] ** 2 + (
                                      pdd_full_7cm[b, 1, np.argmax(pdd_full_7cm[b, 0, :])] ** 2)),
                     label=str(bfields[b]) + 'T')

        plt.title('full')
        plt.axvline(x=5, ls=':')
        plt.xlabel('Position [cm]')
        plt.ylabel('PDD [%]')
        plt.legend()
plt.savefig('ppd_dose_full.eps')
plt.show()

# Small fields

b=0
plt.errorbar(pos_full, pdd_full_1cm[b, 0, :] / max(pdd_full_1cm[b, 0, :]) * 100, yerr=pdd_full_1cm[b, 1, :],
                 label=bfields_char2[b] + 'T, 1 x 1 cm2')
plt.errorbar(pos_full, pdd_full_7cm[b, 0, :] / max(pdd_full_7cm[b, 0, :]) * 100, yerr=pdd_full_7cm[b, 1, :],
                 label=bfields_char2[b] + 'T, 7 x 7 cm2')

b=4
plt.errorbar(pos_full, pdd_full_1cm[b, 0, :] / max(pdd_full_1cm[b, 0, :]) * 100,  yerr=pdd_full_1cm[b, 1, :],
                 linestyle='--', label=str(bfields2[b]) + 'T, 1 x 1 cm2')
b=3
plt.errorbar(pos_full, pdd_full_7cm[b, 0, :] / max(pdd_full_7cm[b, 0, :]) * 100, yerr=pdd_full_7cm[b, 1, :],
                 linestyle='--', label=str(bfields[b]) + 'T, 7 x 7 cm2')
plt.axvline(x=5, color='black', ls=':')
plt.ylabel('PDD[%]')
plt.xlabel('Position [cm]')
plt.legend(framealpha=1, frameon=True, loc='best')
plt.savefig('ppd_full_1cm_7cm.eps')
plt.show()

