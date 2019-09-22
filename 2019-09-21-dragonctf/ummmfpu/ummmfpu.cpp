// +--+ ummmfpu
//    +--+ Teaser Dragon CTF 2019
//       +--+ by Gynvael Coldwind
//          +--+ HF GL!
//
//   Arduino UNO       uM-FPU (PDIP-18)
//      13 (SCK) ----- (SCLK) 16
//     11 (MOSI) ----- (SIN) 12
//     12 (MISO) ----- (SOUT) 11
//     7 (input) ----- (SOUT) 11
//

#include <SPI.h>
#include <Fpu.h>
#include <FpuSerial.h>

#include "generated.h"

void goodbye() {
  for (;;);
}

// Makes sure FPU is not busy.
void fpu_wait() {
  // Wait at least Minimum Data Period (1.6us) before checking the Ready/Busy pin.
  delayMicroseconds(3);

  while (digitalRead(7) == 1) {
    delayMicroseconds(100);
  }
}

void fpu_force_sync() {
  fpu_wait();

  while (Fpu.sync() != SYNC_CHAR) {
    delay(1);
  }
}

void fpu_eeprom_upload(uint8_t slot, const void *src, size_t sz) {
  const uint8_t *data = (const uint8_t*)src;
  const size_t BATCH_SZ = 4;  // MUST be 4 (slot size).
  fpu_force_sync();

  // Upload BATCH_SZ bytes at a time.
  size_t uploaded = 0;
  size_t next_batch_sz;

  while (uploaded != sz) {
    // Assume FPU is not busy.
    next_batch_sz = (sz - uploaded > BATCH_SZ) ? BATCH_SZ : sz - uploaded;

    bool good_write = false;
    int retry = 0;

    while (1) {
      // Start with verify, since maybe the data is already in place (and
      // EEPROM reads are about 1000 faster on this architecture than writes).
      Fpu.write(EELOAD, 0, slot, LREAD0);
      uint32_t v_eeprom = Fpu.readLong();
      uint32_t v_written = 0;
      if (next_batch_sz >= 1) v_written |= ((uint32_t)data[uploaded + 0] << 0);
      if (next_batch_sz >= 2) v_written |= ((uint32_t)data[uploaded + 1] << 8);
      if (next_batch_sz >= 3) v_written |= ((uint32_t)data[uploaded + 2] << 16);
      if (next_batch_sz == 4) v_written |= ((uint32_t)data[uploaded + 3] << 24);

      uint32_t mask = 0xffffffff >> (8 * (4 - next_batch_sz));
      v_eeprom &= mask;
      v_written &= mask;

      if (v_eeprom == v_written) {
        if (retry == 0) {
          Serial.print('.');
        } else {
          Serial.print('w');
        }
        break;
      } else {
        retry++;

        if (retry > 10) {
          Serial.println("HARD FAIL!");
          Serial.print("\nError at ");
          Serial.print(uploaded);
          Serial.print(": ");
          Serial.print(v_written, HEX);
          Serial.print(" vs ");
          Serial.println(v_eeprom, HEX);
          goodbye();
        }

        if (retry > 1) {
          Serial.print("R");
        }
      }

      // Write to EEPROM.
      Fpu.write(EEWRITE, slot, next_batch_sz);
      for (size_t i = 0; i < next_batch_sz; i++) {
        Fpu.write(data[uploaded + i]);
      }
      fpu_wait();
    }

    // Iterate.
    uploaded += next_batch_sz;
    slot++;

    fpu_wait();
  }
}

void setup()
{
  pinMode(7, INPUT);  // Connected to SOUT to monitor Ready/Busy signal from FPU.

  Serial.begin(9600);

  SPI.begin();
  Fpu.begin();

  if (Fpu.sync() == SYNC_CHAR) {
    char version[16];
    Fpu.write(VERSION);
    Fpu.readString(version);
    Serial.print("FPU version: ");
    Serial.println(version);
    if (strcmp(version, "uM-FPU V3.1.2") != 0) {
      Serial.println("error: incorrect FPU version");
      goodbye();
    }
  } else {
    Serial.println("error: FPU not detected");
    goodbye();
  }
}

void loop() {
  Serial.print("Flashing FPU's EEPROM...");
  fpu_eeprom_upload(task_slot, task, task_sz);
  Serial.println("DONE");

  Serial.println("Please enter the flag/password:");
  Serial.setTimeout(60000UL);
  String flag = Serial.readStringUntil('\n');

  flag.trim();
  if (flag.length() == 0) {
    Serial.println("No flag entered?");
    goodbye();
  }

  Serial.println("Checking...");

  fpu_wait();
  Fpu.write(STRSET);
  for (unsigned int i = 0; i < flag.length(); i++) {
    Fpu.write(flag[i]);
  }
  Fpu.write(0);

  Fpu.write(EECALL, start_slot);
  fpu_wait();

  Serial.print("Result: ");
  FpuSerial.printStringln();

  goodbye();
}
