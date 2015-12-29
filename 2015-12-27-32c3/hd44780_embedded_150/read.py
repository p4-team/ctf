import matplotlib.pyplot as plt
from copy import *
datafiles = ['RSPI_GPIO_7.txt','RSPI_GPIO_8.txt','RSPI_GPIO_18.txt','RSPI_GPIO_23.txt','RSPI_GPIO_24.txt','RSPI_GPIO_25.txt']
labels = ['RS','CLK','BIT7','BIT6','BIT5','BIT4']
data=[]
class Point:
    def __init__(self,x,y,l):
        self.x=x
        self.y=y
        self.l=l
    def __repr__(self):
        return '('+str(self.x)+' ; '+str(self.y)+' ; '+str(self.l)+')'
class State:
    def __init__(self,rs,clk,bit4,bit5,bit6,bit7):
        self.rs=rs
        self.clk=clk
        self.bit4=bit4
        self.bit5=bit5
        self.bit6=bit6
        self.bit7=bit7
    def __repr__(self):
        return str(self.rs)+'\t'+str(self.clk)+'\t'+str(self.bit4)+'\t'+str(self.bit5)+'\t'+str(self.bit6)+'\t'+str(self.bit7)

    
    
    
for n,i in enumerate(datafiles):
    with open(i) as f:
        datax=map(float,f.readline().split())
        datay=map(float,f.readline().split())
        for ii in range(len(datax)):
            data.append(Point(datax[ii],datay[ii],labels[n]))
    
data.sort(key=lambda s: s.x)
states=[]
st = State(0,1,0,0,0,0)
for i in data:
    if i.l=='RS':
        st.rs=i.y
    elif i.l=='CLK':
        if i.y==0 and st.clk==1:
            st.clk=i.y
            #if st.rs==0:
            states.append(copy(st))
        else:
            st.clk=i.y
    elif i.l=='BIT4':
        st.bit4=i.y
    elif i.l=='BIT5':
        st.bit5=i.y
    elif i.l=='BIT6':
        st.bit6=i.y
    elif i.l=='BIT7':
        st.bit7=i.y
    else:
        states.append('\033[1;34m\]ERROR '+str(i.l)+'\033[0m\]')
        
#print '!!!JUST FOR WATCHING TO DECODE UGLY PRINT DATA!!!\n\n'        
#print 'no\trs\tclk\tbit4\tbit5\tbit6\tbit6'
#for i in range(1,len(states)):
#   print i,'\t',states[i]

###UGLY PRINTING### for decoding
for i in range(1,len(states)):
    print states[i]