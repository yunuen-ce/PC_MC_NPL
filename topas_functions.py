import numpy as np
import pandas as pd
import math


def read_topas_files(filename, n_bins=200, e_min=0.001, e_max=1.25, skiplines=7):
    df = pd.read_csv(filename, skiprows=skiplines, header=None).to_numpy()
    e_fluence = np.array(df[0][2:2 * n_bins + 1:2])
    s_e_fluence = np.array(df[0][3:2 * n_bins + 2:2])
    energy = np.linspace(e_min, e_max, n_bins)
    return energy, e_fluence, s_e_fluence


def read_topas_files_log(filename, n_bins=200, e_min=0.001, e_max=7, skiplines=7):
    df = pd.read_csv(filename, skiprows=skiplines, header=None).to_numpy()
    e_fluence = np.array(df[0][2:2 * n_bins + 1:2])
    s_e_fluence = np.array(df[0][3:2 * n_bins + 2:2])
    energy_log = energy_in_log(n_bins, e_min, e_max)
    return energy_log, e_fluence, s_e_fluence


def energy_in_log(n_bins=1000, e_min=0.001, e_max=7):
    energy_log = np.zeros(n_bins)
    bin_width = (math.log(e_max, 10) - math.log(e_min, 10)) / n_bins
    for i in range(n_bins):
        energy_log[i] = pow(10, math.log(e_min, 10) + i * bin_width)
    return energy_log


def recombine_files_1(path: str,
                      basename_topasfile: str,
                      n_bins: int,
                      e_min: float,
                      e_max: float,
                      n_files: int,
                      histories: int,
                      skiplines: int = 7):
    energy = np.zeros((1, n_bins))
    ef = np.zeros((n_files, n_bins))
    s_ef = np.zeros((n_files, n_bins))
    for i in range(n_files):
        topasfile = path + basename_topasfile + str(i + 1) + '.csv'
        energy, fluence, s_fluence = read_topas_files(topasfile, n_bins, e_min, e_max, skiplines)
        ef[i][:] = fluence
        s_ef[i][:] = s_fluence / np.sqrt(histories)

    """ Recombination: method 1 """
    mean_fluence = np.nanmean(ef, axis=0)
    unc_fluence = np.nanstd(s_ef, axis=0) / math.sqrt(n_files)
  #  rel_unc_fluence = (unc_fluence / mean_fluence) * 100

    return energy, mean_fluence, unc_fluence #, rel_unc_fluence


def recombine_files_2(path: str,
                      basename_topasfile: str,
                      n_bins: int,
                      e_min: float,
                      e_max: float,
                      n_files: int,
                      histories: int,
                      skiplines: int = 7):
    energy = np.zeros((1, n_bins))
    ef = np.zeros((n_files, n_bins))
    s_ef = np.zeros((n_files, n_bins))
    for i in range(n_files):
        topasfile = path + basename_topasfile + str(i + 1) + '.csv'
        energy, fluence, s_fluence = read_topas_files(topasfile, n_bins, e_min, e_max, skiplines)
        ef[i][:] = fluence
        s_ef[i][:] = s_fluence / np.sqrt(histories)

    '''Recombination: method 2 '''
    mean_fluence = np.nanmean(ef, axis=0)
    unc_fluence_2 = (1 / n_files) * np.sqrt(np.sum(np.square(s_ef), axis=0))
 #   rel_unc_fluence_2 = (unc_fluence_2 / mean_fluence) * 10

    return energy, mean_fluence, unc_fluence_2 #, rel_unc_fluence_2

def recombine_files_log(path: str,
                      basename_topasfile: str,
                      n_bins: int,
                      e_min: float,
                      e_max: float,
                      n_files: int,
                      histories: int,
                      skiplines: int = 7):
    energy = np.zeros((1, n_bins))
    ef = np.zeros((n_files, n_bins))
    s_ef = np.zeros((n_files, n_bins))
    for i in range(n_files):
        topasfile = path + basename_topasfile + str(i + 1) + '.csv'
        energy, fluence, s_fluence = read_topas_files_log(topasfile, n_bins, e_min, e_max, skiplines)
        ef[i][:] = fluence
        s_ef[i][:] = s_fluence / np.sqrt(histories)

    """ Recombination: method 1 """
    mean_fluence = np.nanmean(ef, axis=0)
    unc_fluence = np.nanstd(s_ef, axis=0) / math.sqrt(n_files)
  #  rel_unc_fluence = (unc_fluence / mean_fluence) * 100

    return energy, mean_fluence, unc_fluence
