"""
load data from zeo binary file and process

"""

## Copyright 2013, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from BinaryReader import BinaryReader
import sys, os, csv, numpy
from zeoRecord import ZeoRecord

def epochs_to_minutes(val):
    # Zeo time stats are counts of 30-second epochs
    return int(round(float(val) / 2.0))

def export_to_oscar_csv(chosen_records, filename="zeo_data_for_oscar.csv"):
    if not chosen_records:
        print("No valid records found.")
        return

    # Exact headers and structure from your example CSV
    headers = [
        'ZQ', 'Total Z', 'Time to Z', 'Time in Wake', 'Time in REM', 
        'Time in Light', 'Time in Deep', 'Awakenings', 'Sleep Graph', 
        'Detailed Sleep Graph', 'Start of Night', 'End of Night', 'Rise Time'
    ]

    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        for timestamp in sorted(chosen_records.keys()):
            rec = chosen_records[timestamp]
            
            # Detailed Sleep Graph is space-separated integers
            # Zeo stages: 0=Unknown, 1=Wake, 2=REM, 3=Light, 4=Deep
            count = int(rec.base_hypnogram_count)
            hyp_str = " ".join(map(str, rec.base_hypnogram[:count]))
            
            writer.writerow([
                rec.zq_score,
                epochs_to_minutes(rec.total_z),
                epochs_to_minutes(rec.time_to_z),
                epochs_to_minutes(rec.time_in_wake),
                epochs_to_minutes(rec.time_in_rem),
                epochs_to_minutes(rec.time_in_light),
                epochs_to_minutes(rec.time_in_deep),
                rec.awakenings,
                "", # Sleep Graph
                hyp_str,
                rec.start_of_night,
                rec.end_of_night,
                rec.end_of_night # Rise Time
            ])
    print(f"\nSUCCESS: Created '{filename}'")

# --- EXECUTION ---
if len(sys.argv) < 2:
    print('USAGE: python3 process_zeodata.py <ZEOLOG.DAT>')
    sys.exit(1)

datafile = sys.argv[1]
binaryReader = BinaryReader(datafile)
alldata = {}
start_timestamps = []

print("Scanning file...")
while binaryReader.BytesRemaining() >= 1680:
    found = False
    while not found and binaryReader.BytesRemaining() >= 6:
        # Python 3: Search for bytes
        if binaryReader.read('char') == b'S':
            if binaryReader.read('char') == b'L':
                if binaryReader.read('char') == b'E':
                    if binaryReader.read('char') == b'E':
                        if binaryReader.read('char') == b'P':
                            found = True

    if found:
        # Skip the trailing space after 'SLEEP'
        binaryReader.read('char')
        rec = ZeoRecord()
        try:
            rec.getRecordData(binaryReader)
            if rec.start_of_night_timestamp > 0:
                alldata[rec.start_of_night_timestamp] = rec
        except Exception:
            continue

binaryReader.close()
export_to_oscar_csv(alldata)
