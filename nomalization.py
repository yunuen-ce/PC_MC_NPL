import numpy as np


def normalization(energy, fluence, std, n_bins):
    """
    Normalization of the spectra to compare between the two
    Spectrum columns: energy, fluence, standard deviation
    :param energy:
    :param fluence:
    :param std:
    :param n_bins:
    :return:
    """
    s_n = np.empty([n_bins])
    area = np.empty([n_bins])
    s_area = np.empty([n_bins])
    for i in range(n_bins):
        if i == 0:
            bin_width = energy[i]
        else:
            bin_width = energy[i] - energy[i - 1]

        area[i] = fluence[i] * bin_width
        s_area[i] = np.sqrt(std[i] ** 2 * bin_width ** 2)

    area_total = np.nansum(area)
    s_area_total = np.sqrt(np.nansum(np.square(s_area)))

    for i in range(n_bins):
        if fluence[i] == 0:
            s_n[i] = 0
        else:
            s_n[i] = (fluence[i] / area_total) * np.sqrt((std[i] / fluence[i]) ** 2 + (s_area_total / area_total) ** 2)

    return energy, fluence / area_total, s_n


def normalization_1keV(energy, fluence, std, n_bins):
    s_n = np.empty([n_bins])
    area = np.empty([n_bins])
    s_area = np.empty([n_bins])
    for i in range(n_bins):
        bin_width = 0.001
        area[i] = fluence[i] * bin_width
        s_area[i] = np.sqrt(std[i] ** 2 * bin_width ** 2)

    area_total = np.nansum(area)
    s_area_total = np.sqrt(np.nansum(np.square(s_area)))

    for i in range(n_bins):
        if fluence[i] == 0:
            s_n[i] = 0
        else:
            s_n[i] = (fluence[i] / area_total) * np.sqrt((std[i] / fluence[i]) ** 2 + (s_area_total / area_total) ** 2)

    return energy, fluence/area_total, s_n
