import os
import numpy as np

global msg

def compute_thickness(BV, V, F, sigma, msg=[]):
    sd = 0 ## initializing
    T = 0 ## initializing

    if (type(F)==np.ndarray) or (F==None):
        if V == 'CC':
            sd = 0.089
            T = (0.60 * BV/(0.073 * BV+36.01) )+ 0.70
        elif V == 'MLO':
            sd = 0.10
            T = (0.66 * BV / (0.064 *  BV + 74.53)) + 1.58
    else:
        if (F < 50) or (F > 200):
            msg.append("Compression Force out of range. Expected forces in range [50, 200] N")
            print("")
            print(msg[-1])

        if V == 'CC':
            sd = 0.08
            T = 1.97 * np.sqrt(BV / F) + 1.15
        elif V == 'MLO':
            sd = 0.09
            T = 1.86 * np.sqrt(BV / F) + 1.42

    Tmin = T * (1 - sigma * sd)
    Tmax = T * (1 + sigma * sd)
    return T, Tmin, Tmax, sd


def MPACT(BV, view, Force=None, Thickness=None, sigma=2, msg=[]):
    if (BV <102.10) or (BV > 1933.59):
        msg.append("Breast volume out of range. Expected values between [102.10, 1933.59] cm³")
        print("")
        print(msg[-1])
        print("BE CAREFULL WITH YOUR RESULTS!")

    T, Tmin, Tmax, sd = compute_thickness(BV, view, Force, sigma, msg)

    print("")
    print(f"Expected Thickness: {np.round(T,3)} cm")
    print(f"Expected Thickness range: [{np.round(Tmin,2)}, {np.round(Tmax,2)}] cm")

    if Thickness == None:
        return T, Tmin, Tmax
    else:
        Sscore = (Thickness - T) / (T *sd)
        print("")
        print(f"S-score value: {np.round(Sscore,2)}")

        classification = 'Within the normal range'
        if Sscore<-2.0:
            #msg.append("Recorded thickness is smaller than the expected minimum")
            print(f"Recorded thickness is smaller than the expected minimum: {np.round(Thickness,2)} < {np.round(Tmin,2)}")
            classification = 'Potentially overcompressed'
        elif Sscore>2.0:
            #msg.append("Recorded thickness is larger than the expected maximum")
            print(f"Recorded thickness is larger than the expected maximum: {np.round(Thickness, 2)} > {np.round(Tmax, 2)}")
            classification = 'Potentially undercompressed'
        print(classification)

    print("")
    return T, Tmin, Tmax, classification, Sscore
