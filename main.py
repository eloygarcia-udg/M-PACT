import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

from Arguments import get_args
from MPACT import MPACT
from Visualization import visualization


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

                data = MPACT(row['BreastVolumeCm3'], row['MammographyView'], F, T, args.S, msg)
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

        data = MPACT(args.BV, args.V, args.F, args.T, args.S, msg)

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