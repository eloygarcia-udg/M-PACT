import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

from Arguments import get_args

global msg


def visualization(df):
    views = np.unique(df['MammographyView'])

    fig, ax = plt.subplots(ncols=len(views))
    for i in range(len(views)):
        vi=views[i]

        temp_df = df[df['MammographyView']==vi]

        colours = np.array(['green']*len(temp_df.index))
        colours[temp_df['S-score'] < -2.0] = 'red'
        colours[temp_df['S-score'] > 2.0] = 'blue'

        if not 'CompressionForceN' in temp_df.columns:
            bv = np.arange(102., 2000, 10)
            t2_vis, t2min_vis, t2max_vis, sdim = compute_thickness(bv, vi, None, 2)
            t3_vis, t3min_vis, t3max_vis, sdim = compute_thickness(bv, vi, None, 3)

            ax[i].plot(bv, t2_vis)
            ax[i].fill_between(bv, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
            ax[i].fill_between(bv, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')

            ax[i].scatter(temp_df['BreastVolumeCm3'], temp_df['RecordedThicknessCm'], color=colours)
            for idx, row in temp_df.iterrows():
                ax[i].text(25+row['BreastVolumeCm3'], 0.15+row['RecordedThicknessCm'], row['PatientID'],
                           horizontalalignment='center', verticalalignment='bottom')
            ax[i].title.set_text(f"Mammography view {vi}")
            ax[i].set_ylabel("Thickness (cm)")
            ax[i].set_xlabel("Breast Volume (cm³)")
        else:
            bv = np.arange(102., 2000, 10)
            cf = np.arange(0.5, 12.0, 11.5/len(bv))

            t2_vis, t2min_vis, t2max_vis, sdim = compute_thickness(bv, vi, bv/cf, 2)
            t3_vis, t3min_vis, t3max_vis, sdim = compute_thickness(bv, vi, bv/cf, 3)

            ax[i].plot(cf, t2_vis)
            ax[i].fill_between(cf, t3min_vis, t3max_vis, alpha=0.4, facecolor='red')
            ax[i].fill_between(cf, t2min_vis, t2max_vis, alpha=0.4, facecolor='green')

            ax[i].scatter(temp_df['BreastVolumeCm3'] / temp_df['CompressionForceN'], temp_df['RecordedThicknessCm'], color=colours)
            for idx, row in temp_df.iterrows():
                ax[i].text(row['BreastVolumeCm3'] / row['CompressionForceN'], 0.15+row['RecordedThicknessCm'], row['PatientID'],
                           horizontalalignment='center', verticalalignment='bottom')
            ax[i].title.set_text(f"Mammography view {vi}")
            ax[i].set_ylabel("Thickness (cm)")
            ax[i].set_xlabel("Breast Volume / Compression Force (cm³ / N)")
    plt.show()


def compute_thickness(BV, V, F, sigma):
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


def MPACT(BV, view, Force=None, Thickness=None, sigma=2):
    if (BV <102.10) or (BV > 1933.59):
        msg.append("Breast volume out of range. Expected values between [102.10, 1933.59] cm³")
        print("")
        print(msg[-1])
        print("BE CAREFULL WITH YOUR RESULTS!")

    T, Tmin, Tmax, sd = compute_thickness(BV, view, Force, sigma)

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


def main():
    ## argument parser
    args = get_args()

    ## To compile results
    PatientID_results = []
    BreastVolume_results = []
    MammographyView_results = []
    CompressionForce_results = []
    RecordedThickness_results = []
    ###
    Thickness_results = []
    ThicknessMin_results = []
    ThicknessMax_results = []
    ##
    Sscore_results = []
    Classification_results = []
    Errors_results = []


    """
    Running the M-PACT core
    """
    if ("use_csv" in args) and os.path.exists(args.use_csv):
        """
        Checking input and output filenames
        """
        if args.use_csv==args.output:
            print("Origin and output csv files are the same. ")
            print("Please, DO NOT REWRITE the initial document")
            print("")
            return 0

        """
            Running the M-PACT core using a csv file
        """
        infodoc = pd.read_csv(args.use_csv)
        if {'PatientID','BreastVolumeCm3','MammographyView'}.issubset(infodoc.columns):
            for index, row in infodoc.iterrows():
                global msg
                msg = []

                print(row)
                PatientID_results.append(row['PatientID'])
                BreastVolume_results.append(row['BreastVolumeCm3'])
                MammographyView_results.append(row['MammographyView'])

                F = None
                T = None

                if ('CompressionForceN' in infodoc.columns):
                    F = row['CompressionForceN']
                    CompressionForce_results.append(F)
                if ('ThicknessCm' in infodoc.columns):
                    T = row['ThicknessCm']
                    RecordedThickness_results.append(T)

                data = MPACT(row['BreastVolumeCm3'], row['MammographyView'], F, T, args.S)
                # data = [ T, Tmin, Tmax, classification, Sscore]

                Thickness_results.append(data[0])
                ThicknessMin_results.append(data[1])
                ThicknessMax_results.append(data[2])
                Errors_results.append(msg)

                if ('ThicknessCm' in infodoc.columns):
                    Classification_results.append(data[3])
                    Sscore_results.append(data[4])

        else:
            print("M-PACT csv requires of, at least, columns 'PatientID','BreastVolumeCm3', and 'MammographyView' ")
            return 0
    else:
        """
            Running the M-PACT core in terminal for isolated cases
        """
        msg = []
        ##
        PatientID_results.append(args.ID)
        BreastVolume_results.append(args.BV)
        MammographyView_results.append(args.V)

        if not args.F==None:
            CompressionForce_results.append(args.F)
        if not args.T==None:
            RecordedThickness_results.append(args.T)

        data = MPACT(args.BV, args.V, args.F, args.T, args.S)

        ## Results
        Thickness_results.append(data[0])
        ThicknessMin_results.append(data[1])
        ThicknessMax_results.append(data[2])
        Errors_results.append(msg)

        if not args.T==None:
            Classification_results.append(data[3])
            Sscore_results.append(data[4])

    """
        Saving results into a .csv file 
    """
    ## Preparing dictionary
    temp_dict = {'PatientID':PatientID_results,
                 'MammographyView':MammographyView_results,
                 'BreastVolumeCm3':BreastVolume_results}
    if len(CompressionForce_results)>0:
        temp_dict['CompressionForceN'] = CompressionForce_results
    if len(RecordedThickness_results)>0:
        temp_dict['RecordedThicknessCm'] = RecordedThickness_results

    temp_dict['ExpectedThicknessCm'] = Thickness_results
    temp_dict['MinThicknessIntervalCm'] = ThicknessMin_results
    temp_dict['MaxThicknessIntervalCm'] = ThicknessMax_results
    if len(RecordedThickness_results)>0:
        temp_dict['S-score'] = Sscore_results
        temp_dict['Classification'] = Classification_results

    temp_dict['Messages']=Errors_results

    #Preparing dataframe
    resultsDF = pd.DataFrame(temp_dict)

    ## Recording dataframe
    if args.output is not None:
        if args.output.endswith('.csv'):
            resultsDF.to_csv(args.output, index=False)
            print(f"Results saved into {args.output }")
        else:
            resultsDF.to_csv(args.output+'.csv', index=False)
            print(f"Results saved into {args.output+'.csv'}")

    """
        VISUALIZATION
    """
    if len(RecordedThickness_results) > 0 and args.vis:
        visualization(resultsDF)


if __name__=='__main__':
    main()