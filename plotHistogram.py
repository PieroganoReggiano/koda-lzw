import dataFunc
import argparse

parser = argparse.ArgumentParser(description="Ploting")
parser.add_argument('-f', '--filename', help='Filename ', required=True)
args = parser.parse_args()

dataFunc.plot_histogram(args.filename, args.output)
