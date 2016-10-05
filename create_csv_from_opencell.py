# Create a new CSV file from the opencellid database based on MCC

import sys
import os
import math
import sqlite3

__author__ = 'Michael CARLIER'
__version__ = "0.1"
__email__ = "michael.carlier@fccu.be"

'''
    Towers structure :
      |
      |--[MCC #1]
      |      |-----[MNC #1]
      |      |      |
      |      |      |
      |      |      |------[LAC #1]
      |      |      |          |
      |      |      |          |---------[CID #1] = [Coord #1, Coord #2, ...]
      |      |      |          |
      |      |      |          |
      |      |      |          |---------[CID #2] = [Coord #1, Coord #2, ...].
      |      |      |          .
      |      |      |          .
      |      |      |
      |      |      |------[LAC #2]
      |      |      .
      |      |      .
      |      |
      |      |-----[MNC #2]
      |      .
      |      .
      |
      |--[MCC #2]
      .
      .
    '''
class TowersStruct:
    def __init__(self):
        self.towers = {}

    def add(self, mcc, mnc, cid, lac, coord):
        if mcc not in self.towers:
            self.towers[mcc] = {}

        if mnc not in self.towers[mcc]:
            self.towers[mcc][mnc] = {}

        if lac not in self.towers[mcc][mnc]:
            self.towers[mcc][mnc][lac] = {}

        if cid not in self.towers[mcc][mnc][lac]:
            self.towers[mcc][mnc][lac][cid] = []

        self.towers[mcc][mnc][lac][cid].append(coord)

    def get(self, mcc, mnc, lac, cid):
        if mcc in self.towers and mnc in self.towers[mcc] and lac in self.towers[mcc][mnc] and cid in self.towers[mcc][mnc][lac]:
            return self.towers[mcc][mnc][lac][cid]

        return None

    def list(self):
        listcountries = []

        for mcc in self.towers:
            listcountries.append(mcc)

        return listcountries

    '''
    Source: http://stackoverflow.com/questions/6671183/calculate-the-center-point-of-multiple-latitude-longitude-coordinate-pairs
    '''
    def computeMidPoint(self, coords):
        total = len(coords)
        if total == 1:
            return coords[0]

        x = y = z = 0

        for coord in coords:
            latitude = coord.lat * math.pi / 180
            longitude = coord.long * math.pi / 180

            x += math.cos(latitude) * math.cos(longitude)
            y += math.cos(latitude) * math.sin(longitude)
            z += math.sin(latitude)

        x = x / total
        y = y / total
        z = z / total

        centralLongitude = math.atan2(y, x)
        centralSquareRoot = math.sqrt(x * x + y * y)
        centralLatitude = math.atan2(z, centralSquareRoot)

        return Coord(centralLatitude * 180 / math.pi, centralLongitude * 180 / math.pi)

    def dumpAllWithMidpoint(self,country):
        dumpStruct = []

        for mcc in self.towers:
            if country == mcc:
                for mnc in self.towers[mcc]:
                    for lac in self.towers[mcc][mnc]:
                        for cid in self.towers[mcc][mnc][lac]:
                            midCoord = self.computeMidPoint(self.towers[mcc][mnc][lac][cid])
                            dumpStruct.append(Tower(mcc, mnc, lac, cid, midCoord))

        return dumpStruct

class Tower:
    def __init__(self, mcc, mnc, lac, cid, midCoord):
        self.mcc = mcc
        self.mnc = mnc
        self.lac = lac
        self.cid = cid
        self.midCoord = midCoord

    def __str__(self):
        return "MMC:%s | MNC:%s | CID:%s | LAC:%s | MidCoord:%s" % (self.mcc, self.mnc, self.lac, self.cid, self.midCoord)


class Coord:
    def __init__(self, lat, long):
        self.lat = float(lat)
        self.long = float(long)

    def __str__(self):
        return "%s,%s" % (self.lat, self.long)

def isExistinInTower(mcc, mnc, lac, cid):
    for line in tower.keys():
        if (line[0] == mcc) and (line[1] == mnc) and (line[2] == lac) and (line[3] == cid):
            return True
    return False

print("Opening Opencell database file (opencell.csv) to create the sqlite file.")
inputfile = open("opencell.csv", 'r')
next(inputfile) # Skip header of file
i = 0
stats = {}
con = sqlite3.Connection('celltowers.sqlite')
cur = con.cursor()
cur.execute('CREATE TABLE "towers" ("mcc" varchar(12), "mnc" varchar(12),"lac" varchar(12),"cid" varchar(12),"lon" varchar(12),"lat" varchar(12));')

for line in inputfile:
    i += 1

    #sys.stdout.write("\rProcessing entry %s to create stat file                   " % i)
    #sys.stdout.flush()

    type = line.split(",")
    mcc = type[1]
    mnc = type[2]
    lac = type[3]
    cid = type[4]
    lat = type[6]
    lon = type[7]

    #if i > 90000:
     #   break

    if mcc not in stats:
        stats[mcc] = 1
    else:
        stats[mcc] =  stats[mcc]+1  # update existing entry
    csv = [mcc, mnc, lac, cid, lat, lon]
    cur.execute('INSERT INTO towers VALUES (?, ?, ?, ?, ?, ?)', csv)
cur.close()
con.commit()
con.close()
inputfile.close()

outputfile = open("stats.txt", 'w')
print("Creating stat file (stats.txt).")
for entry in sorted(stats):
    outputfile.write("MCC : %s Country : %s Total : %s\r" % (entry, entry, stats[entry]))
outputfile.write("Total different MCC : %s\r" % len(stats.keys()))
outputfile.write("Total entries : %s\r" % i)
print("Total different MCC : %s" % len(stats.keys()))
print("Total entries : %s" % i)
outputfile.close()

current_entry = 0
db = sqlite3.connect('cellTowers.sqlite')
cursor = db.cursor()

for entry in sorted(stats):
    current_entry += 1
    inputfile = open("opencell.csv", 'r')
    next(inputfile)  # SKip header of file
    i = 0
    towersDb = TowersStruct()
    print("Parsing opencell db for MCC : %s." % entry)
    cursor.execute("select * from towers where mcc = '%s'" % entry)
    for row in cursor:
        mcc = row[0]
        mnc = row[1]
        lac = row[2]
        cid = row[3]
        lat = row[4]
        lon = row[5]
        towersDb.add(mcc, mnc, cid, lac, Coord(lat, lon))

    inputfile.close()

    print("Creating CSV files for MCC %s (%s). [%s/%s]" % (entry, entry, current_entry, len(stats.keys())))

    outputfile = open( entry + ".csv",'w')
    for tower in towersDb.dumpAllWithMidpoint(entry):
        outputfile.write("%s;%s;%s;%s;%s;%s\n" % (tower.mcc, tower.mnc, tower.lac, tower.cid, tower.midCoord.lat, tower.midCoord.long))
    outputfile.close()
print("Total differents countries : %s." % len(stats.keys()))
cursor.close
