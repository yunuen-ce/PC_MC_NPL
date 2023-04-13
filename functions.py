import numpy as np
import pandas as pd


def get_line(filename: str, e_min: str = '0.001046'):
    """
    Finds the line where the data begins
    :param filename: name of the egs file
    :param e_min: min
    :return: lo que saca
    """
    file = open(filename, "r")
    for i, line in enumerate(file):
        if e_min in line:
            index = i
            mistake = False
            break
        else:
            index = 0
            mistake = True
    return index, mistake



def get_parameters(filename, n_bins: int, e_min: str):
    index, mistake = get_line(filename, e_min)
    if not mistake:
        df = pd.read_csv(filename, skiprows=int(index) - 1, header=None, skipinitialspace=True, delim_whitespace=True,
                         nrows=n_bins)
        e_raw = np.array(df[0])
        f_e_raw = np.array(df[1])
        s_f_e_raw = np.array(df[2])
    else:
        empty_array = np.zeros(n_bins)
        empty_array[:] = np.nan
        e_raw = empty_array
        f_e_raw = empty_array
        s_f_e_raw = empty_array
    return e_raw, f_e_raw, s_f_e_raw, mistake


def read_files(n_files, path, basename_files, n_bins: int, e_min):
    f_e_raw = np.zeros((n_bins, n_files))
    s_f_e_raw = np.zeros((n_bins, n_files))
    mistakes = 0

    for i in range(n_files):
        filename = path + basename_files + str(i + 1) + ".egslog"
        e, f_e, s_f_e, mistake = get_parameters(filename, n_bins, e_min)
        f_e_raw[:, i] = f_e
        s_f_e_raw[:, i] = s_f_e
        if mistake:
            mistakes += 1
    return e, f_e_raw, mistakes


def recombine_electron_fluence(e_raw, f_e_raw, sim_mistake, n_bins, n_files=112):
    en = e_raw
    f_e = np.zeros(n_bins)
    s_f_e = np.zeros(n_bins)

    for b in range(n_bins):
        f_e[b] = np.nanmean(f_e_raw[b, :])
        # Uncertainty
        s_f_e[b] = np.nanstd(f_e_raw[b, :]) / (np.sqrt(n_files - sim_mistake))

    return en, f_e,  s_f_e

# dose

def get_line_dose(filename: str, loc: str = 'Cavity dose'):
    file = open(filename, "r")
    for i, line in enumerate(file):
        if loc in line:
            index = i
            mistake = False
            break
        else:
            index = 0
            mistake = True
    return index, mistake


def get_dose(filename):
    index, mistake = get_line_dose(filename)
    if mistake:
        dose = np.nan
    else:
        with open(filename) as f:
            cavity_dose = f.readlines()[index + 2][25:38]
            dose = float(cavity_dose)
    return dose, mistake


def recombine_dose(path, basename, n_files):
    dose_raw = np.zeros(n_files)
    mistake = 0
    for i in range(n_files):
        filename = path + basename + str(i + 1) + ".egslog"
        dose_raw[i], error = get_dose(filename)
        if error:
            mistake = mistake + 1
            dose_raw[i] = np.nan
            #print(mistake)
    dose = np.nanmean(dose_raw)
    s_dose = np.nanstd(dose_raw) / np.sqrt(n_files - mistake)
    r_dose = s_dose / dose
    return dose, s_dose, r_dose

def get_pdd(filename, n_points):
    index, mistake = get_line_dose(filename)
    pdd = np.zeros(n_points)
    if mistake:
        pdd = np.nan
    else:
        with open(filename) as f:
            data = pd.read_csv(filename, skiprows=int(index+2), header=None, skipinitialspace=True,
                               delim_whitespace=True, nrows=n_points)
            pdd = data[1]
    return pdd, mistake

def recombine_pdd(path, basename, n_files, n_points):
    data_raw = np.zeros([n_files, n_points])
    mistake = 0
    for i in range(n_files):
        filename = path + basename + str(i + 1) + ".egslog"
        data_raw[i], error = get_pdd(filename, n_points)
        if error:
            mistake = mistake + 1
            data_raw[i] = np.nan
            print('mistake')

    data = np.nanmean(data_raw, axis=0)

    s_data = np.nanstd(data_raw, axis=0) / np.sqrt(n_files - mistake)
    return data, s_data

