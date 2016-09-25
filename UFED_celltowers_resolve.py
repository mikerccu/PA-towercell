#   Resolve Cell Towers coordinated based on their MCC/MNC/LAC/CID
#   celltowers.csv structure is : mcc;mnc;lac;cid;address;postal code;city;lat,lon
#   Opencellid structure is : radio,mcc,net,area,cell,unit,lon,lat,range,samples,changeable,created,updated,averageSignal
#
#   It removes duplicates and drops multiple coordinates to only keep the first one. So it does NOT midpoint multiples entries
#


__author__ = 'Michael CARLIER'

from physical import *
import os

def load_db():
    f = open(towerfilename, 'r')    # Open the celltowers.csv file in read mode
    for line in f:  # Read all lines in the celltowers.csv file, split the contents and put it in a dictionnary
        Type = line.split(";")
        mcc = Type[0]
        mnc = Type[1]
        lac = Type[2]
        cid = Type[3]
        lat = Type[4]
        lon = Type[5]
        tower[cid] = [mcc,mnc,lac,cid,lat,lon]
    f.close()
    return

towerfilename = os.path.dirname(__file__)+"\\celltowers.csv"  # Get the path of the running script to find the celltowers.csv file
tower = {}
load_db()

for ct in ds.Models.GetEnumerator():    # Check if the Cell Towers exist
    if (ct.ModelType != Data.Models.LocationModels.CellTower):
        continue
    for entry in ct.GetEnumerator():    # Read trough all the line in Cell Towers and try to resolve them
        cid = entry.CID.Value
        if (entry.CID.Value in tower) and (entry.MCC.Value == tower[cid][0]) and (entry.MNC.Value == tower[cid][1]):    # If the MCC MNC and CID are the same then update the coordinate
            entry.Position.Value = Coordinate(float(tower[cid][4]), float(tower[cid][5]))
