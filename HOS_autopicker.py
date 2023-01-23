# Higher-order statistics automatic picker.

'''
This code was developed at the High Pressure and Temperature Lab
at Utrecht University, to pick first arrivals in acoustic emission (AE)
waveforms from friction experiments.

This code is meant to work with AE waveforms collected in block
(also known as "trigger") mode.

The goal is to produce an automatic picker of first arrivals that
does not require multiple parameters.

To apply the code to individual waveforms, type:

import HOS_autopicker as hosa
pick_index = hosa.autopicker(trace, N)

where 'trace' is an AE trace in the form of a 1D Numpy array, and N is an integer.
The output of the autopicker is the index of the sample that corresponds to the
first arrival, NOT the first arrival time.

The idea is that the first arrival corresponds to the minimum of an Akaike
information criterion (AIC) function from Zhang et al., 2003
(https://doi.org/10.1785/0120020241). The accuracy of AIC-based picking improves
when the AIC function is evaluated in the vicinity of the first arrival (as opposed
to evaluated for the entire waveform). Thus, to obtain a rough estimate of the
first arrival, the autopicker will first calculate the expanding kurtosis (EK) of
the input waveform. EK will be maximum shortly after the first arrival. The
autopicker will then look for the first arrival by calculating the AIC function
only in the N samples of the waveform preceeding the maximum of the EK function.

For more details, see: Korkolis et al. (2021): A Laboratory Perspective on the
Gutenberg‐Richter and Characteristic Earthquake Models. Journal of Geophysical
Research - Solid Earth. DOI: https://doi.org/10.1029/2021JB021730.

Author: Evangelos Korkolis, ekorko@gmail.com
'''

import numpy as np
import pandas as pd


def expanding_kurtosis(trace):
    ''' Pandas-optimized online kurtosis function. '''
    return pd.Series(trace).expanding().kurt()


def aic_zhang(trace):
    ''' This is the Pandas-optimized AIC function from Zhang et al., 2003 (BSSA).
    It accepts 1D numpy arrays as input.
    
    Format: aic_array = aic_zhang(signal)

    AIC(k)=k*log(variance(x[1,k]))+(n-k-1)*log(variance(x[k+1,n]))
    x: data (eg: ch1, ch2, ch3, ch4, ...)
    n: length of data
    k: variable that goes through x
    
    '''
    
    waveform = pd.Series(trace)
    
    n = len(waveform)
        
    aic = np.zeros((n))
    
    exp_var = np.log10(np.array(waveform.expanding(1).var()))
    rev_exp_var = np.log10(np.array(waveform.sort_index(ascending=False).expanding(1).var()))
    
    for k in np.arange(0, n):
        aic[k] = k*exp_var[k] + (n-k-1)*rev_exp_var[n-k-1]
        
    # mask negative infs
    aic[np.isneginf(aic)] = 0
    
    # mask nans
    aic[np.isnan(aic)] = 0
    
    return aic


def autopicker(trace, aic_backstep_samples):
    ''' Provide a trace and the AIC backstep (number of samples) '''
    
    # calculate expanding kurtosis CF
    cfk = expanding_kurtosis(trace)
    indx_k = np.where(cfk/np.max(cfk) > 0.99)[0][0]
    
    # calculate rolling AIC CF
    cfaic = aic_zhang(trace[indx_k - aic_backstep_samples:indx_k])
    
    return (indx_k - aic_backstep_samples) + np.argmin(cfaic)

