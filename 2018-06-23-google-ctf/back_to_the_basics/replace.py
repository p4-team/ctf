import sys
import struct

tab = {
128: "END",
129: "FOR",
130: "NEXT",
131: "DATA",
132: "INPUT#",
133: "INPUT",
134: "DIM",
135: "READ",
136: "LET",
137: "GOTO",
138: "RUN",
139: "IF",
140: "RESTORE",
141: "GOSUB",
142: "RETURN",
143: "REM",
144: "STOP",
145: "ON",
146: "WAIT",
147: "LOAD",
148: "SAVE",
149: "VERIFY",
150: "DEF",
151: "POKE",
152: "PRINT#",
153: "PRINT",
154: "CONT",
155: "LIST",
156: "CLR",
157: "CMD",
158: "SYS",
159: "OPEN",
160: "CLOSE",
161: "GET",
162: "NEW",
163: "TAB(",
164: "TO",
165: "FN",
166: "SPC(",
167: "THEN",
168: "NOT",
169: "STEP",
170: "+",
171: "-",
172: "*",
173: "/",
174: "^",
175: "AND",
176: "OR",
177: ">",
178: "=",
179: "<",
180: "SGN",
181: "INT",
182: "ABS",
183: "USR",
184: "FRE",
185: "POS",
186: "SQR",
187: "RND",
188: "LOG",
189: "EXP",
190: "COS",
191: "SIN",
192: "TAN",
193: "ATN",
194: "PEEK",
195: "LEN",
196: "STR$",
197: "VAL",
198: "ASC",
199: "CHR$",
200: "LEFT$",
201: "RIGHT$",
202: "MID$",
203: "GO",
}

def mp(c):
    c = ord(c)
    if c in tab:
        return tab[c] + " "
    return chr(c)

s = open(sys.argv[1], "rb").read()
s2 = []
while len(s):
    s = s[2:] # ptr
    q = struct.unpack("<H", s[:2])[0]
    s = s[2:]
    tot = ""
    while s[0] != '\x00':
        tot += mp(s[0])
        s = s[1:]
    print q, tot
    s = s[1:]
