from enum import Enum

class Address:
    IPv4_mask = 31
    
    def __init__(self, _str):
        self.readableIP = _str
        value2 = _str.split('/')
        _ip = value2[0].split('.')
        self.IP = (int(_ip[0])<<24) + (int(_ip[1])<<16) + (int(_ip[2])<<8) + (int(_ip[3]))
        self.mask = int(value2[1])
    
    def __str__(self):
        return f"{self.readableIP}"
    
    def GetBitValue(self, _mask: int):
        try:
            if ((1  << (self.IPv4_mask - _mask)) & self.IP) > 0:
                return 1
            else:
                return 0
        except:
            print(_mask)
            exit()