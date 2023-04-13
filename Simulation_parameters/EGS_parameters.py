import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Results for simulations using an EJ-204 scintillator
df = pd.read_csv('mc_macro_emestepe_results.txt', delimiter='\t', on_bad_lines='skip',
                 names= ['Macro', 'Bfield', 'EM_ESTEPE', 'Dose','rel_unc', 'abs_unc', 'Histperhour', 'Histories', 'CPU_time'])


EEMF = df[df['Macro'] == 'EEMF']
emf = df[df['Macro'] == 'emf']


plt.errorbar(EEMF.EM_ESTEPE, EEMF.Dose/df.Dose[0], yerr=(EEMF.Dose/df.Dose[0]) * np.sqrt( (EEMF.rel_unc/100)**2 + (df.rel_unc[0]/100)**2 ) , marker = 's', linestyle=':', label = 'EEMF')
plt.errorbar(emf.EM_ESTEPE, emf.Dose/df.Dose[0], yerr=(emf.Dose/df.Dose[0]) * np.sqrt( (emf.rel_unc/100)**2 + (df.rel_unc[0]/100)**2 ),  marker = 'o', linestyle=':', label = 'emf')
plt.xlabel('EM ESTEPE')
plt.ylabel('Normalized dose to 0 T ')
plt.legend()
plt.tight_layout()
plt.savefig("norm_dose_parameters.eps")
plt.show()

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
plt.subplot(121)
plt.title('EJ-204, 1.5 T')
plt.errorbar(EEMF.EM_ESTEPE, EEMF.Dose, yerr=EEMF.abs_unc, marker = 's', linestyle=':', label = 'EEMF')
plt.errorbar(emf.EM_ESTEPE, emf.Dose, yerr=emf.abs_unc, marker = 'o', linestyle=':', label = 'emf')
plt.xlabel('EM ESTEPE')
plt.ylabel('Dose per incident photon')
plt.legend()

plt.subplot(122)
plt.plot(EEMF.EM_ESTEPE, EEMF.Histperhour,  marker = 's', linestyle=':', label = 'EEMF')
plt.plot(emf.EM_ESTEPE, emf.Histperhour,  marker = 'o', linestyle=':', label = 'emf')
plt.xlabel('EM ESTEPE')
plt.ylabel('Histories per hour')
plt.legend()
plt.tight_layout()
plt.savefig("dose_parameters_egs.eps")
plt.show()