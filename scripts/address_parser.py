import sys
import re

pattern1 = "."
pattern2 = ":"

def ParseAddressIPv4(_ip):
    if pattern1 in _ip and pattern2 not in _ip:
        print(_ip, end='')
    return

def ParseAddressIPv6(_ip):
    if pattern2 in _ip:
        print(_ip, end='')
    return

def ParseUpdateMessageIPv4():
    for update in sys.stdin:
        _update = update.split('\n')
        _line = _update[0].split('|')
        if pattern1 in _line[5]:
            print(f"{_line[2]} {_line[5]}")

def ParseUpdateMessageIPv6():
    for update in sys.stdin:
        _update = update.split('\n')
        _line = _update[0].split('|')
        if pattern2 in _line[5]:
            print(f"{_line[2]} {_line[5]}")

if __name__ == "__main__":
    if sys.argv[1] == "-b":
        for prefix in sys.stdin:
            if len(prefix) > 0 and sys.argv[2] == "-v4":
                ParseAddressIPv4(prefix[8:])
            elif len(prefix) > 0 and sys.argv[2] == "-v6":
                ParseAddressIPv6(prefix[8:])
    if sys.argv[1] == "-u":
        if sys.argv[2] == "-v4":
            ParseUpdateMessageIPv4()
        elif sys.argv[2] == "-v6":
            ParseUpdateMessageIPv6()
