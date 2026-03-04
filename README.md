zeodata
=======

fork of Russell Poldrack's code to parse zeo data file
updated for python3 compatability

USAGE: process_zeodata.py ZEOSLEEP.DAT  
  ZEOSLEEP.DAT must be in the same directory as process_zeodata.py, zeoRecord.py, and BinaryReader.py
  "python3 process_zeodata.py ZEOSLEEP.DAT" will output the data to a file called zeo_data_for_oscar.csv
  import zeo_data_for_oscar.csv to OSCAR

requires:
- pytz
- numpy
- matplotlib


