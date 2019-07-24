# sim-sparky
Simulate 2D NMR spectra in SPARKY format from a peak list file.

## Description

Sim-Sparky is a python tool to simulate several types of 2D NMR spectra (i.e., HN-HSQC, HC-HSQC, NCA, NCO, DARR etc.) from a peak list files obtained from the BMRB database or ShiftX prediction server. The tool is built on top of NMRGlue, which allows it to simalute peaks as Gaussian lineshapes directly into Sparky format. A peak list file, also in Sparky format, is generated and can be loaded into Sparky with the spectrum.

## Examples

### 1H-15N HSQC of GB1
