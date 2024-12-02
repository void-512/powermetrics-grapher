import os
import sys
import argparse

log = None
save = None

parser = argparse.ArgumentParser()
parser.add_argument("-l", type=str, required=True, help="Log file path")
parser.add_argument("-s", action="store_true", help="Save figure")
args = parser.parse_args()

if args.s:
    save = True
else:
    save = False
if not os.path.isfile(args.l):
    sys.exit("File doesn't exist")
else:
    log = args.l