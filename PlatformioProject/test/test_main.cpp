#include <Arduino.h>
#include <unity.h>
#include <math.h>

extern "C" {

void serialBegin() {
	Serial.begin(9600);
}

void printStr(const char *str) {
	Serial.print(str);
}

void printlnStr(const char *str) {
	Serial.println(str);
}

void printInteger(int i) {
	Serial.print(i);
}

void printlnInteger(int i) {
	Serial.println(i);
}

int divide(int a, int b) {
	//always floor to remove unexpected behaviour
	return floor(a / b);
}



// void smartPrint(const char *str);

void ScolangMain();

int multi(int a, int b);
int add(int a, int b);
int subtract(int a, int b);
int divF(int num, int denom);

bool even(unsigned int i);
bool odd(unsigned int i);
int sommig(int i);

bool greater(int a, int b);
int power(int base, int exponent);

}


// copied from the reader
unsigned int sommigReference(unsigned int n) 
{
    unsigned int result = 0;
    while (n >= 1)
    {
        result += n;
        n--;
    }
    return result;
}

void testMulti() {
	TEST_ASSERT_EQUAL(36, multi(6, 6));
	TEST_ASSERT_EQUAL(12, multi(6, 2));
	TEST_ASSERT_EQUAL(24, multi(3, 8));
	TEST_ASSERT_EQUAL(12, multi(2, 6));

	// one or more negative
	TEST_ASSERT_EQUAL(-12, multi(-2, 6));
	TEST_ASSERT_EQUAL(-12, multi(2, -6));
	TEST_ASSERT_EQUAL(12, multi(-2, -6));

	// one of the numbers is 0
	TEST_ASSERT_EQUAL(0, multi(2, 0));
	TEST_ASSERT_EQUAL(0, multi(0, 2));
	TEST_ASSERT_EQUAL(0, multi(0, 0));
}

void testPower(){
	TEST_ASSERT_EQUAL(pow(2,3), power(2, 3));
	TEST_ASSERT_EQUAL(pow(5,5), power(5, 5));
	TEST_ASSERT_EQUAL(pow(0,0), power(0, 0));
	TEST_ASSERT_EQUAL(pow(5,0), power(5, 0));
	TEST_ASSERT_EQUAL(pow(0,5), power(0, 5));
	TEST_ASSERT_EQUAL(pow(4,4), power(4, 4));
}

void testDivide(){
	TEST_ASSERT_EQUAL(floor(2/1), 	divF(2,1));
	TEST_ASSERT_EQUAL(floor(4/1), 	divF(4,1));
	TEST_ASSERT_EQUAL(floor(14/7), 	divF(14,7));
	TEST_ASSERT_EQUAL(floor(12/13), divF(12,13));
	TEST_ASSERT_EQUAL(floor(2/4), 	divF(2,4));
	TEST_ASSERT_EQUAL(floor(20/3), 	divF(20,3));
	TEST_ASSERT_EQUAL(floor(50/7), 	divF(50,7));
	// negative
	TEST_ASSERT_EQUAL(floor(-50/7), divF(-50,7));
	TEST_ASSERT_EQUAL(floor(50/-7), divF(50,-7));

	TEST_ASSERT_EQUAL(floor(-2/4), 	divF(-2,4));
	TEST_ASSERT_EQUAL(floor(2/-4), 	divF(2,-4));

	TEST_ASSERT_EQUAL(floor(0/5), 	divF(0,5));
  //TEST_ASSERT_EQUAL(floor(5/0),   divF(5,0));   // division by 0 should never work
	TEST_ASSERT_EQUAL(floor(1/7), 	divF(1,7));

}

void testAdd(){
	TEST_ASSERT_EQUAL(10, add(5, 5));

	TEST_ASSERT_EQUAL(5,  add(5, 0)); 
	TEST_ASSERT_EQUAL(5,  add(0, 5)); 
	TEST_ASSERT_EQUAL(0,  add(0, 0)); 

	TEST_ASSERT_EQUAL(6,  add(1, 5)); 
	TEST_ASSERT_EQUAL(6,  add(5, 1)); 

}

void testSubtract(){
	TEST_ASSERT_EQUAL(0,  subtract(5, 5)); 

    TEST_ASSERT_EQUAL(5,  subtract(5, 0)); 
    TEST_ASSERT_EQUAL(-5, subtract(0, 5));
    TEST_ASSERT_EQUAL(0,  subtract(0, 0)); 

    TEST_ASSERT_EQUAL(-4, subtract(1, 5));
    TEST_ASSERT_EQUAL(4,  subtract(5, 1)); 
}

void testEven() {
	TEST_ASSERT_EQUAL(true, even(2));
	TEST_ASSERT_EQUAL(true, even(20));
	TEST_ASSERT_EQUAL(true, even(194));
	TEST_ASSERT_EQUAL(true, even(2488));

	TEST_ASSERT_EQUAL(false,even(13));
	TEST_ASSERT_EQUAL(false,even(13));
	TEST_ASSERT_EQUAL(false,even(1963));
	TEST_ASSERT_EQUAL(false,even(875));
}

void testOdd() {

	TEST_ASSERT_EQUAL(true, odd(1));
	TEST_ASSERT_EQUAL(true, odd(3));
	TEST_ASSERT_EQUAL(true, odd(53));
	TEST_ASSERT_EQUAL(true, odd(1831));

	TEST_ASSERT_EQUAL(false,odd(2));
	TEST_ASSERT_EQUAL(false,odd(732));
	TEST_ASSERT_EQUAL(false,odd(26));
	TEST_ASSERT_EQUAL(false,odd(42)); // the answer to everything... just not this assertion
}

void testSommig()
{
    for (int i = 0; i < 2000; i++)
    {
        TEST_ASSERT_EQUAL(sommigReference(i), sommig(i));
    }
}

void testGreater(){
	TEST_ASSERT_EQUAL(true,greater(6,3));
	TEST_ASSERT_EQUAL(true,greater(12,6));
	TEST_ASSERT_EQUAL(true,greater(378,1));
	TEST_ASSERT_EQUAL(true,greater(672,0));

	TEST_ASSERT_EQUAL(false,greater(2,3));
	TEST_ASSERT_EQUAL(false,greater(6,12));
	TEST_ASSERT_EQUAL(false,greater(1,278));
	TEST_ASSERT_EQUAL(false,greater(0,624));
}


void setup() {
	serialBegin();
	// platformio recommended delay of 2 sec to establish serial connection
	delay(2000);

#ifdef UNIT_TEST
	UNITY_BEGIN(); // start UNIT_TESTS

	// BuiltIn operators
	RUN_TEST(testMulti);
	RUN_TEST(testAdd);
	RUN_TEST(testSubtract);
	RUN_TEST(testDivide);

	// Code criteria examples testing
	RUN_TEST(testEven);
	RUN_TEST(testOdd);
	RUN_TEST(testSommig);

	// Testing extra code functionality common math functions
	RUN_TEST(testGreater);
	RUN_TEST(testPower);

	// if you want to test arduino code comment UNITY_END() below
	UNITY_END(); // end UNIT_TESTS
  #endif      
}

void loop() {

	ScolangMain();
	Serial.println("End of test");
#ifdef UNIT_TEST
	UNITY_END();
#endif
	//exit(0); // or use [Ctrl]+[C] to exit monitor
	Serial.end();
}