from __future__ import print_function
from flask import Flask, request, render_template, session, redirect, url_for
import os
import time
import csv
from collections import Counter



try:
    import serial
except ImportError:
    serial = None

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me-before-deploying")

THRESHOLD = 15          # abs difference to count as BENT
NUM_READINGS = 20       # readings for both calibration and detection
NUM_FINGERS = 5
BENT_MIN_COUNT = 2     # how many readings must exceed THRESHOLD to call a finger BENT

# ── GESTURE MAP (loaded from data.csv) ───────────────────────────────────────
# CSV columns: thumb, index, middle, ring, pinky, roll, pitch, motion, gesture
# Key tuple order: (thumb, index, middle, ring, pinky, roll, pitch, motion)
GESTURE_MAP = {}
try:
    with open('data1.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (
                row['thumb'].strip(),
                row['index'].strip(),
                row['middle'].strip(),
                row['ring'].strip(),
                row['pinky'].strip(),
                row['roll'].strip(),
                row['pitch'].strip(),
                row['motion'].strip()
            )
            GESTURE_MAP[key] = row['gesture'].strip()
except FileNotFoundError:
    print("WARNING: data.csv not found. Gesture map is empty.")

GESTURE_UNKNOWN = "WE ARE WORKING ON IT"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/glove')
def glove():
    return render_template(
        "glove.html",
        param=[],
        result=None,
        message="Ready — calibrate your glove first.",
        message_type="ready",
        calibrated=('baseline' in session)
    )


# ── CALIBRATION ──────────────────────────────────────────────────────────────
# Only flex values (first 5) are calibrated here.
# Roll, pitch, motion come pre-calibrated from Arduino.
@app.route('/calibrate', methods=['POST'])
def calibrate():

    if serial is None:
        return render_template(
            "glove.html", param=[], result=None,
            message="pyserial not installed. Run: pip install pyserial",
            message_type="error", calibrated=False
        )

    port = os.getenv("GLOVE_PORT", "COM13")
    baud = int(os.getenv("GLOVE_BAUD", "9600"))

    try:
        ser = serial.Serial(port, baud, timeout=2)
        time.sleep(2)  # let Arduino reset

        readings = []
        start = time.time()

        # Collect exactly NUM_READINGS valid 8-value lines (max 15 sec)
        while len(readings) < NUM_READINGS and (time.time() - start) < 15:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            parts = line.split(",")
            if len(parts) >= 8:
                try:
                    vals = [int(parts[i]) for i in range(NUM_FINGERS)]
                    readings.append(vals)
                except ValueError:
                    continue

        ser.close()

        if not readings:
            return render_template(
                "glove.html", param=[], result=None,
                message="No data received from glove. Check connection.",
                message_type="error", calibrated=False
            )

        # Per-finger average (flex only)
        avg = [0] * NUM_FINGERS
        for r in readings:
            for i in range(NUM_FINGERS):
                avg[i] += r[i]
        avg = [round(v / len(readings)) for v in avg]

        session['baseline'] = avg

        return render_template(
            "glove.html",
            param=avg,
            result=None,
            message=f"Calibration complete! ({len(readings)} readings averaged)",
            message_type="success",
            calibrated=True
        )

    except Exception as e:
        return render_template(
            "glove.html", param=[], result=None,
            message=f"Serial error: {e}",
            message_type="error", calibrated=False
        )


# ── DETECTION ────────────────────────────────────────────────────────────────
@app.route('/detect', methods=['POST'])
def detect():

    if serial is None:
        return render_template(
            "glove.html", param=[], result=None,
            message="pyserial not installed. Run: pip install pyserial",
            message_type="error", calibrated=False
        )

    if 'baseline' not in session:
        return render_template(
            "glove.html", param=[], result=None,
            message="Please calibrate the glove first.",
            message_type="info", calibrated=False
        )

    baseline = session['baseline']
    port = os.getenv("GLOVE_PORT", "COM13")
    baud = int(os.getenv("GLOVE_BAUD", "9600"))

    try:
        ser = serial.Serial(port, baud, timeout=2)
        time.sleep(2)

        readings = []
        start = time.time()

        # Collect exactly NUM_READINGS valid 8-value lines (max 20 sec)
        # Each reading: [flex0, flex1, flex2, flex3, flex4, roll_str, pitch_str, motion_str]
        while len(readings) < NUM_READINGS and (time.time() - start) < 20:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            parts = line.split(",")
            if len(parts) >= 8:
                try:
                    flex = [int(parts[i]) for i in range(NUM_FINGERS)]
                except ValueError:
                    continue
                roll_raw   = parts[5].strip()
                pitch_raw  = parts[6].strip()
                motion_raw = parts[7].strip()
                readings.append(flex + [roll_raw, pitch_raw, motion_raw])

        ser.close()

        if not readings:
            return render_template(
                "glove.html", param=[], result=None,
                message="No data received from glove. Check connection.",
                message_type="error", calibrated=True
            )

        # ── Flex fingers: bent/straight via threshold count ──
        result = []
        for i in range(NUM_FINGERS):
            hit_count = 0
            for r in readings:
                if abs(r[i] - baseline[i]) >= THRESHOLD:
                    hit_count += 1
                    if hit_count >= BENT_MIN_COUNT:
                        break
            bent = hit_count >= BENT_MIN_COUNT
            result.append(f"F{i+1}: {'BENT' if bent else 'STRAIGHT'}")

        # ── Roll / Pitch / Motion: majority vote across all readings ──
        roll_vote   = Counter(r[5] for r in readings).most_common(1)[0][0]
        pitch_vote  = Counter(r[6] for r in readings).most_common(1)[0][0]
        motion_vote = Counter(r[7] for r in readings).most_common(1)[0][0]

        # ── Build 8-tuple lookup key ──
        finger_states = tuple(
            "bent" if "BENT" in result[i] else "straight"
            for i in range(NUM_FINGERS)
        )
        full_key = finger_states + (roll_vote, pitch_vote, motion_vote)
        gesture = GESTURE_MAP.get(full_key, GESTURE_UNKNOWN)

        return render_template(
            "glove.html",
            param=baseline,
            result=result,
            finger_states=finger_states,
            roll=roll_vote,
            pitch=pitch_vote,
            motion=motion_vote,
            gesture=gesture,
            message=f"Detected: {gesture}",
            message_type="success",
            calibrated=True
        )

    except Exception as e:
        return render_template(
            "glove.html", param=[], result=None,
            message=f"Serial error: {e}",
            message_type="error", calibrated=True
        )


# ── OTHER ROUTES (unchanged) ──────────────────────────────────────────────────
@app.route('/trial', methods=['GET', 'POST'])
def trial():
    ans = request.form.get('ans', '')
    session['ans'] = ans
    return render_template('trial.html', ans=ans)


@app.route('/vids')
def vids():
    ans = session.get('ans', '')
    words = ans
    params = []
    if ans:
        for word in ans.split():
            word = word.strip('.,!?;:\'"()-').lower()
            if not word:
                continue
            filename = word + '.mp4'
            filepath = os.path.join(app.root_path, 'static', filename)
            if os.path.exists(filepath):
                params.append(url_for('static', filename=filename))
    return render_template('vids.html', params=params, words=words)


if __name__ == '__main__':
    app.run(debug=True)