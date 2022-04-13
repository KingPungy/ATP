#ifdef UNIT_TEST
// to not have duplicate Definitions during unit testing
#else
#include <Arduino.h>

extern "C"
{
  void ScolangMain();

  void serialBegin()
  {
    Serial.begin(9600);
  }

  void printStr(const char *str)
  {
    Serial.print(str);
  }

  void printlnStr(const char *str)
  {
    Serial.println(str);
  }

  void printInteger(int i)
  {
    Serial.print(i);
  }

  void printlnInteger(int i)
  {
    Serial.println(i);
  }

  int divide(int a, int b)
  {
    return a / b;
  }
}

void setup()
{
  serialBegin();       
  printlnStr("Start"); 
  Sleep(1000);


  ScolangMain();         
  printlnStr("End");   
}

void loop()
{
  // Arduino gets big mad without this function
  int iter = 5;
  while (iter < 5){
    printlnStr("Text"); 
    iter++;
  }
  printlnStr("\n========\n"); 
  delay(1000);
  //exit(0); // or use [Ctrl]+[C] to exit monitor
}
#endif