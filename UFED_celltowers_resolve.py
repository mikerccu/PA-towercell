#   Resolve Cell Towers coordinated based on their MCC/MNC/LAC/CID
#   CSV structure is : mcc;mnc;lac;cid;lon,lat

__author__ = 'Michael CARLIER'
__version__ = "0.1"
__email__ = "michael.carlier@fccu.be"

from physical import *
import os

def load_db(country):
    f = open(os.path.dirname(__file__) + "\\" + country + ".csv", 'r')    # Open the celltowers csv file based on the MCC

    for line in f:  # Read all lines in the csv file, split the contents and put it in a dictionnary
        type = line.split(";")
        mcc = type[0]
        mnc = type[1]
        lac = type[2]
        cid = type[3]
        lon = type[4]
        lat = type[5]
        tower[cid] = [mcc, mnc, lac, cid, lat, lon]
    f.close()
    return

tower = {}
loaded_country = []

for ct in ds.Models.GetEnumerator():
    if (ct.ModelType != Data.Models.LocationModels.CellTower):  # Check if the Cell Towers exist
        continue
    for entry in ct.GetEnumerator():    # Read trough all the line in Cell Towers and try to resolve them
        cid_found = entry.CID.Value
        if entry.MCC.Value not in loaded_country:  # Check if the MCC dictionnary is already loaded into memory
            loaded_country.append(entry.MCC.Value)
            print("MCC %s not yet loaded. Loading csv file." % entry.MCC.Value)
            load_db(entry.MCC.Value)
        if (cid_found in tower) and (entry.MCC.Value == tower[cid_found][0]) and (entry.MNC.Value == tower[cid_found][1]):    # If the MCC MNC and CID are the same then update the coordinate
            entry.Position.Value = Coordinate(float(tower[cid_found][4]), float(tower[cid_found][5]))
