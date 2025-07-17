import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

from Arguments import get_args


def compute_thickness(args):
    sd = 0 ## initializing
    T = 0 ## initializing

    if args.F == None:
        if args.V == 'CC':
            sd = 0.089
            T = (0.60 * args.BV/(0.073*args.BV+36.01) )+ 0.70
        elif args.V == 'MLO':
            sd = 0.10
            T = (0.66 * args.BV / (0.064 * args.BV + 74.53)) + 1.58
    else:
        if (args.F < 50) or (args.F > 220):
            print("")
            print(f"Force out of range. Expected forces in range [50, 220] N")

        if args.V == 'CC':
            sd = 0.08
            T = 1.97 * np.sqrt(args.BV / args.F) + 1.15
        elif args.V == 'MLO':
            sd = 0.09
            T = 1.86 * np.sqrt(args.BV / args.F) + 1.42

    Tmin = T * (1 - args.S * sd)
    Tmax = T * (1 + args.S * sd)
    return T, Tmin, Tmax, sd


def MPACT():
    ## argument parser
    args = get_args()

    if (args.BV <102.10) or (args.BV > 1933.59):
        print("")
        print("Breast volume out of range. Expected values between [102.10, 1933.59] cm³")
        print("BE CAREFULL WITH YOUR RESULTS!")


    T, Tmin, Tmax, sd = compute_thickness(args)

    print("")
    print(f"Expected Thickness: {np.round(T,3)} cm")
    print(f"Expected Thickness range: [{np.round(Tmin,2)}, {np.round(Tmax,2)}] cm")


    if (not args.T==None) :
        Sscore = (args.T - T) / (T *sd)
        print(f"S-score value: {np.round(Sscore,2)}")

        classification = 'Within the normal range'
        if Sscore<-2.0:
            print(f"Recorded thickness is smaller than the expected minimum: {np.round(args.T,2)} < {np.round(Tmin,2)}")
            classification = 'Potentially overcompressed'
        elif Sscore>2.0:
            print(f"Recorded thickness is larger than the expected maximum: {np.round(args.T, 2)} > {np.round(Tmax, 2)}")
            classification = 'Potentially overcompressed'

        print(classification)

    print("")
    return 0

if __name__=='__main__':
    MPACT()