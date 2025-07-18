import sys
import argparse


terms = {'ID':'Patient ID or image name','use_csv':'Use csv file', 'BV':'Breast Volume (cm3)', 'V':'Mammography projection',
         'F':'Compression Force (N)', 'T':'Recorded Breast Thickness (cm)', 'S':'Sigma threshold',
         'vis':'Visualization','output':'Output file'}

def csv_parser(parser):
    #parser = argparse.ArgumentParser(description="MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)")
    parser.add_argument('--use_csv', dest='use_csv', type=str, help='File path', required=True)
    parser.add_argument('--outputfile', '-o', dest='output', type=str, help='File path', required=True)

    parser.add_argument('--Sigma', '-S', dest='S', type=float, default=2,
                        help='Sigma Threshold (default:2)')
    parser.add_argument('--visualization', dest='vis', action='store_true', default=False)

    args = parser.parse_args()
    return args

def terminal_parser(parser):
    #parser = argparse.ArgumentParser(description="MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)")
    parser.add_argument('--PatientID', '-ID', dest='ID', type=str, help='Patient ID or image name')
    parser.add_argument('--outputfile', '-o', dest='output', default = None, type=str, help='File path')

    ## Required
    parser.add_argument('--BreastVolume', '-BV', dest='BV', type=int,
                        help='Breast volume in cubic centimeters', required=True)
    parser.add_argument('--MammographyView', '-V', dest='V', type=str,
                        choices=('CC', 'MLO'), help='Mammography view. Only "CC" and "MLO" views are available', required=True)

    ## Optional
    parser.add_argument('--CompressionForce', '-F', dest='F', type=int,
                        help='Compression force, in Newtons (N), during the mammography acquisition')
    parser.add_argument('--Thickness', '-T', dest='T', type=float,
                        help='Breast thickness, in centimeters (cm), during the mammography acquisition')
    parser.add_argument('--Sigma', '-S', dest='S', type=float, default=2,
                        help='Sigma Threshold (default:2)')
    parser.add_argument('--visualization', dest='vis', action='store_true', default=False)

    args = parser.parse_args()
    return args

def get_args():
    ## Deciding parser to use csv file or isolate examples
    deciding_args_parser = argparse.ArgumentParser(description="MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)")
    deciding_args_parser.add_argument('--use_csv', dest='use_csv', required=False, action='store_true')
    deciding_args, _ = deciding_args_parser.parse_known_args()

    ## Real parser
    parser = argparse.ArgumentParser(description="MPACT: Mammography Pressure and Compression tracking for Quality Control (v.0.1)")
    if deciding_args.use_csv:
        args = csv_parser(parser)
    else:
        args = terminal_parser(parser)

    # Print args
    print(parser.description)
    print("")

    print("Arguments:")
    for arg in vars(args):
        if not getattr(args, arg)==None:
            print(f"\t{terms[arg]}: {getattr(args, arg)}")

    print("")
    return args

