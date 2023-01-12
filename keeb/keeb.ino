#include <Keyboard.h>

#define NUM_COLS 3
#define NUM_ROWS 3

#define MODE_SW_PIN 8

#define DEBOUNCE 2
#define SCAN_DELAY 300

enum switchMode { NUMPAD = 0,
                  VAL = 1,
                  HELPER = 2,
                  _NUM_MODES = 3 };

static const uint8_t ColPins[NUM_COLS] = { 6, 5, 4 };
static const uint8_t RowPins[NUM_ROWS] = { 3, 2, 1 };
static uint8_t debounce_count[NUM_ROWS][NUM_COLS];
uint8_t pos = 0;

const char keyData[9] = { '1', '2', '3', '4', '5', '6', '7', '8', '9' };
const char *valStrings[11] = {
  "Sheeeeeeeeeeeeeeeeeeeeeeeeesh",
  "You were a boulder. I am a mountain!",
  "How did every piece of trash end up on the same team?",
  "Just some good old hard yakka, standing in between us and victory.",
  "Oi! I'm pissed!",
  "Bloinded",
  "I am on a higher plane, chale, literally!",
  "Activating kill mode. That's a joke. Kill mode is default.",
  "Buy stuff, kaching, lil' skkkrrrr, then we're done, yeah?",
  "Yo!    Nice.",
  "Sheee-achoo!-eeesh!",
};
const char *valPickupStrings[5] = {
  "Are you Cypher? Because I'd give you my corpse.",
  "Are you killjoy? Because i want you to detain me.",
  "Are you Viper? Because your toxicity has me addicted.",
  "I wish I were Omen because I want to teleport into your bed tonight.",
  "You must be be Reyna, because you are sucking more than just my soul.",
};

static unsigned long lastMillis;  // for 1 second counter
static uint8_t currentRow = 0;
static uint8_t currentCol;  // for column loop counters
static uint8_t currentMode;
static char pressedKey;
uint8_t valStrPos = 11;
uint8_t valPUStrPos = 5;

bool lightOn = false;

void setup() {
  Serial.begin(9600);  // use the same baud-rate as the python side
  while (!Serial && millis() < 1000) {}

  Serial.println("log:Starting Macro Pad...");

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

  // Handle input depending on mode
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

  // Every second...
  // 2 * 60 * 1000UL = 2 mins
  if (millis() - lastMillis >= 1000UL) {
    lastMillis = millis();  //get ready for the next iteration
    Serial.print("secmode:");
    Serial.println(currentMode);

    Serial.print("valstr:");
    Serial.println(valStrPos);
  }

  // sendRandomString(valStrings, sizeof(valStrings) / sizeof(valStrings[0]));
}

// Input functions
void handleHelper(bool isDown) {
  if (isDown) {
    _logKeyPressed();

    switch (pressedKey) {
      case '1':
        Keyboard.print('c');
        delay(50);
        Keyboard.print('q');
        delay(50);
        Keyboard.print('e');
        delay(50);
        break;
      case '2':
        _sendValString(getRandomString(valPickupStrings, sizeof(valPickupStrings) / sizeof(valPickupStrings[0])), true);
        break;
      case '3':
        sendOpenIncognito();
        break;
      case '4':
        sendUndo();
        break;
      case '5':
        Keyboard.press(KEY_TAB);
        delay(500);
        Keyboard.press('c');
        delay(50);
        Keyboard.press('c');
        delay(50);
        Keyboard.press('c');
        delay(50);
        Keyboard.press('c');
        delay(100);
        Keyboard.press('v');
        delay(100);
        Keyboard.releaseAll();
        break;
      case '7':
        _sendValString("Hey how about you go touch a fern, eh bud?", true);
        break;
      case '8':
        _sendValString("To become a better person, touch grass, one must.  Hmmmm?", true);
        break;
      case '9':
        _sendValString("So, I guess you're allergic to grass or something?", true);
        break;
      default:
        Keyboard.println("Other keys!");
    }
  }
}


void handleVal(bool isDown) {
  if (isDown) {
    _logKeyPressed();

    switch (pressedKey) {
      case '1':
        // Count valStrPos up 1 or reset
        if (valStrPos > 0) {
          valStrPos -= 1;
        } else {
          valStrPos = 10;
        }
        _sendValString(valStrings[valStrPos], true);
        break;
      case '2':
        if (valPUStrPos > 0) {
          valPUStrPos -= 1;
        } else {
          valPUStrPos = sizeof(valPickupStrings) / sizeof(valPickupStrings[0]);
        }
        _sendValString(valPickupStrings[valPUStrPos], true);
        break;
      case '3':
        // Count valStrPos up 1 or reset
        if (valStrPos < (int)sizeof(valStrings) / sizeof(valStrings[0]) - 1) {
          valStrPos += 1;
        } else {
          valStrPos = 0;
        }
        _sendValString(valStrings[valStrPos], true);
        break;
      case '4':
        _sendValString("gg", true);
        break;
      case '5':
        _sendValString("ggwp", true);
        break;
      case '6':
        _sendValString("ggez", true);
        break;
      case '7':
        _sendValString("nt", false);
        break;
      case '8':
        _sendValString("nice", false);
        break;
      case '9':
        _sendValString("Nice!", false);
        break;
    }

    Serial.print("log:");
    Serial.println(valStrPos);
  }
}

void handleNumPad(bool isDown) {
  if (isDown) {
    _logKeyPressed();
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

void _logKeyPressed() {
  Serial.print("key:");
  Serial.println(pressedKey);
}

// Macro functions
void _sendValString(const char *str, bool isAllChat) {
  // Get into all chat
  if (isAllChat) {
    Keyboard.press(KEY_LEFT_SHIFT);
  }
  Keyboard.press(KEY_RETURN);
  delay(250);
  Keyboard.releaseAll();
  delay(100);

  // Send text
  Keyboard.println(str);
  delay(250);

  // sendRandomString(valStrings, sizeof(valStrings) / sizeof(valStrings[0]));
}

const char *getRandomString(const char **strings, int numStrings) {
  // int idx = random(numStrings);
  int idx = random(numStrings);
  return strings[idx];  // random str
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
