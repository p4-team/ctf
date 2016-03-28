#include <Keypad.h>

int a;
int b;
int c;
int d;
int e;
int f;
int g;
int h;
int i;

char numUm;
char numDois;

const byte numRows= 4; 
const byte numCols= 4; 
char keymap[numRows][numCols]=
{
{'1', '2', '3', 'A'},
{'4', '5', '6', 'B'},
{'7', '8', '9', 'C'},
{'*', '0', '#', 'D'}
};
byte rowPins[numRows] = {53,52,51,50}; 
byte colPins[numCols]= {49,48,47,46}; 

Keypad myKeypad= Keypad(makeKeymap(keymap), rowPins, colPins, numRows, numCols);


void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);
  pinMode(4, OUTPUT);
  pinMode(5, INPUT);
  pinMode(6, OUTPUT);
  pinMode(7, INPUT);
  pinMode(8, OUTPUT);
  pinMode(9, INPUT);
  pinMode(22, OUTPUT);
  pinMode(23, INPUT);
  pinMode(24, OUTPUT);
  pinMode(25, INPUT);
  pinMode(26, OUTPUT);
  pinMode(27, INPUT);
  pinMode(28, OUTPUT);
  pinMode(29, INPUT);
  Serial.begin(9600);
}

void loop() {
  char keypressed = myKeypad.getKey();
  if (keypressed != NO_KEY){
    if (i == 0){
      numUm = keypressed;
      i = i+1;
      Serial.print(numUm);
    }else{
      if (i == 1){
        numDois = keypressed;
        Serial.print(numDois);
        i = 10;
      }
    }
  }
  if (i == 10){  
    if ((numUm == '1') && (numDois == '3')){
      voto('pt');  
    }
    if ((numUm == '1') && (numDois == '6')){
      voto('pstu');
    }
    if ((numUm == '2') && (numDois == '0')){
      voto('psc');
    }
    if ((numUm == '2') && (numDois == '1')){
      voto('pcb');
    }
    if ((numUm == '2') && (numDois == '7')){
      voto('psdc');
    }
    if ((numUm == '2') && (numDois == '8')){
      voto('prtb');
    }
    if ((numUm == '2') && (numDois == '9')){
      voto('pco');
    }
    if ((numUm == '4') && (numDois == '0')){
      voto('psb');
    }
    if ((numUm == '4') && (numDois == '3')){
      voto('pv');
    }
    if ((numUm == '4') && (numDois == '5')){
      voto('psdb');
    }
    if ((numUm == '5') && (numDois == '0')){
      voto('psol');
    }
   i = 0; 
  }
}

void voto(char partido){
  switch(partido){
    case 'pt':
      digitalWrite(2, HIGH);
      delay(10);
      digitalWrite(4, HIGH);
      delay(10);
      digitalWrite(6, HIGH);
      delay(10);
      digitalWrite(8, LOW);
      delay(10);
      digitalWrite(22, LOW);
      delay(10);
      digitalWrite(24, HIGH);
      delay(10);
      digitalWrite(26, LOW);
      delay(10);
      digitalWrite(28, HIGH);

      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9);
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27) + 1;
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29) - 1;
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'pstu':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, LOW);
      digitalWrite(22, LOW);
      digitalWrite(24, LOW);
      digitalWrite(26, LOW);
      digitalWrite(28, HIGH);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9) + 1;
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27) + 1;
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29) - 1;
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'psc':
      digitalWrite(2, HIGH);
      digitalWrite(4, LOW);
      digitalWrite(6, HIGH);
      digitalWrite(8, LOW);
      digitalWrite(22, HIGH);
      digitalWrite(24, LOW);
      digitalWrite(26, HIGH);
      digitalWrite(28, LOW);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9);
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29);
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'pcb':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, LOW);
      digitalWrite(22, HIGH);
      digitalWrite(24, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(28, HIGH);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9) + 1;
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29);
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'psdc':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, LOW);
      digitalWrite(22, HIGH);
      digitalWrite(24, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(28, LOW);  
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9);
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29) - 1;
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'prtb':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, HIGH);
      digitalWrite(22, LOW);
      digitalWrite(24, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(28, HIGH);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9);
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29);
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'pco':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, LOW);
      digitalWrite(22, LOW);
      digitalWrite(24, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(28, LOW);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9) + 1;
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29) - 1;
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'psb':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, LOW);
      digitalWrite(8, HIGH);
      digitalWrite(22, LOW);
      digitalWrite(24, HIGH);
      digitalWrite(26, LOW);
      digitalWrite(28, HIGH);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9);
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23);
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27) + 1;
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29);
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'pv':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, LOW);
      digitalWrite(22, HIGH);
      digitalWrite(24, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(28, LOW);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9) + 1;
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29) - 1;
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'psdb':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, HIGH);
      digitalWrite(22, LOW);
      digitalWrite(24, LOW);
      digitalWrite(26, HIGH);
      digitalWrite(28, HIGH);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9);
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23) - 1;
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29);
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    case 'psol':
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(6, HIGH);
      digitalWrite(8, HIGH);
      digitalWrite(22, LOW);
      digitalWrite(24, HIGH);
      digitalWrite(26, HIGH);
      digitalWrite(28, LOW);
      
      a = digitalRead(3);
      Serial.print(a);
      Serial.print('-');
      b = digitalRead(5);
      Serial.print(b);
      Serial.print('-');
      c = digitalRead(7);
      Serial.print(c);
      Serial.print('-');
      d = digitalRead(9);
      Serial.print(d);
      Serial.print('-');
      e = digitalRead(23);
      Serial.print(e);
      Serial.print('-');
      f = digitalRead(25);
      Serial.print(f);
      Serial.print('-');
      g = digitalRead(27);
      Serial.print(g);
      Serial.print('-');
      h = digitalRead(29) - 1;
      Serial.print(h);
      Serial.println(" ");
      delay(100);
    default:
      Serial.print('Here is your flag - FLAGGGGGGG');
  }
}
