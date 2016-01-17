#delete newline first at end of input file#
with open('read2.out') as f:
    data = f.read()
    
data=data.split('\n')
trans = []
for i in range(0,len(data),2):
    tmp1=map(str,map(int,map(float,data[i].split('\t'))))
    tmp2=map(str,map(int,map(float,data[i+1].split('\t'))))
    t=''
    if tmp1[0] != tmp2[0]:
        print '\033[1;31m\]ERROR for',i,'data:',tmp1,tmp2,'\033[0m\]'
    else:
        if tmp1[0]=='0':
            t+='COM\t'
        else:
            t+='DAT\t'
        try:
            d=''
            t+=tmp1[5]+tmp1[4]+tmp1[3]+tmp1[2]
            t+=tmp2[5]+tmp2[4]+tmp2[3]+tmp2[2]
            d+=tmp1[5]+tmp1[4]+tmp1[3]+tmp1[2]
            d+=tmp2[5]+tmp2[4]+tmp2[3]+tmp2[2]
        except:
            print tmp1
            print tmp2
        if tmp1[0]=='1':
            t+='\t'+chr(int(d,2))
        elif tmp1[0] =='0':
            if d[0]=="1":
                t+='\t'+'jump to '+str(int(d[1:],2))
            elif d=="00000001":
                t+='\t'+'clear screen'
            elif d[:7]=="0000001":
                t+='\t'+'cursor to 0'
            elif d[:6]=="000001":
                t+='\t'+'entry mode set'
                if d[6]=='0':
                    t+=' decrement cursor'
                elif d[6]=='1':
                    t+=' increment cursor'
                if d[7]=='0':
                    t+=' no display shift'
                elif d[7]=='1':
                    t+=' display shift'
            elif d[:5]=="00001":
                t+='\t'+'display on/off control'
                if d[5]=='0':
                    t+=' display off'
                elif d[5]=='1':
                    t+=' display on'
                if d[6]=='0':
                    t+=' cursor off'
                elif d[6]=='1':
                    t+=' cursor on'
                if d[7]=='0':
                    t+=' no blink'
                elif d[7]=='1':
                    t+=' blink'
            elif d[:4]=="0001":
                t+='\t'+'Cursor/display shift'
                if d[4]=='0':
                    t+=' move cursor'
                elif d[4]=='1':
                    t+=' shift display'
                if d[5]=='0':
                    t+=' shift left'
                elif d[5]=='1':
                    t+=' shift right'
            elif d[:3]=="001":
                t+='\t'+'Function set'
                if d[3]=='0':
                    t+=' 4bit interface'
                elif d[3]=='1':
                    t+=' 8bit interface'
                if d[4]=='0':
                    t+=' 1/8 or 1/11 duty (1 line)'
                elif d[4]=='1':
                    t+=' 1/16 duty (2 lines)'
                if d[5]=='0':
                    t+='  5x8 dots'
                elif d[5]=='1':
                    t+='  5x10 dots'
        trans.append(t)
        
for i in trans:
    print i