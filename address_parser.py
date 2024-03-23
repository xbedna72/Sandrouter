import sys
import re

def ParseAddress(_ip, pattern):
    if pattern in _ip:
        print(_ip)
    return

def ParseUpdateMessage(pattern):
    for update in sys.stdin:
        _update = update.split('\n')
        _line = _update[0].split('|')    
        if pattern in _line[5]:
            print(f"{_line[2]} {_line[5]}")
        
if __name__ == "__main__":
    pattern = "."
    if sys.argv[1] == "-p":
        for prefix in sys.stdin:
            if len(prefix) > 0:
                ParseAddress(prefix[8:], pattern)
    if sys.argv[1] == "-u":
        ParseUpdateMessage(pattern)
