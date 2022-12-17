#include <Keyboard.h>

#define NUM_COLS 3
#define NUM_ROWS 3

#define DEBOUNCE 2
#define SCAN_DELAY 200

static const uint8_t ColPins[NUM_COLS] = { 6, 5, 4 };
static const uint8_t RowPins[NUM_ROWS] = { 3, 2, 1 };
static uint8_t debounce_count[NUM_ROWS][NUM_COLS];
uint8_t pos = 0;

const char keyData[9] = { '1', '2', '3', '4', '5', '6', '7', '8', '9' };
static uint8_t currentRow = 0;
static uint8_t currentCol;  // for column loop counters

void setup() {
  Serial.begin(9600);

  // Setup row pins
  uint8_t i;
  for (i = 0; i < NUM_ROWS; i++) {
    pinMode(RowPins[i], OUTPUT);
    digitalWrite(RowPins[i], HIGH);
  }
  // Setup col pins
  for (i = 0; i < NUM_COLS; i++) {
    pinMode(ColPins[i], INPUT_PULLUP);
  }
}

void loop() {
  // Select current row
  digitalWrite(RowPins[currentRow], LOW);
  // add a slight delay
  delayMicroseconds(SCAN_DELAY);

  // Scan through switches on this row:
  for (currentCol = 0; currentCol < NUM_COLS; currentCol++) {

    if (digitalRead(ColPins[currentCol]) == LOW) {
      if (debounce_count[currentRow][currentCol] < DEBOUNCE) {
        debounce_count[currentRow][currentCol]++;
        // If debounce counter hits MAX_DEBOUNCE, trigger key press
        if (debounce_count[currentRow][currentCol] == DEBOUNCE) {
          Serial.print("ROW:");
          Serial.println(currentRow);
          Serial.print(" COL:");
          Serial.println(currentCol);
          Serial.println(" PRESSED");
          Serial.print(pos);
          Serial.println(" POS");

          Keyboard.press(keyData[pos]);
        }
      }
    } else  // Otherwise, button is released
    {
      if (debounce_count[currentRow][currentCol] > 0) {
        // Decrement debounce counter
        debounce_count[currentRow][currentCol]--;
        if (debounce_count[currentRow][currentCol] == 0) {  // If debounce counter hits 0
          Keyboard.release(keyData[pos]);
        }
      }
    }
    pos++;
  }

  // Once done scanning, de-select the row pin
  digitalWrite(RowPins[currentRow], HIGH);
  // Increment currentRow, so next time we scan the next row
  currentRow = (currentRow > NUM_ROWS - 2) ? 0 : currentRow + 1;
  if (currentRow == 0) pos = 0;
}



// #include <Keyboard.h>

// // Rows
// #define R0 1
// #define R1 2
// #define R2 3

// // Cols
// #define C1 6
// #define C2 5
// #define C3 4

// bool hasPressed = false;

// void setup() {
//   // Setup cols
//   pinMode(R0, OUTPUT);
//   pinMode(R1, OUTPUT);
//   pinMode(R2, OUTPUT);
//   digitalWrite(R0, LOW);
//   digitalWrite(R1, LOW);
//   digitalWrite(R1, LOW);

//   // Rows
//   pinMode(C1, INPUT_PULLUP);
//   pinMode(C2, INPUT_PULLUP);
//   pinMode(C3, INPUT_PULLUP);

// }

// void loop() {
//   delay(200);

//   for (int i = 1;  i < 4; i++) {
//     if (hasPressed) {
//       hasPressed = false;
//       break;
//     }
//     // Set row val temporarily
//     digitalWrite(i, HIGH);

//     if (digitalRead(C1) == LOW) {
//       hasPressed = true;
//       Serial.print("Pressed row: ");
//       Serial.print(i);
//       Serial.print(", col: 1\n");
//     }
//     if (digitalRead(C2) == LOW) {
//       Serial.println("pressed c1 r0");
//     }

//     digitalWrite(i, LOW);
//   }
// }
