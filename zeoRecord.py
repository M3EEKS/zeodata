"""
defines a class to store a ZEO raw data record
- based heavily upon java code from http://zeodecoderview.sourceforge.net/

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

import datetime
import numpy

def timestamp_to_calendar(timestamp):
    # Converts Zeo timestamp to MM/DD/YYYY HH:MM for OSCAR.
    # If the time is still off, change 'hours=0' to your timezone offset
    # (e.g., hours=-5 for EST, hours=1 for CET).
    try:
        ts = float(timestamp)
        d = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
        d = d + datetime.timedelta(hours=0) # Shift is now set to zero
        return d.strftime('%m/%d/%Y %H:%M')
    except:
        return "00/00/0000 00:00"

class ZeoRecord:
    def __init__(self):
        self.timestamp = 0
        self.version = 0
        self.crc = 0
        self.start_of_night_timestamp = 0
        self.end_of_night_timestamp = 0
        self.start_of_night = ""
        self.end_of_night = ""
        self.zq_score = 0
        self.total_z = 0
        self.time_to_z = 0
        self.time_in_wake = 0
        self.time_in_rem = 0
        self.time_in_light = 0
        self.time_in_deep = 0
        self.awakenings = 0
        self.base_hypnogram = []
        self.base_hypnogram_count = 0

    def getRecordData(self, binaryReader):
        self.version = binaryReader.read('int16')
        self.timestamp = binaryReader.read('uint32')
        self.crc = binaryReader.read('uint32')
        binaryReader.read('uint32') # history
        binaryReader.read('uint32') # airplane_off
        binaryReader.read('uint32') # airplane_on

        for _ in range(8): binaryReader.read('uint32') # change_time/value
        for _ in range(20): binaryReader.read('char') # assert_name
        binaryReader.read('int32') # assert_line
        binaryReader.read('int32') # factory_reset
        binaryReader.read('int32') # headband_id
        for _ in range(144*3 + 36): binaryReader.read('uint8') # headband stats
        binaryReader.read('uint16') # id_hw
        binaryReader.read('uint16') # id_sw
        for _ in range(8): binaryReader.read('uint32') # more change events
        binaryReader.read('uint32') # sensor_life_reset
        binaryReader.read('uint32') # sleep_stat_reset
        for _ in range(2 + 9 + 1): binaryReader.read('uint32') # alarm/snooze events

        self.awakenings = binaryReader.read('uint16')
        binaryReader.read('uint16') # awakenings_avg
        
        self.end_of_night_timestamp = binaryReader.read('uint32')
        self.end_of_night = timestamp_to_calendar(self.end_of_night_timestamp)
        self.start_of_night_timestamp = binaryReader.read('uint32')
        self.start_of_night = timestamp_to_calendar(self.start_of_night_timestamp)
        
        self.time_in_deep = binaryReader.read('uint16')
        binaryReader.read('uint16') # deep_avg
        binaryReader.read('uint16') # deep_best
        self.time_in_light = binaryReader.read('uint16')
        binaryReader.read('uint16') # light_avg
        self.time_in_rem = binaryReader.read('uint16')
        binaryReader.read('uint16') # rem_avg
        binaryReader.read('uint16') # rem_best
        self.time_in_wake = binaryReader.read('uint16')
        binaryReader.read('uint16') # wake_avg
        self.time_to_z = binaryReader.read('uint16')
        binaryReader.read('uint16') # time_to_z_avg
        self.total_z = binaryReader.read('uint16')
        binaryReader.read('uint16') # total_z_avg
        binaryReader.read('uint16') # total_z_best
        self.zq_score = binaryReader.read('uint16')
        binaryReader.read('uint16') # zq_avg
        binaryReader.read('uint16') # zq_best

        binaryReader.read('uint16') # forced_index
        binaryReader.read('uint16') # forced_stage
        binaryReader.read('uint32') # hyp_start_time
        binaryReader.read('uint8') # rating
        for _ in range(3): binaryReader.read('uint8') # padding
        binaryReader.read('uint32') # padding
        
        self.base_hypnogram_count = binaryReader.read('uint32')

        for _ in range(0, 1920, 2):
            val = binaryReader.read('uint8')
            self.base_hypnogram.append(val & 0x0F)
            self.base_hypnogram.append(val >> 4)
