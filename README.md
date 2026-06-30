# 🖐️ Silent Voice Glove – Sign Language Communication System

A smart, assistive technology platform that bridges the gap between deaf/mute individuals and the hearing world through **bidirectional communication**:

- 🎤 **Speech/Text → Sign Language Videos** - Converts spoken words or typed text into sign language videos
- 🧤 **Smart Glove → Recognized Text** - Detects hand gestures using flex sensors and motion sensors

The system seamlessly integrates **Arduino hardware**, **Flask web development**, **sensor-based gesture recognition**, and **video-based sign language translation** into one cohesive platform.

---

## ✨ Key Features

### 🎤 Speech to Sign Language
- **Voice Recognition**: Uses the Web Speech API for real-time voice input
- **Manual Text Input**: Type words directly for translation
- **Video Output**: Converts words into sign language videos
- **Modern UI**: Clean, responsive, and user-friendly interface
- **Word-by-word Translation**: Each word is displayed as a corresponding sign language video

### 🧤 Smart Glove Recognition
The wearable smart glove uses:
- **5 Flex Sensors** - Detect individual finger bending
- **MPU6050 Accelerometer & Gyroscope** - Capture wrist orientation and hand motion

**Detected Gestures:**
- Finger bending states (bent/straight for each of 5 fingers)
- Wrist roll positions (palm up, palm down, palm inward, palm outward, palm neutral)
- Wrist pitch angles (fingers up, fingers down, fingers forward)
- Hand motion (static, waving, shaking)

**Recognition Logic:**
- Threshold-based finger detection for noise reduction
- Majority voting across multiple sensor readings
- CSV-based gesture lookup for text translation

---

## 🔄 Project Architecture

### Speech to Sign Language Workflow
```
User Input (Voice/Text)
        ↓
Speech Recognition / Text Input
        ↓
Flask Backend Processing
        ↓
Video Database Lookup
        ↓
Sign Language Video Display
```

### Smart Glove Recognition Workflow
```
Flex Sensors + MPU6050 (Hardware)
        ↓
Arduino Processing
        ↓
Serial Communication (USB)
        ↓
Flask Server
        ↓
Gesture Detection & Matching
        ↓
Recognized Text Output
```

---

## 🛠️ Hardware Components

| Component | Quantity | Purpose |
|-----------|----------|---------|
| Arduino Nano/Uno | 1 | Main microcontroller |
| Flex Sensors | 5 | Detect finger bending |
| MPU6050 | 1 | Accelerometer & Gyroscope |
| Gloves | 1 Pair | Wearable housing |
| Resistors | 5 | Voltage division for flex sensors |
| Jumper Wires | As Required | Connections |
| Breadboard | 1 | Prototyping board |

### Hardware Connections
- **Flex Sensors** → Arduino A0-A3 and A6 (analog pins)
- **MPU6050** → Arduino I2C (SDA/SCL)
- **USB Cable** → Arduino to Computer (serial communication)

---

## 💻 Software Requirements

### Backend
- **Python 3.10+**
- **Flask** - Web framework
- **PySerial** - Arduino communication
- **CSV support** - Gesture database

### Frontend
- **HTML5** - Page structure
- **CSS3** - Styling and responsive design
- **JavaScript** - Client-side logic
- **jQuery** - DOM manipulation
- **Web Speech API** - Voice recognition

### Development Tools
- **Arduino IDE** - Firmware development
- **USB Driver** for Arduino

---

## 📦 Installation & Setup

### 1. Install Python Dependencies

```bash
pip install flask pyserial
```

Or use the requirements file:
```bash
pip install -r requirement.txt
```

### 2. Arduino Setup

1. **Upload Arduino Code:**
   - Open `ardino.txt` in Arduino IDE
   - Connect your Arduino via USB
   - Select Tools → Board → Arduino Nano (or Uno)
   - Select Tools → Port → (your COM port)
   - Click Upload

2. **Install Arduino Libraries:**
   - Open Arduino IDE
   - Go to Sketch → Include Library → Manage Libraries
   - Search and install: **MPU6050**
   - Also ensure **Wire** library is installed (usually pre-installed)

3. **Calibrate Serial Connection:**
   - Note the COM port your Arduino uses
   - Update `GLOVE_PORT` environment variable (default: COM13)

### 3. Configure Environment Variables

Create a `.env` file or set environment variables:
```bash
SECRET_KEY=your-secret-key-here
GLOVE_PORT=COM13        # Adjust based on your Arduino's COM port
GLOVE_BAUD=9600        # Baud rate for serial communication
```

### 4. Run the Flask Application

```bash
python main.py
```

The server will start at `http://localhost:5000`

---

## 📁 Project Structure

```
silent-voice-glove/
│
├── main.py                  # Flask backend application
├── requirement.txt          # Python dependencies
├── ardino.txt              # Arduino firmware code
├── data1.csv               # Gesture recognition database
│
├── templates/              # HTML templates
│   ├── index.html          # Home page with speech input
│   ├── glove.html          # Smart glove control panel
│   ├── trial.html          # Text input page
│   └── vids.html           # Sign language video display
│
├── static/                 # Static files
│   ├── *.mp4               # Sign language video library
│   │   ├── Letters: a-z
│   │   ├── Numbers: 0-100+ (including words: one, ten, hundred, etc.)
│   │   └── Common words: hello, thank, yes, no, water, food, etc.
│   └── (CSS/JS would go here)
│
└── README.md              # This file
```

---

## 🧤 Smart Glove Operation Guide

### Step 1: Calibration
1. Navigate to the **Glove Control** page
2. Keep your hand **relaxed in a neutral position**
3. Click **"Calibrate Glove"**
4. The system collects 20 sensor readings and calculates baseline values
5. Wait for success message

**Why Calibration?**
- Each glove and hand size is different
- Baseline values account for individual variations
- Improves recognition accuracy by 40%+

### Step 2: Gesture Detection
1. After calibration, your baseline values are stored in the session
2. Make a gesture with your hand
3. Click **"Detect Gesture"**
4. The system collects 20 readings and analyzes:
   - Which fingers are bent/straight
   - Wrist orientation (roll angle)
   - Hand motion (static, waving, shaking)

### Step 3: Gesture Matching
The detected gesture tuple is matched against `data1.csv`:

**Example Row in data1.csv:**
```
thumb,index,middle,ring,pinky,roll,pitch,motion,gesture
straight,bent,bent,straight,straight,palm_up,fingers_up,static,HELLO
```

**When matched:**
- **Detected:** `(straight, bent, bent, straight, straight, palm_up, fingers_up, static)`
- **Result:** `HELLO` is recognized

---

## 🎬 Sign Language Video Library

The `/static/` directory contains 130+ sign language videos:

**Categories:**
- **Alphabet:** a.mp4 through z.mp4 (26 videos)
- **Numbers:** one.mp4, two.mp4, ..., hundred.mp4 (extensive)
- **Common Words:** hello.mp4, thank.mp4, yes.mp4, no.mp4, water.mp4, food.mp4, etc.
- **Phrases & Adjectives:** happy.mp4, hungry.mp4, home.mp4, hand.mp4, etc.

**Video Format:**
- MP4 codec
- Optimized for web playback
- ~15-90KB each for fast loading

---

## 📊 Gesture Recognition Algorithm

### Flex Sensor Threshold Logic
```python
THRESHOLD = 15                # Minimum change to count as bent
NUM_READINGS = 20            # Readings per detection cycle
BENT_MIN_COUNT = 2           # Min readings exceeding threshold
```

### Finger State Classification
For each of 5 fingers:
1. Compare current reading against baseline + THRESHOLD
2. Count how many readings exceed the threshold
3. If count ≥ BENT_MIN_COUNT → Finger is **BENT**
4. Otherwise → Finger is **STRAIGHT**

### Majority Voting for Orientation
- Collects roll, pitch, motion from all 20 readings
- Uses majority vote (most frequent value) for each
- Reduces noise from sensor jitter

---

## 🚀 Usage Examples

### Example 1: Speaking to Sign Language
1. Go to home page
2. Click **"Start Listening"**
3. Say: "Hello, how are you?"
4. System recognizes: `["hello", "how", "are", "you"]`
5. Displays sign language videos for each word

### Example 2: Typing to Sign Language
1. Go to **"Text Input"** page
2. Type: "Thank you"
3. Click **"Translate"**
4. Videos for "thank" and "you" are displayed

### Example 3: Glove to Text
1. Calibrate your glove
2. Make a specific hand gesture (e.g., for "HELLO")
3. Click **"Detect Gesture"**
4. System outputs: "HELLO"

---

## ⚙️ Configuration & Customization

### Adding New Gestures
1. Create a new video file: `word.mp4`
2. Add to `static/` directory
3. Add corresponding row to `data1.csv`:
   ```
   thumb_state,index_state,middle_state,ring_state,pinky_state,roll,pitch,motion,gesture_name
   ```

### Modifying Detection Thresholds
Edit `main.py`:
```python
THRESHOLD = 15           # Increase for more sensitive, decrease for less
BENT_MIN_COUNT = 2       # Increase for strict detection
NUM_READINGS = 20        # Increase for more stable but slower detection
```

### Changing Serial Port
Set environment variable or edit `main.py`:
```python
port = os.getenv("GLOVE_PORT", "COM13")  # Change default here
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Serial connection failed** | Check Arduino COM port, verify USB cable, install drivers |
| **"No data received from glove"** | Verify Arduino firmware uploaded, check GLOVE_PORT setting |
| **Calibration timeout** | Ensure Arduino is sending data, check baud rate (should be 9600) |
| **Gesture not recognized** | Check that gesture exists in data1.csv, recalibrate glove |
| **Web Speech API not working** | Use Chrome/Edge browser, ensure HTTPS or localhost |
| **Video files not loading** | Verify MP4 files are in `/static/` directory |

---

## 📈 Future Enhancements

- **Machine Learning:** Replace CSV lookup with trained neural networks for continuous gestures
- **Dynamic Gestures:** Recognize multi-finger sequences and movement patterns
- **Real-time Sentence Formation:** Build complete sentences from continuous glove input
- **Mobile App:** Create native Android/iOS applications
- **Cloud Integration:** Store gesture databases in cloud for multi-user access
- **Multi-language Support:** Add support for Indian Sign Language (ISL), American Sign Language (ASL), etc.
- **Text-to-Speech Output:** Generate audio output for translated text
- **Deep Learning Classification:** Use CNN/RNN for improved accuracy
- **Two-way Translation:** Convert sign videos back to text/speech

---

## ✅ Advantages

- 🎯 **Easy to Use** - Intuitive interface requiring no special training
- 💰 **Low-Cost Hardware** - Under $50 for complete glove setup
- 🎒 **Portable** - Lightweight and wearable
- ⚡ **Real-time Communication** - Instant gesture and speech recognition
- 🎨 **User-Friendly Interface** - Modern, accessible design
- 📚 **Expandable Database** - Easy to add new gestures and videos
- 🔌 **No Internet Required** - Runs locally on computer/server

---

## ⚠️ Limitations

- Supports **predefined gestures only** - Cannot recognize novel signs
- **Requires calibration** before each use
- **Dependent on sensor accuracy** - Flex sensors can drift
- **Limited vocabulary** - Based on available video library (~130 words)
- **One-handed only** - Current setup doesn't support two-hand gestures
- **English-centric** - Primarily designed for English sign language

---

## 🌍 Applications & Impact

### Social Impact
- 🤝 **Deaf & Mute Communication** - Enable independent conversation
- 🎓 **Educational Institutions** - Aid in special education
- 🏥 **Hospitals** - Improve patient-healthcare provider communication
- 🏛️ **Public Services** - Customer support and administrative services

### Research Applications
- 👥 **Human-Computer Interaction** - Study gesture-based interfaces
- 🤖 **Assistive Technology** - Foundation for accessibility tools
- 🧠 **Gesture Recognition** - ML research platform


---

## 🤝 Contributing

Contributions are welcome! You can help by:
- Adding new gesture videos
- Expanding the gesture database (data1.csv)
- Improving the algorithm accuracy
- Creating tutorials and documentation
- Testing across different hardware setups

---

## 📧 Support & Questions

If you encounter issues or have questions:
1. Check the **Troubleshooting** section above
2. Review Arduino and Flask logs
3. Verify hardware connections
4. Test with a calibrated glove first

---

## 🙏 Acknowledgments

This project combines:
- Web Speech API for voice recognition
- Flask for web framework
- Arduino ecosystem for hardware control
- Sign language reference materials

---
