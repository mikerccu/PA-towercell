# PA-towercell
Python script to resolve Cell Towers into coordinates in Cellebrite UFED Physical Analyzer

The purpose of this script is to resolve the informations contained in the "Cell Towers" of your Cellebrite UFED Physical Analyzer.
It will use a CSV created file containing information from Mobile provider or using the Opencell database (http://opencellid.org/).

Your CSV file should be formatted as follow :
mcc;mnc;lac;cid;address;postal code;city;lat,lon

Example :
206;01;2001;26286;50.897875;4.358859

The opencellid database is formatted as follow :
radio,mcc,net,area,cell,unit,lon,lat,range,samples,changeable,created,updated,averageSignal

So it needs to be converted. You can use the “create_csv_from_opencell.py” script to extract all entries based on the MCC (country code) from the opencellid db and it will create a csv file for each MCC.

The UFED PA script to resolve the tower cells into coordinates is “UFED_celltowers_resolve.py”.

