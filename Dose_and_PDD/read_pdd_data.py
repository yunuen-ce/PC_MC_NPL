# Read pdd data from EGSnrc

from functions import *

path = '/Users/yun/Documents/MC_Npl/EGSdata/PDD/7cm/'

n_files = 360

scintillator = ['full', 'pvtpb', 'water']
# Arrays for the pdd for the 7 x 7 cm2 field
bfields = [0, 0.5, 1, 1.5, -1.5]
bfields_char = ['0', '05', '1', '15', '-15']
pdd_water_7cm = np.zeros([len(bfields), 2, 20])
pdd_pvtpb_7cm = np.zeros([len(bfields), 2, 20])
pos = np.arange(0, 10, 0.5)
pdd_full_7cm = np.zeros([len(bfields), 2, 40])
pos_full = np.arange(0.25, 10.25, 0.25)
# Arrays for the pdd for the 1 x 1 cm2 field, only computed for the full scintillator
bfields2 = [0, 0.35, 0.5, 1, 1.5, -1.5]
bfields_char2 = ['0', '035', '05', '1', '15', '-15']
pdd_full_1cm = np.zeros([len(bfields2), 2, 40])
pdd_EE = np.zeros([2, 20])

# Reference field : 7 x 7 cm2
for s in range(len(scintillator)):
    for b in range(len(bfields)):
        basename = "PDD_" + scintillator[s] + "_7cm_" + bfields_char[b] + "T_w"
        if s == 0:
            n_points = 40
            pdd_full_7cm[b, 0, :], pdd_full_7cm[b, 1, :] = recombine_pdd(path, basename, n_files, n_points)
        elif s == 1:
            if b==len(bfields)-1:
                continue
            else:
                n_points = 20
                pdd_pvtpb_7cm[b, 0, :], pdd_pvtpb_7cm[b, 1, :] = recombine_pdd(path, basename, n_files, n_points)
        else :
            if b==len(bfields)-1:
                continue
            else:
                n_points = 20
                pdd_water_7cm[b, 0, :], pdd_water_7cm[b, 1, :] = recombine_pdd(path, basename, n_files, n_points)


#####################
# Small fields
path = '/Users/yun/Documents/MC_Npl/EGSdata/PDD/5cm/'
n_points = 40

s = 0
for b in range(len(bfields2)):
    basename = "PDD_" + scintillator[s] + "_1cm_" + bfields_char2[b] + "T_w"
    if b == 0 or b == 4:
        n_files = 360
    else:
        n_files = 120
    pdd_full_1cm[b, 0, :], pdd_full_1cm[b, 1, :] = recombine_pdd(path, basename, n_files, n_points)

# Influence of EM ESTEPE
path = '/Users/yun/Documents/MC_Npl/EGSdata/PDD/7cm/'
basename = 'PDD_water_7cm_EE0005_15T_w'
pdd_EE[0], pdd_EE[1] = recombine_pdd(path, basename, n_files=360, n_points=20)

np.savez('data_pdd.npz', pdd_pvtpb_7cm=pdd_pvtpb_7cm, pdd_water_7cm=pdd_water_7cm, pdd_full_7cm=pdd_full_7cm,
         pos_full=pos_full, pdd_full_1cm=pdd_full_1cm, pdd_EE=pdd_EE, pos=pos)
