import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

from Arguments import get_args

def visualization(BV, col):
    bv = np.arange(102., 2000, 10)
    t2_vis, t2min_vis, t2max_vis, sdim = compute_thickness(bv, args.V, args.F, 2)
    t3_vis, t3min_vis, t3max_vis, sdim = compute_thickness(bv, args.V, args.F, 3)
    # print(tic)
    fig, ax = plt.subplots()
    if args.F == None:
        ax.plot(bv, t2_vis)
        ax.fill_between(bv, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
        ax.fill_between(bv, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')
        ax.scatter(BV, args.T, color=col)
        ax.title.set_text(f"Patient {args.ID}, mammography view {args.V}")
        ax.set_ylabel("Thickness (cm)")
        ax.set_xlabel("Breast Volume (cm³)")
    else:
        ax.plot(bv / args.F, t2_vis)
        ax.fill_between(bv / args.F, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
        ax.fill_between(bv / args.F, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')

        ax.scatter(BV / args.F, args.T, color=col)
        ax.title.set_text(f"Patient {args.ID}, mammography view {args.V}, compression force {args.F} N")
        ax.set_ylabel("Thickness (cm)")
        ax.set_xlabel("Breast Volume / Compression Force (cm³ / N)")
    plt.show()



def compute_thickness(BV, V, F, sigma):
    sd = 0 ## initializing
    T = 0 ## initializing

    if F == None:
        if V == 'CC':
            sd = 0.089
            T = (0.60 * BV/(0.073 * BV+36.01) )+ 0.70
        elif V == 'MLO':
            sd = 0.10
            T = (0.66 * BV / (0.064 *  BV + 74.53)) + 1.58
    else:
        if (F < 50) or (F > 220):
            print("")
            print(f"Force out of range. Expected forces in range [50, 220] N")

        if V == 'CC':
            sd = 0.08
            T = 1.97 * np.sqrt(BV / F) + 1.15
        elif V == 'MLO':
            sd = 0.09
            T = 1.86 * np.sqrt(BV / F) + 1.42

    Tmin = T * (1 - sigma * sd)
    Tmax = T * (1 + sigma * sd)
    return T, Tmin, Tmax, sd


def MPACT(BV, view, Force=None, sigma=2, Thickness=None):
    if (BV <102.10) or (BV > 1933.59):
        print("")
        print("Breast volume out of range. Expected values between [102.10, 1933.59] cm³")
        print("BE CAREFULL WITH YOUR RESULTS!")


    T, Tmin, Tmax, sd = compute_thickness(BV, view, Force, sigma)

    print("")
    print(f"Expected Thickness: {np.round(T,3)} cm")
    print(f"Expected Thickness range: [{np.round(Tmin,2)}, {np.round(Tmax,2)}] cm")


    if (not Thickness==None) :
        Sscore = (Thickness - T) / (T *sd)
        print(f"S-score value: {np.round(Sscore,2)}")

        classification = 'Within the normal range'
        col = 'green'
        if Sscore<-2.0:
            print(f"Recorded thickness is smaller than the expected minimum: {np.round(Thickness,2)} < {np.round(Tmin,2)}")
            classification = 'Potentially overcompressed'
            col = 'red'
        elif Sscore>2.0:
            print(f"Recorded thickness is larger than the expected maximum: {np.round(args.T, 2)} > {np.round(Tmax, 2)}")
            classification = 'Potentially overcompressed'
            col ='blue'

        print(classification)

    print("")
    return 0

if __name__=='__main__':
    ## argument parser
    args = get_args()

    if ("use_csv" in args) and os.path.exists(args.use_csv):
        infodoc = pd.read_csv(args.use_csv)
        for index, row in infodoc.iterrows():
            print(row['PatientID'])
            MPACT(row['BreastVolumeCm3'], row['View'], row['CompressionForceN'])
    """
    if (not Thickness==None) and args.vis:
        visualization(args, col)
    """
    #MPACT()