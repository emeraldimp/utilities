from os import listdir
from os.path import isfile, join
from shutil import copyfile
import argparse

defaultSourcePath = "."
resourcesPath = "../../asc-mobile-app/src/Aspen.Mobile/Aspen.Mobile/Aspen.Mobile.Droid/Resources/"


parser = argparse.ArgumentParser(description='Automatically copy android image files to the correct resource folder based on the file name.')
parser.add_argument('--src', type=str, default=defaultSourcePath, help='the source path (default: .)')
parser.add_argument('--dest', type=str, default=resourcesPath, help='the destination path (default: ../../asc-mobile-app/src/Aspen.Mobile/Aspen.Mobile/Aspen.Mobile.Droid/Resources/)')
parser.add_argument('--run', action='store_true', help='perform the copy (default: prints the proposed list)')

args = parser.parse_args()
print args

def matchDensity(resourcesPath, density, file):
    prefixedDensity = '_' + density
    if prefixedDensity in file:
        return join(resourcesPath, 'drawable-' + density, file.replace(prefixedDensity, ''))
    elif density in file:
        return join(resourcesPath, 'drawable-' + density, file.replace(density, ''))
    return False

def getDestination(resourcesPath, file):
    destination = \
        matchDensity(resourcesPath, 'xxxhdpi', file) or \
        matchDensity(resourcesPath, 'xxhdpi', file) or \
        matchDensity(resourcesPath, 'xhdpi', file) or \
        matchDensity(resourcesPath, 'hdpi', file) or \
        matchDensity(resourcesPath, 'mdpi', file) or \
        matchDensity(resourcesPath, 'ldpi', file) or \
        'notmatched'
    return destination

def isExcluded(file):
    return 'notmatched' in file[1] or 'ldpi' in file[1]

def performCopy(files, dryRun):
    for file in files:
        if isExcluded(file):
            print "[EXCLUDED] " + file[0]
            continue

        print 'copy ' + file[0] + ' to ' + file[1]

        if not dryRun:
            copyfile(file[0], file[1])


files = [(join(args.src, f), getDestination(args.dest, f)) for f in listdir(args.src) if isfile(join(args.src, f)) and not f.endswith('.svg')]

performCopy(files, not args.run)
