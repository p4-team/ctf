#!/usr/bin/python

from binascii import hexlify
import sys
from pcapfile import savefile

hidMap = {0:"Reserved (no event indicated)", 1:"Keyboard ErrorRollOver", 2:"Keyboard POSTFail", 3:"Keyboard ErrorUndefined", 4:"Keyboard a and A", 5:"Keyboard b and B", 6:"Keyboard c and C", 7:"Keyboard d and D", 8:"Keyboard e and E", 9:"Keyboard f and F", 10:"Keyboard g and G", 11:"Keyboard h and H", 12:"Keyboard i and I", 13:"Keyboard j and J", 14:"Keyboard k and K", 15:"Keyboard l and L", 16:"Keyboard m and M", 17:"Keyboard n and N", 18:"Keyboard o and O", 19:"Keyboard p and P", 20:"Keyboard q and Q", 21:"Keyboard r and R", 22:"Keyboard s and S", 23:"Keyboard t and T", 24:"Keyboard u and U", 25:"Keyboard v and V", 26:"Keyboard w and W", 27:"Keyboard x and X", 28:"Keyboard y and Y", 29:"Keyboard z and Z", 30:"Keyboard 1 and !", 31:"Keyboard 2 and @", 32:"Keyboard 3 and #", 33:"Keyboard 4 and $", 34:"Keyboard 5 and %", 35:"Keyboard 6 and ^", 36:"Keyboard 7 and &", 37:"Keyboard 8 and *", 38:"Keyboard 9 and (", 39:"Keyboard 0 and )", 40:"Keyboard Return (ENTER)", 41:"Keyboard ESCAPE", 42:"Keyboard DELETE (Backspace)", 43:"Keyboard Tab", 44:"Keyboard Spacebar", 45:"Keyboard - and _", 46:"Keyboard = and +", 47:"Keyboard [ and {", 48:"Keyboard ] and }", 49:"Keyboard \ and |", 50:"Keyboard Non-US # and ~", 51:"Keyboard ; and :", 52:"Keyboard quote and doubleQoute", 53:"Keyboard Grave Accent and Tilde", 54:"Keyboard, and <", 55:"Keyboard . and >", 56:"Keyboard / and ?", 57:"Keyboard Caps Lock11", 58:"Keyboard F1", 59:"Keyboard F2", 60:"Keyboard F3", 61:"Keyboard F4", 62:"Keyboard F5", 63:"Keyboard F6", 64:"Keyboard F7", 65:"Keyboard F8", 66:"Keyboard F9", 67:"Keyboard F10", 68:"Keyboard F11", 69:"Keyboard F12", 70:"Keyboard PrintScreen", 71:"Keyboard Scroll Lock", 72:"Keyboard Pause1", 73:"Keyboard Insert", 74:"Keyboard Home", 75:"Keyboard PageUp", 76:"Keyboard Delete Forward", 77:"Keyboard End", 78:"Keyboard PageDown", 79:"Keyboard RightArrow", 80:"Keyboard LeftArrow", 81:"Keyboard DownArrow", 82:"Keyboard UpArrow", 83:"Keypad Num Lock and Clear", 84:"Keypad /", 85:"Keypad *", 86:"Keypad -", 87:"Keypad +", 88:"Keypad ENTER5", 89:"Keypad 1 and End", 90:"Keypad 2 and Down Arrow", 91:"Keypad 3 and PageDn", 92:"Keypad 4 and Left Arrow", 93:"Keypad 5", 94:"Keypad 6 and Right Arrow", 95:"Keypad 7 and Home", 96:"Keypad 8 and Up Arrow", 98:"Keypad 0 and Insert", 99:"Keypad . and Delete", 100:"Keyboard Non-US \ and |", 101:"Keyboard Application10", 102:"Keyboard Power", 103:"Keypad =", 104:"Keyboard F13", 105:"Keyboard F14", 106:"Keyboard F15", 107:"Keyboard F16", 108:"Keyboard F17", 109:"Keyboard F18", 110:"Keyboard F19", 111:"Keyboard F20", 112:"Keyboard F21", 113:"Keyboard F22", 114:"Keyboard F23", 115:"Keyboard F24", 116:"Keyboard Execute", 117:"Keyboard Help", 118:"Keyboard Menu", 119:"Keyboard Select", 120:"Keyboard Stop", 121:"Keyboard Again", 122:"Keyboard Undo", 123:"Keyboard Cut", 124:"Keyboard Copy", 125:"Keyboard Paste", 126:"Keyboard Find", 127:"Keyboard Mute", 128:"Keyboard Volume Up", 129:"Keyboard Volume Down", 130:"Keyboard Locking Caps Lock12", 131:"Keyboard Locking Num Lock12", 132:"Keyboard Locking Scroll Lock12", 133:"Keypad Comma", 134:"Keypad Equal Sign", 135:"Keyboard International115", 136:"Keyboard International216", 137:"Keyboard International317", 138:"Keyboard International418", 139:"Keyboard International519", 140:"Keyboard International620", 141:"Keyboard International721", 142:"Keyboard International822", 143:"Keyboard International922", 144:"Keyboard LANG125", 145:"Keyboard LANG226", 146:"Keyboard LANG330", 147:"Keyboard LANG431", 148:"Keyboard LANG532", 149:"Keyboard LANG68", 150:"Keyboard LANG78", 151:"Keyboard LANG88", 152:"Keyboard LANG98", 153:"Keyboard Alternate Erase", 154:"Keyboard SysReq/Attention", 155:"Keyboard Cancel", 156:"Keyboard Clear", 157:"Keyboard Prior", 158:"Keyboard Return", 159:"Keyboard Separator", 160:"Keyboard Out", 161:"Keyboard Oper", 162:"Keyboard Clear/Again", 163:"Keyboard CrSel/Props", 164:"Keyboard ExSel", 165:"AF Reserved", 166:"AF Reserved", 167:"AF Reserved", 169:"AF Reserved", 170:"AF Reserved", 171:"AF Reserved", 172:"AF Reserved", 173:"AF Reserved", 174:"AF Reserved", 175:"AF Reserved", 176:"Keypad 00", 177:"Keypad 000", 178:"Thousands Separator", 179:"Decimal Separator", 180:"Currency Unit", 181:"Currency Sub-unit", 182:"Keypad (", 184:"Keypad {", 185:"Keypad }", 186:"Keypad Tab", 187:"Keypad Backspace", 188:"Keypad A", 189:"Keypad B", 190:"Keypad C", 191:"Keypad D", 192:"Keypad E", 193:"Keypad F", 194:"Keypad XOR", 195:"Keypad ^", 196:"Keypad %", 197:"Keypad <", 198:"Keypad >", 199:"Keypad &", 200:"Keypad &&", 201:"Keypad |", 202:"Keypad ||", 203:"Keypad :", 204:"Keypad #", 205:"Keypad Space", 206:"Keypad @", 207:"Keypad !", 208:"Keypad Memory Store", 209:"Keypad Memory Recall", 210:"Keypad Memory Clear", 211:"Keypad Memory Add", 212:"Keypad Memory Subtract", 213:"Keypad Memory Multiply", 214:"Keypad Memory Divide", 215:"Keypad +/-", 216:"Keypad Clear", 217:"Keypad Clear Entry", 218:"Keypad Binary", 219:"Keypad Octal", 220:"Keypad Decimal", 221:"Keypad Hexadecimal", 222:"DF Reserved", 223:"DF Reserved", 224:"Keyboard LeftControl", 225:"Keyboard LeftShift", 226:"Keyboard LeftAlt", 227:"Keyboard Left GUI10", 228:"Keyboard RightControl", 229:"Keyboard RightShift", 230:"Keyboard RightAlt", 231:"Keyboard Right GUI"}


def main():
    s=""
    lastt=0
    if(len(sys.argv) != 2):
        print("Usage: python parsePcap.py <pcap.file>")
        return


    fileIn = open(sys.argv[1])
    capFile = savefile.load_savefile(fileIn, verbose=True)

    for packet in capFile.packets:
        if(len(hexlify(packet.raw())) == 0x41*2):
            leftoverPacketData = hexlify(packet.raw())[-2:]

            t=packet.timestamp*1000+packet.timestamp_ms
            diff=t-lastt
            lastt=t
            if diff>100000:
                continue
            if leftoverPacketData!="03":
                if diff>300:
                    s+="_"
                else:
                    s+="."
            else:
                if diff<300:
                    s+=""
                else:
                    s+=" "
    print s

if __name__ == "__main__":
    main()
