// thermometer and photometer, sensing the heat and light of enviornment
// actuators for controlling enviornment: fan for heat, LEDs for brightness

int thermalIn = A0;
int thermalOut = 6;
int lightIn = A1;
int lightOut = 7;
float temperature = 0;
int brightness = 0;
float maxT;
int minBright;
const int IGNORE_AUTO = -999;  // value that tells us to ignore this auto setting
char c;
String str;
boolean autoOn;
boolean fanOn;
boolean lightOn;


void setup() {
  pinMode(thermalOut, OUTPUT);
  pinMode(lightOut, OUTPUT);
  maxT = IGNORE_AUTO;
  minBright = IGNORE_AUTO;
  autoOn = false;
  fanOn = false;
  lightOn = false;
  Serial.begin(9600);  // transmits 9600 bits per second
}

void loop() {
  str = "";
  while (Serial.available()) {
    c = Serial.read();
    str += c;
    if (str == "read") {      
      Serial.print("Temperature: ");
      Serial.print("<span style='color:blue'>");
      Serial.print(temperature, 2);      
      Serial.println(" C");
      Serial.print("</span>");
      Serial.print("Light level (0-100, 0=dark, 100=bright): ");
      Serial.print("<span style='color:blue'>");
      Serial.println(brightness);
      Serial.print("</span>");
      
      
      Serial.print("Light: ");
      if (lightOn) Serial.println("<span style='color:green'>ON</span>");
      else Serial.println("<span style='color:red'>OFF</span>");
      
      Serial.print("Fan: ");
      if (fanOn) Serial.println("<span style='color:green'>ON</span>");
      else Serial.println("<span style='color:red'>OFF</span>");
 
      Serial.print("Auto: ");
      if (autoOn) {
        Serial.println("<span style='color:green'>ON</span>");
        Serial.print("Minimum Temperature: ");
        Serial.print(maxT);
        Serial.println(" C.");
        Serial.print("Minimum Brightness: ");
        Serial.println(minBright);
        Serial.println();
      }
      else Serial.println("<span style='color:red'>OFF</span>");
      Serial.println();    
    } else if (str == "light on") {
      lightOn = true;
    } else if (str == "light off") {
      lightOn = false;
    } else if (str == "fan on") {
      fanOn = true;
    } else if (str == "fan off") {
      fanOn = false;
    } else if (str == "auto") {  // auto [Temp] [Bright]
      maxT = Serial.parseInt();
      minBright = Serial.parseInt();
      if (maxT != IGNORE_AUTO && minBright != IGNORE_AUTO) autoOn = false;
      else autoOn = true;
    }
    delay(50);
  }
  // read temp and light
  temperature = analogRead(thermalIn) * 0.004882814;  // convert temp to volts, see TMP36 docs
  temperature = (temperature - 0.5) * 100;
  brightness = analogRead(lightIn);
  brightness = map(brightness, 0, 900, 100, 0);  // convert range from 0-900 to 0-100
  
  // auto control
  if (autoOn) {
    fanOn = (temperature > maxT);
    lightOn = (brightness < minBright);
  }
  
  // turn lights on
  if (lightOn) {
    digitalWrite(lightOut, HIGH);
  } else {
    digitalWrite(lightOut, LOW);
  }
  
  // turn motor on for some time then off again
  if (fanOn) {
    digitalWrite(thermalOut, HIGH);
  } else {
    digitalWrite(thermalOut, LOW);
  }
  delay(1000);
    
}
