# 🖐️ Silent Voice Glove –  Sign Language Communication System

The project provides **two-way communication**:

- 🎤 **Speech/Text → Sign Language Videos**
- 🧤 **Smart Glove → Recognized Text**

The system combines **Arduino hardware**, **Flask web development**, **Computer Vision concepts**, and **Sensor-based gesture recognition** into one integrated platform.

---

# Features

## 🎤 Speech to Sign Language

- Voice recognition using Web Speech API
- Manual text input support
- Converts words into sign language videos
- Clean and modern user interface

---

## 🧤 Smart Glove Recognition

The smart glove uses:

- 5 Flex Sensors
- MPU6050 Accelerometer & Gyroscope

The glove detects:

- Finger bending
- Wrist orientation
- Hand movement

The detected gesture is compared with predefined gestures stored in a CSV file and translated into text.

---

# Project Workflow

## Speech to Sign

```
User
   │
   ▼
Voice / Text Input
   │
   ▼
Speech Recognition
   │
   ▼
Flask Backend
   │
   ▼
Video Matching
   │
   ▼
Sign Language Videos
```

---

## Smart Glove

```
Flex Sensors + MPU6050
          │
          ▼
      Arduino
          │
          ▼
   Serial Communication
          │
          ▼
      Flask Server
          │
          ▼
Finger Detection
          │
          ▼
Gesture Recognition
          │
          ▼
Recognized Text
```

---

# Hardware Components

| Component | Quantity |
|-----------|---------:|
| Arduino Nano/Uno | 1 |
| Flex Sensors | 5 |
| MPU6050 | 1 |
| Gloves | 1 Pair |
| Resistors | 5 |
| Jumper Wires | As Required |
| Breadboard | 1 |

---

# Software Requirements

- Python 3.10+
- Flask
- PySerial
- Arduino IDE
- HTML
- CSS
- JavaScript
- jQuery

---

# Python Libraries

Install the required libraries using:

```bash
pip install flask pyserial
```

---

# Project Structure

```
SignSpeak/
│
├── app.py
├── data1.csv
│
├── templates/
│   ├── index.html
│   ├── glove.html
│   ├── trial.html
│   └── vids.html
│
├── static/
│   ├── hello.mp4
│   ├── thank.mp4
│   ├── yes.mp4
│   └── ...
│
├── Arduino/
│   └── SmartGlove.ino
│
└── README.md
```

---

# Smart Glove Working

## Step 1 – Calibration

The user keeps the hand relaxed.

The system collects multiple sensor readings and calculates an average value for each flex sensor.

These values become the baseline.

---

## Step 2 – Gesture Detection

The glove continuously reads:

- Flex sensor values
- Roll
- Pitch
- Motion

Finger states are classified as:

- Bent
- Straight

---

## Step 3 – Gesture Recognition

The detected finger states, wrist orientation, and motion are matched against predefined gestures stored in `data1.csv`.

Example:

```
straight,bent,bent,straight,straight,palm_up,fingers_up,static
```

↓

```
HELLO
```

---

# Speech Recognition

The web application uses the browser's Web Speech API to capture speech.

Workflow:

```
Speech

↓

Transcript

↓

Flask

↓

Video Matching

↓

Sign Language Animation
```

---

# Technologies Used

## Frontend

- HTML5
- CSS3
- JavaScript
- jQuery

## Backend

- Python
- Flask

## Hardware

- Arduino
- Flex Sensors
- MPU6050

## Communication

- Serial Communication (USB)

---

# Gesture Recognition Logic

The system performs:

- Flex sensor calibration
- Threshold-based finger detection
- Majority voting
- CSV-based gesture lookup

This improves recognition accuracy by reducing noise from individual sensor readings.

---

# User Interface

The project includes:

- Modern responsive homepage
- Voice recording interface
- Smart glove dashboard
- Live gesture recognition
- Finger status visualization
- Orientation display
- Calibration screen
- Sign language video player

---

# Future Improvements

- Machine Learning-based gesture recognition
- Dynamic gesture detection
- Real-time sentence formation
- Mobile application
- Cloud database integration
- Multi-language support
- Text-to-Speech output
- Deep Learning-based gesture classification

---

# Advantages

- Easy to use
- Low-cost hardware
- Portable
- Real-time communication
- User-friendly interface
- Expandable gesture database

---

# Limitations

- Supports predefined gestures only
- Requires calibration before use
- Depends on sensor accuracy
- Limited vocabulary based on available videos

---

# Applications

- Communication for deaf and mute individuals
- Educational institutions
- Hospitals
- Public service centers
- Customer support
- Smart assistive technology
- Human-computer interaction research

---
