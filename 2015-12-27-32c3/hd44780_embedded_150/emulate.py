class Display:
    def __init__(self):
        self.data=[' ' for i in range(256)]
        self.ptr = 0
    def __repr__(self):
        return '#'*22+'\n'+'#'+''.join(self.data[:20])+'#'+'\n'+'#'+''.join(self.data[64:84])+'#'+'\n'+'#'+''.join(self.data[20:40])+'#'+'\n'+'#'+''.join(self.data[84:104])+'#'+'\n'+'#'*22
    def com(self,d):
        if d[0]=="1":
            self.ptr=(int(d[1:],2))
        elif d=="00000001":
            self.data=[' ' for i in range(256)]
            self.ptr = 0
        elif d[:7]=="0000001":
            self.ptr = 0
    
    def putchr(self,c):
        self.data[self.ptr]=chr(int(c,2))
        self.ptr+=1
        self.ptr=self.ptr

#input file        
with open('decode.out') as f:
    data =f.read().split('\n')
dsp=Display()
for i in data:
    a=i.split('\t')
    if a[0]=='DAT':
        dsp.putchr(a[1])
    elif a[0]=='COM':
        dsp.com(a[1])
    print dsp
