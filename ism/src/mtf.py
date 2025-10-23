from math import pi
from config.ismConfig import ismConfig
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import j1
from numpy.matlib import repmat
from common.io.readMat import writeMat
from common.plot.plotMat2D import plotMat2D
from scipy.interpolate import interp2d
from numpy.fft import fftshift, ifft2
import os

class mtf:
    """
    Class MTF. Collects the analytical modelling of the different contributions
    for the system MTF
    """
    def __init__(self, logger, outdir):
        self.ismConfig = ismConfig()
        self.logger = logger
        self.outdir = outdir

    def system_mtf(self, nlines, ncolumns, D, lambd, focal, pix_size,
                   kLF, wLF, kHF, wHF, defocus, ksmear, kmotion, directory, band):
        """
        System MTF
        :param nlines: Lines of the TOA
        :param ncolumns: Columns of the TOA
        :param D: Telescope diameter [m]
        :param lambd: central wavelength of the band [m]
        :param focal: focal length [m]
        :param pix_size: pixel size in meters [m]
        :param kLF: Empirical coefficient for the aberrations MTF for low-frequency wavefront errors [-]
        :param wLF: RMS of low-frequency wavefront errors [m]
        :param kHF: Empirical coefficient for the aberrations MTF for high-frequency wavefront errors [-]
        :param wHF: RMS of high-frequency wavefront errors [m]
        :param defocus: Defocus coefficient (defocus/(f/N)). 0-2 low defocusing
        :param ksmear: Amplitude of low-frequency component for the motion smear MTF in ALT [pixels]
        :param kmotion: Amplitude of high-frequency component for the motion smear MTF in ALT and ACT
        :param directory: output directory
        :return: mtf
        """

        self.logger.info("Calculation of the System MTF")

        # Calculate the 2D relative frequencies
        self.logger.debug("Calculation of 2D relative frequencies")
        fn2D, fr2D, fnAct, fnAlt = self.freq2d(nlines, ncolumns, D, lambd, focal, pix_size)

        # Diffraction MTF
        self.logger.debug("Calculation of the diffraction MTF")
        print("Hasta aqui debugguea para ver los valores")
        Hdiff = self.mtfDiffract(fr2D)

        # Defocus
        Hdefoc = self.mtfDefocus(fr2D, defocus, focal, D)

        # WFE Aberrations
        Hwfe = self.mtfWfeAberrations(fr2D, lambd, kLF, wLF, kHF, wHF)

        # Detector
        Hdet  = self. mtfDetector(fn2D)

        # Smearing MTF
        Hsmear = self.mtfSmearing(fnAlt, ncolumns, ksmear)

        # Motion blur MTF
        Hmotion = self.mtfMotion(fn2D, kmotion)

        # Calculate the System MTF
        self.logger.debug("Calculation of the Sysmtem MTF by multiplying the different contributors")
        #Hsys = 1 # dummy
        Hsys = Hdiff * Hdefoc * Hwfe * Hdet * Hsmear * Hmotion  # dummy


        # Plot cuts ACT/ALT of the MTF
        self.plotMtf(Hdiff, Hdefoc, Hwfe, Hdet, Hsmear, Hmotion, Hsys, nlines, ncolumns, fnAct, fnAlt, directory, band)


        return Hsys

    def freq2d(self,nlines, ncolumns, D, lambd, focal, w):
        """
        Calculate the relative frequencies 2D (for the diffraction MTF)
        :param nlines: Lines of the TOA
        :param ncolumns: Columns of the TOA
        :param D: Telescope diameter [m]
        :param lambd: central wavelength of the band [m]
        :param focal: focal length [m]
        :param w: pixel size in meters [m]
        :return fn2D: normalised frequencies 2D (f/(1/w))
        :return fr2D: relative frequencies 2D (f/(1/fc))
        :return fnAct: 1D normalised frequencies 2D ACT (f/(1/w))
        :return fnAlt: 1D normalised frequencies 2D ALT (f/(1/w))
        """
        #TODO

        #hacemos la normalizacion de las frecuencias
        fsAlt = 1 / nlines / w
        fsAct = 1 / ncolumns / w

        #importante poner parentesis porque despues no sale bien
        eps = 1e-10
        fAlt = np.arange(-1 / (2 * w), 1 / (2 * w) - eps, fsAlt)

        fAct = np.arange(-1 / (2 * w), 1 / (2 * w) - eps, fsAct)

        fc = D / (lambd * focal)

        # Normalized 1D frequencies
        fnAct = fAct / (1 / w) #pones pareentesis porque sino se queda rayado
        fnAlt = fAlt / (1 / w)

        #frecuencias relativas
        # Relative 1D frequencies
        frAct = fAct / fc
        frAlt = fAlt / fc

        # 2D frequencies
        [fnAltxx, fnActxx] = np.meshgrid(fnAlt, fnAct, indexing='ij')
        fn2D = np.sqrt(fnAltxx ** 2 + fnActxx ** 2)
        [frAltxx, frActxx] = np.meshgrid(frAlt, frAct, indexing='ij')
        fr2D = np.sqrt(frAltxx ** 2 + frActxx ** 2)

        return fn2D, fr2D, fnAct, fnAlt


    def mtfDiffract(self,fr2D):
        """
        Optics Diffraction MTF
        :param fr2D: 2D relative frequencies (f/fc), where fc is the optics cut-off frequency
        :return: diffraction MTF
        """
        #TODO
        Hdiff = (2 / pi) * (np.arccos(fr2D) - fr2D * (1 - fr2D ** 2) ** (1 / 2))
        return Hdiff


    def mtfDefocus(self, fr2D, defocus, focal, D):
        """
        Defocus MTF
        :param fr2D: 2D relative frequencies (f/fc), where fc is the optics cut-off frequency
        :param defocus: Defocus coefficient (defocus/(f/N)). 0-2 low defocusing
        :param focal: focal length [m]
        :param D: Telescope diameter [m]
        :return: Defocus MTF
        """
        #TODO
        x = pi * defocus * fr2D * (1 - fr2D)
        Hdefoc = (2 * j1(x)) / x
        return Hdefoc

    def mtfWfeAberrations(self, fr2D, lambd, kLF, wLF, kHF, wHF):
        """
        Wavefront Error Aberrations MTF
        :param fr2D: 2D relative frequencies (f/fc), where fc is the optics cut-off frequency
        :param lambd: central wavelength of the band [m]
        :param kLF: Empirical coefficient for the aberrations MTF for low-frequency wavefront errors [-]
        :param wLF: RMS of low-frequency wavefront errors [m]
        :param kHF: Empirical coefficient for the aberrations MTF for high-frequency wavefront errors [-]
        :param wHF: RMS of high-frequency wavefront errors [m]
        :return: WFE Aberrations MTF
        """
        #TODO
        Hwfe = np.exp(-fr2D * (1 - fr2D) * (kLF * ((wLF / lambd) ** 2) + kHF * ((wHF / lambd) ** 2)))
        return Hwfe

    def mtfDetector(self,fn2D):
        """
        Detector MTF
        :param fnD: 2D normalised frequencies (f/(1/w))), where w is the pixel width
        :return: detector MTF
        """
        #TODO
        Hdet = np.abs(np.sinc(fn2D))
        return Hdet

    def mtfSmearing(self, fnAlt, ncolumns, ksmear):
        """
        Smearing MTF
        :param ncolumns: Size of the image ACT
        :param fnAlt: 1D normalised frequencies 2D ALT (f/(1/w))
        :param ksmear: Amplitude of low-frequency component for the motion smear MTF in ALT [pixels]
        :return: Smearing MTF
        """
        #TODO
        fnAlt = np.repeat(fnAlt[:, None], ncolumns, axis=1)
        Hsmear = np.sinc(ksmear * fnAlt)
        return Hsmear

    def mtfMotion(self, fn2D, kmotion):
        """
        Motion blur MTF
        :param fnD: 2D normalised frequencies (f/(1/w))), where w is the pixel width
        :param kmotion: Amplitude of high-frequency component for the motion smear MTF in ALT and ACT
        :return: detector MTF
        """
        #TODO
        Hmotion = np.sinc(kmotion * fn2D)
        return Hmotion

    def plotMtf(self,Hdiff, Hdefoc, Hwfe, Hdet, Hsmear, Hmotion, Hsys, nlines, ncolumns, fnAct, fnAlt, directory, band):
        """
        Plotting the system MTF and all of its contributors
        :param Hdiff: Diffraction MTF
        :param Hdefoc: Defocusing MTF
        :param Hwfe: Wavefront electronics MTF
        :param Hdet: Detector MTF
        :param Hsmear: Smearing MTF
        :param Hmotion: Motion blur MTF
        :param Hsys: System MTF
        :param nlines: Number of lines in the TOA
        :param ncolumns: Number of columns in the TOA
        :param fnAct: normalised frequencies in the ACT direction (f/(1/w))
        :param fnAlt: normalised frequencies in the ALT direction (f/(1/w))
        :param directory: output directory
        :param band: band
        :return: N/A
        """

        """
                Plot the central ALT position of the MTFs and the Nyquist frequency
                """

        # Índice central (posición del píxel central)
        center_line = nlines // 2

        # Cortes a lo largo del eje ALT (vertical)
        mtf_diff = Hdiff[center_line, :]
        mtf_def = Hdefoc[center_line, :]
        mtf_wfe = Hwfe[center_line, :]
        mtf_det = Hdet[center_line, :]
        mtf_smear = Hsmear[center_line, :]
        mtf_motion = Hmotion[center_line, :]
        mtf_sys = Hsys[center_line, :]

        # Frecuencia de Nyquist
        nyquist = 0.5

        # Filtra las frecuencias positivas
        mask = fnAct >= 0
        fnAct_pos = fnAct[mask]

        mtf_diff = mtf_diff[mask]
        mtf_def = mtf_def[mask]
        mtf_wfe = mtf_wfe[mask]
        mtf_det = mtf_det[mask]
        mtf_smear = mtf_smear[mask]
        mtf_motion = mtf_motion[mask]
        mtf_sys = mtf_sys[mask]

        plt.figure(figsize=(7, 5))
        plt.plot(fnAct_pos, mtf_diff, color='navy', label='Optics Diffraction MTF')
        plt.plot(fnAct_pos, mtf_def, color='blue', label='Defocus MTF')
        plt.plot(fnAct_pos, mtf_wfe, color='orange', label='Wavefront Error Aberrations MTF')
        plt.plot(fnAct_pos, mtf_det, color='red', label='Detector MTF')
        plt.plot(fnAct_pos, mtf_smear, color='violet', label='Smearing MTF')
        plt.plot(fnAct_pos, mtf_motion, color='brown', label='Motion blur MTF')
        plt.plot(fnAct_pos, mtf_sys, color='green', label='System MTF')
        plt.axvline(0.5, color='k', linestyle='--', label='Nyquist Limit')

        plt.xlabel('Spatial frequencies f/(1/w) [-]')
        plt.ylabel('MTF Values')
        plt.title(f'Central ALT position of the MTFs and Nyquist in band ->VNIR-{band}.')
        plt.legend(fontsize=8)
        plt.grid(True)
        plt.tight_layout()

        # Guardar y mostrar
        path = os.path.join(directory, f"MTF_band{band}_ALT.png")
        plt.savefig(path, dpi=300)
        plt.show()
        #TODO


