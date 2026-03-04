import struct

class BinaryReader:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.file.seek(0, 2)
        self.file_size = self.file.tell()
        self.file.seek(0)

    def read(self, type_str):
        if type_str == 'int16':
            return struct.unpack('<h', self.file.read(2))[0]
        elif type_str == 'uint16':
            return struct.unpack('<H', self.file.read(2))[0]
        elif type_str == 'uint32':
            return struct.unpack('<I', self.file.read(4))[0]
        elif type_str == 'int32':
            return struct.unpack('<i', self.file.read(4))[0]
        elif type_str == 'uint8':
            return struct.unpack('B', self.file.read(1))[0]
        elif type_str == 'char':
            return self.file.read(1)
        return None

    def BytesRemaining(self):
        return self.file_size - self.file.tell()

    def close(self):
        self.file.close()
