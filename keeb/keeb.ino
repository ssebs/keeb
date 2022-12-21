#include <Keyboard.h>

#define NUM_COLS 3
#define NUM_ROWS 3

#define MODE_SW_PIN 8

#define DEBOUNCE 2
#define SCAN_DELAY 200

enum switchMode { NUMPAD = 0,
                  VAL = 1,
                  HELPER = 2,
                  _NUM_MODES = 3 };

static const uint8_t ColPins[NUM_COLS] = { 6, 5, 4 };
static const uint8_t RowPins[NUM_ROWS] = { 3, 2, 1 };
static uint8_t debounce_count[NUM_ROWS][NUM_COLS];
uint8_t pos = 0;

const char keyData[9] = { '1', '2', '3', '4', '5', '6', '7', '8', '9' };
const char *valStrings[10] = {
  "Sheeeeeeeeeeeeeeeeeeeeeeeeesh",
  "You were a boulder. I am a mountain!",
  "How did every piece of trash end up on the same team?",
  "Just some good old hard yakka, standing in between us and victory.",
  "Oi! I'm pissed!",
  "Bloinded",
  "I am on a higher plane, chale, literally!",
  "Activating kill mode. That's a joke. Kill mode is default.",
  "Buy stuff, kaching, lil' skkkrrrr, then we're done, yeah?",
  "Yo!    Nice."
};
const char *valPickupStrings[5] = {
  "Are you Cypher? Because I'd give you my corpse.",
  "Are you killjoy? Because i want you to detain me.",
  "Are you Viper? Because your toxicity has me addicted.",
  "I wish I were Omen because I want to teleport into your bed tonight.",
  "You must be be Reyna, because you are sucking more than just my soul.",
};

static uint8_t currentRow = 0;
static uint8_t currentCol;  // for column loop counters
static uint8_t currentMode;
static char pressedKey;

bool lightOn = false;

void setup() {
  Serial.begin(2000000);  // use the same baud-rate as the python side
  while (!Serial && millis() < 1000) {}

  Serial.println("Starting Macro Pad...");

  // Setup row pins
  uint8_t i;
  for (i = 0; i < NUM_ROWS; i++) {
    pinMode(RowPins[i], OUTPUT);
    digitalWrite(RowPins[i], HIGH);
    delay(100);
  }
  // Setup col pins
  for (i = 0; i < NUM_COLS; i++) {
    pinMode(ColPins[i], INPUT_PULLUP);
  }

  // Setup extras
  pinMode(MODE_SW_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);

  currentMode = NUMPAD;
  Keyboard.begin();
}

void loop() {
  // Mode switch
  if (digitalRead(MODE_SW_PIN) == LOW) {
    if (currentMode >= _NUM_MODES - 1) {
      currentMode = NUMPAD;
    } else {
      currentMode += 1;
    }
    if (lightOn) {
      digitalWrite(LED_BUILTIN, LOW);
      lightOn = !lightOn;
    } else {
      digitalWrite(LED_BUILTIN, HIGH);
      lightOn = !lightOn;
    }
    Serial.print("mode:");
    Serial.println(currentMode);
    delay(500);
  }

  switch (currentMode) {
    case NUMPAD:
      _handleInput(&handleNumPad);
      break;
    case VAL:
      _handleInput(&handleVal);
      break;
    case HELPER:
      _handleInput(handleHelper);
      break;
    default:
      Serial.println("default mode, how'd you get here?");
      break;
  }

  // sendRandomString(valStrings, sizeof(valStrings) / sizeof(valStrings[0]));
}

// Input functions
void handleHelper(bool isDown) {
  if (isDown) {
    switch (pressedKey) {
      case '1':
        Keyboard.press(KEY_LEFT_SHIFT);
        Keyboard.press(KEY_RETURN);
        delay(500);
        Keyboard.releaseAll();
        Keyboard.println("gg");
        break;
      case '2':
        sendRandomString(valPickupStrings, sizeof(valPickupStrings) / sizeof(valPickupStrings[0]));
        break;
      case '3':
        sendOpenIncognito();
        break;
      case '4':
        sendUndo();
        break;
      default:
        Keyboard.println("Other keys!");
    }
  }
}

void handleVal(bool isDown) {
  if (isDown) {
    sendValString();
  }
}

void handleNumPad(bool isDown) {
  if (isDown) {
    Keyboard.print(pressedKey);
  } else {
  }
}

void _handleInput(void (*funcPtr)(bool)) {
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

          // Key press
          pressedKey = keyData[pos];
          funcPtr(true);
        }
      }
    } else  // Otherwise, button is released
    {
      if (debounce_count[currentRow][currentCol] > 0) {
        // Decrement debounce counter
        debounce_count[currentRow][currentCol]--;
        if (debounce_count[currentRow][currentCol] == 0) {  // If debounce counter hits 0

          // Release key press
          pressedKey = keyData[pos];
          funcPtr(false);
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


// Macro functions
void sendValString() {
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press(KEY_RETURN);
  delay(500);
  Keyboard.releaseAll();

  sendRandomString(valStrings, sizeof(valStrings) / sizeof(valStrings[0]));
}

void sendRandomString(const char **strings, int numStrings) {
  // int idx = random(numStrings);
  int idx = random(numStrings);
  Keyboard.println(strings[idx]);  // random str
  delay(500);
}

void sendShutdown() {
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  delay(500);
  Keyboard.releaseAll();

  // Keyboard.println("shutdown /s");
  Keyboard.println("msinfo32");
}

void sendOpenIncognito() {
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('1');
  delay(500);
  Keyboard.releaseAll();

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press('n');
  delay(500);
  Keyboard.releaseAll();
}

void sendUndo() {
  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press('z');
  delay(500);
  Keyboard.releaseAll();
}
