import argparse
from os import startfile
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--URL", required=True, help="path to input image")
args = vars(ap.parse_args())
startfile(args["URL"])
