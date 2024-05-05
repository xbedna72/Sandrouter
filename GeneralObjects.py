import ipaddress

class AddressIPv4:
    IPv4_mask = 32
    
    def __init__(self, _str):
        self.readableIP = _str
        value2 = _str.split('/')
        _ip = value2[0].split('.')
        self.IP = (int(_ip[0])<<24) + (int(_ip[1])<<16) + (int(_ip[2])<<8) + (int(_ip[3]))
        self.mask = int(value2[1])
    
    def __str__(self):
        return f"{self.readableIP}"
    
    def GetBitValue(self, _mask: int) -> int:
        try:
            if self.IPv4_mask - _mask >= 0:
                if ((1  << (self.IPv4_mask - _mask)) & self.IP) > 0:
                    return 1
                else:
                    return 0
            else:
                return 0
        except:
            print(_mask)
            exit()

class AddressIPv6:
    IPv6_mask = 128
    def __init__(self, _str):
        self.readableIP = _str
        value2 = _str.split('/')
        self.IP = value2[0]
        self.mask = int(value2[1])
    
    def __str__(self) -> str:
        return f"{self.readableIP}"

    def GetBitValue(self, _mask: int) -> int:
        value = int(ipaddress.ip_address(self.IP))

        try:
            if self.IPv6_mask - _mask >= 0:
                if ((1  << (self.IPv6_mask - _mask)) & value) > 0:
                    return 1
                else:
                    return 0
            else:
                return 0
        except:
            print(self)