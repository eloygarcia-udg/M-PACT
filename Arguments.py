import argparse

terms = {'ID':'Patient ID or image name', 'BV':'Breast Volume (cm3)', 'V':'Mammography projection',
         'F':'Compression Force (N)', 'T':'Recorded Breast Thickness (cm)', 'S':'Sigma threshold for classification'}
def get_args():
    parser = argparse.ArgumentParser(description="MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)")
    parser.add_argument('--PatientID', '-ID', dest='ID', type=str, help='Patient ID or image name' )

    ## Required
    parser.add_argument('--BreastVolume', '-BV',
                        dest='BV', type=int, default= 1000,
                        help='Breast volume in cubic centimeters. Default: 1,000 cm3', required=True)
    parser.add_argument('--MammoView','-V', dest='V', type=str,
                        choices=('CC', 'MLO'), help='Mammography view. Only "CC" and "MLO" views are available', required=True)

    ## Optional
    parser.add_argument('--CompressionForce', '-F', dest='F', type=int,
                        help='Compression force, in Newtons (N), during the mammography acquisition')
    parser.add_argument('--Thickness', '-T', dest='T', type=float,
                        help='Breast thickness, in centimeters (cm), during the mammography acquisition')
    parser.add_argument('--Sigma', '-S', dest='S', type=float, default = 2,
                        help='Sigma Threshold (default:2)')
    args = parser.parse_args()

    # Print args
    print(parser.description)

    print("")
    print("Arguments:")
    for arg in vars(args):
        if not getattr(args, arg)==None:
            print(f"\t{terms[arg]}: {getattr(args, arg)}")

    return args
