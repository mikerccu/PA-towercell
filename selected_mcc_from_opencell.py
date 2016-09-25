# Create a new CSV file from the opencellid database based on MCC
# It checks for duplicate and only take the first occurance.  It needs to be updaded to make a midpoint of multiple coordinates

import sys,os

def process_country(country):

    inputfile = open(os.path.dirname(__file__)+"\\opencell.csv", 'r')
    i = 0
    k = 0
    duplicate = 0
    tower = {}
    for line in inputfile:
        i += 1
        sys.stdout.write("\rProcessing entry %s. Found %s corresponding entries and %s duplicates.                    " % (i, k, duplicate))
        sys.stdout.flush()
        Type = line.split(",")
        mcc = Type[1]
        mnc = Type[2]
        lac = Type[3]
        cid = Type[4]
        lat = Type[6]
        lon = Type[7]
        if mcc == country:
            k += 1
            if (cid in tower.keys()) and (tower[cid][0] == mcc) and (tower[cid][1] == mnc) and (tower[cid][2] == lac):  # Check for duplicate entry. There seems to be a bug since it finds not enough duplicates
                duplicate += 1
                continue
            outputfile.write("%s;%s;%s;%s;%s;%s\r" % (mcc, mnc, lac, cid, lat, lon))
            tower[cid] = [mcc, mnc, lac, cid]

    inputfile.close()
    return


country = "206" # Belgium
outputfile = open(os.path.dirname(__file__)+"\\opencell"+str(country)+".csv", 'w')  # Get the path of the running script to find the celltowers.csv file
print("Processing Opencell full database and extract towers based on the MCC.")
process_country(country)
outputfile.close()
