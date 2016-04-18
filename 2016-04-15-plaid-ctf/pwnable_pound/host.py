#!/usr/bin/python
import os
import hashlib
import subprocess
import time



def menu():
    print """
    1. Read Trump article
    2. Run Trump Money Simulator
    3. Quit
    """
    try:
        res = int(raw_input())
        if res <= 0 or res > 3:
            return -1
        else:
            return res
    except:
        return -1

def read_tweet():
    print "Read the top 20 tweets by Trump!"
    print "Enter a number (1 - 20)"
    tweet_number = raw_input()
    time.sleep(5)

    try:
        with open("tweets/{0}".format(tweet_number), 'r') as f:
            print f.read()
    except:
        print "Invalid input!"

def run_sim():
    print "Trump's money simulator (that makes america great again) simulates two different sized states transfering money around, with the awesome Trump algorithm."
    print "The simulator takes in 2 inputs. Due to the awesomeness of the simulator, we can only limit the input to less than a thousand each..."

    input1 = raw_input("[Smaller] State 1 Size:")
    input2 = raw_input("[Larger] State 2 Size:")
    if len(input1) > 3 or len(input2) >3:
        print "Number has to be less than 1000"
        return

    str_to_hash = "[]{0}[]{1}##END".format(input1,input2)
    print "Hashing",repr(str_to_hash)
    sim_id = hashlib.sha256(str_to_hash).hexdigest()
    sim_name = "sims/sim-{0}".format(sim_id)

    if False:#os.path.isfile(sim_name):
        print "Sim compiled, running sim..."
    else:
        print "Compiling Sim"
        args=["clang", "-m32", "-DL1={}".format(input1),
                        "-DL2={}".format(input2), "pound.c", "-o",
                        sim_name]
        print args
        ret = subprocess.call(args)
        if ret != 0:
            print "Compiler error!"
            return

    #os.execve("/usr/bin/sudo", ["/usr/bin/sudo", "-u", "smalluser", sim_name], {})
    os.execve(sim_name, [sim_name], {})



def main():
    print "Welcome to the Trump Secret Portal"
    while 1:
        res = menu()
        if res == 1:
            read_tweet()
        elif res == 2:
            run_sim()
        elif res == 3:
            exit(0)

if __name__ == "__main__":
    main()


