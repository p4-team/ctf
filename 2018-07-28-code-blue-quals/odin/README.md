# Odin Part 1 (part 2 below), re, 334p, 16 solves

> Problem
> Statement
> I’ve installed a smart lock device to the entrance door of my home a while ago.
> The smart lock can be controlled using a smartphone app over Bluetooth Low Energy.
> I noticed, a few times since the installation, that there're some traces left in my home like someone trespassed.
> I really suspect that there’s a hidden backdoor in the smart lock.
> Could you find out the backdoor command for unlocking the door?
> 
> The genuine smartphone app unlocks the door with 1 byte length command "91" (in hex) after authorization.
> Your task is to build another command bytes to unlock the door.
> 
> I’ve got a firmware dump from BLE SoC on the smart lock board (nRF52832) using SWD and captured BLE packets on genuine app’s unlocking operation.
> I also analyzed the smartphone app for smart lock and wrote a document of BLE communication protocol between the app and the smart lock.
> Here is it.
> 
> Files
> Firmware dump (Memory dump of 0x00000000-0x00080000):
> memdump_00000000_00080000.bin
> 
> Captured BLE packets of genuine app’s unlocking operation:
> genuine_app_unlock_operation.pcap
> 
> Communication protocol
> Structure
> Every request from the app to the smart lock is written to Characteristic 38451401-282b-58d1-d5fe-9e95bb5abded as a byte array.
> Every response from the smart lock to the app is sent as a byte array using Notification.
> The smart lock does not have any other Services/Characteristics.
> 
> Request format is (1 byte length command number) + (variable length payload).
> Response format is (1 byte length error number) + (variable length payload).
> 
> Known commands
> CMD_GET_CHALLENGE
> Number: 0x00
> Request/Response payload length: 0/16
> Description
> Retrieve a ramdom challenge bytes for CMD_AUTHORIZE.
> 
> CMD_AUTHORIZE
> Number: 0x01
> Request/Response payload length: 16/0
> Description:
> Authorize the sender for operating the smart lock.
> 
> Payload is aes_ecb_encrypt(key = (Secret bytes set with CMD_INITIALIZE), cleartext = (Challenge bytes retrieved with CMD_GET_CHALLENGE)).
> 
> CMD_GET_INFO
> Number: 0x10
> Request/Response payload length: 1/variable
> Description:
> Retrieve information from the smart lock.
> 
> Request payload format is (1 byte information type).
> Response payload format is (variable length information).
> 
> Known information types are 0x00 for INFO_AUTH_STATE and 0x01 for INFO_TIME.
> INFO_AUTH_STATE is 1 byte length and can be 0x00 (not authorized) or 0x01 (authorized).
> INFO_TIME is 7 byte length.
> A sample code for the time encoding is at https://github.com/SWITCHSCIENCE/samplecodes/blob/bd1b04fc657d58787cbad00297146812ac8d95d2/PCF2129AT_breakout/mbed/Test_PCF2129AT/main.cpp .
> 
> CMD_INITIALIZE
> Number: 0x80
> Request/Response payload length: 16/0
> Description:
> Set secret bytes for the authorization with CMD_AUTHORIZE.
> 
> This command is only sent in device installation time.
> 
> CMD_SET_TIME
> Number: 0x81
> Request/Response payload length: 7/0
> Description:
> Set current time.
> 
> Time encoding is the same with CMD_GET_INFO + INFO_TIME.
> 
> CMD_LOCK
> Number: 0x90
> Request/Response payload length: 0/0
> Description:
> Lock the door.
> 
> CMD_UNLOCK
> Number: 0x91
> Request/Response payload length: 0/0
> Description:
> Unlock the door.
> 
> Known error numbers
> Error number will be 0x00 on success, and other numbers on failure.
> Known numbers are the followings.
> 
> ERR_SUCCESS = 0x00
> ERR_INVALID_LENGTH = 0x01
> ERR_INVALID_DATA = 0x02
> ERR_INVALID_CMD = 0x03
> ERR_NOT_AUTHORIZED = 0x10
> 
> Flag Format
> The backdoor command for unlocking the door is the flag.
> If the command is “12 34 ab cd” in hex, the flag will be “CBCTF{1234abcd}”.

In this problem we got two files, ARM firmware memory dump, and Bluetooth packet dump. From task description we knew the
apparent protocol, as well as that there is a backdoor hidden in firmware allowing to open doors without authentication.
Searching the firmware for protocol constants, such as 0x91, we found function responsible for packet dispatch.
It was fairly straightforward and in line with the description, with one exception: there was additional undocumented
command 0x20. It checked 8 following bytes, four of which had to be equal to part of device's MAC address, and
the other four random-looking constant. If they matched, tenth byte was checked and depending on its value, door
was locked or unlocked. The only thing we didn't get from the firmware was the MAC address - thankfully it
was transmitted and captured in packet dump. With all the information gathered, we could craft backdoor packet.

# Odin Part 2, re, 335p, 13 solves
> Problem
> Statement
> This smart lock has a logging function that records every operation.
> The log is readable only by some special management device.
> Though I don’t have the device, I’ve got a EEPROM dump on the smart lock board which looks like holding the log.
> Could you analyze it and find out when the backdoor was exploited for the first time?

> File
> eeprom.bin

> Flag format
> Flag format is CBCTF{YYYYMMDDhhmmss}.
> If the date is 2018/07/01 12:34:56, the flag will be “CBCTF{20180701123456}”.

The firmware indeed wrote some data to EEPROM just before dispatching Bluetooth packets. It logged each
packet in 16-byte chunks, first 7 of which were packed timestamp, and the remainder - packet payload. The whole
block was AES encrypted with constant key. After decrypting EEPROM blocks, decoding timestamps, we looked
for packets starting with 0x20 byte, i.e. backdoor command. There were only two of these, and the first one
corresponded to time of compromise. Code:

```python
from Crypto.Cipher import AES

key = "88AD3D8347B8CE82082064B4618D7637".decode("hex")
a = AES.new(key, AES.MODE_ECB)

data = open("eeprom", "rb").read()

for i in range(len(data) / 16):
    line = data[i*16:i*16+16]
    if line == "\xff" * 16:
        break
    line = a.decrypt(line)

    date = line[:7]
    payload = line[7:]

    if payload[0] == ' ':
        print date.encode("hex"),
        print payload.encode("hex")

        cmd = [ord(x) for x in date]
        dts  = ((cmd[0] >> 4) * 10) + (cmd[0] & 0x0F);
        dtm  = ((cmd[1] >> 4) * 10) + (cmd[1] & 0x0F);
        dth  = ((cmd[2] >> 4) * 10) + (cmd[2] & 0x0F);
        dtd  = ((cmd[3] >> 4) * 10) + (cmd[3] & 0x0F);
        dtwd = ((cmd[4] >> 4) * 10) + (cmd[4] & 0x0F);
        dtmm = ((cmd[5] >> 4) * 10) + (cmd[5] & 0x0F);
        dty  = ((cmd[6] >> 4) * 10) + (cmd[6] & 0x0F);

        print dty, dtmm, dtd
        print dth, dtm, dts

```

