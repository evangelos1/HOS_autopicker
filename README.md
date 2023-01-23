# HOS_autopicker
Higher-order statistics automatic picker for acoustic emission (AE) waveforms.

The goal is to create an automatic picker with as few tweakable parameters as possible.

This code is meant to be used with individual AE waveforms collected in block (aka "trigger") mode. The original application of the code was the detection of first arrivals from AE waveforms collected during stick-slip experiments on glass bead aggregates (see: Korkolis et al., 2021: A Laboratory Perspective on the Gutenberg‐Richter and Characteristic Earthquake Models, JGR Solid Earth. DOI: https://doi.org/10.1029/2021JB021730). Modifications may be required to apply the code to AE data collected in other ways.

This work has been inspired by the following publications:

1. Zhang et al., 2003: Automatic P-Wave Arrival Detection and Picking with Multiscale Wavelet Analysis for Single-Component Recordings. BSSA. DOI: https://doi.org/10.1785/0120020241.

2. Kueperkoch et al., 2010: Automated determination of P-phase arrival times at regional and local distances using higher order statistics. GJI. DOI: https://doi.org/10.1111/j.1365-246X.2010.04570.x.
