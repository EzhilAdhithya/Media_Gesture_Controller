# Gesture-Based Volume and Media Controller

A sophisticated Python application that enables hands-free control of your system's volume and media playback using computer vision and hand gesture recognition.

## Features

- **Dual Mode Operation**: Smart switching between Media Control and Volume Control modes
- **Media Control**: Play/pause media using hand gestures (fist and open palm)
- **Volume Control**: Precise volume adjustment with thumb and index finger distance
- **Smart Mute/Unmute**: Automatic mute when fingers are close together
- **Smooth Controls**: Advanced smoothing algorithms with dead zone for stable operation
- **Visual Feedback**: Real-time display of hand tracking, current mode, and control status
- **Gesture Cooldown**: Prevents accidental repeated actions

## Prerequisites

- Python 3.7 or higher
- Webcam (built-in or external)
- Windows OS (required for PyCaw volume control)
- Internet connection (for initial MediaPipe model download)

## Installation

1. Clone this repository or download the source code
2. Create a virtual environment (recommended):
   ```bash
   python -m venv gesture_env
   gesture_env\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python gesture_volume_control.py
   ```

2. Position your hand in front of the camera within view

3. Press 'q' to exit the application

## Gesture Controls

### Media Control Mode (Default)
- **Fist**: Pause media playback
- **Open Palm**: Resume/play media
- **Any other gesture**: Maintains media mode

### Volume Control Mode
- **Activation**: Extend thumb and index finger wide apart (>55% distance) for 0.6 seconds
- **Volume Up**: Increase distance between thumb and index finger
- **Volume Down**: Decrease distance between thumb and index finger
- **Mute**: Bring fingers very close together (<15% distance)
- **Unmute**: Separate fingers (>20% distance)

## Technical Details

### Gesture Recognition
- Uses MediaPipe for hand tracking with 70% detection confidence
- Normalizes finger distance based on hand size for consistent control
- Exponential smoothing (α=0.2) with dead zone (2%) for stable operation

### Mode Switching
- Media mode is default and locked with fist/palm gestures
- Volume mode activates when thumb-index distance exceeds 55% threshold
- 0.6 second delay prevents accidental mode switching

### Volume Control
- Quadratic scaling for more natural volume response
- 50ms update interval for smooth adjustments
- Windows volume OSD triggers on significant changes

## Dependencies

- **opencv-python**: Camera capture and image processing
- **mediapipe**: Hand tracking and gesture recognition
- **numpy**: Numerical operations and interpolation
- **pyautogui**: System media control simulation
- **pycaw**: Windows Core Audio API interface
- **comtypes**: COM interface support for PyCaw

## Configuration Parameters

The application includes several tunable parameters:
- `alpha`: Smoothing factor (0.2)
- `DEAD_ZONE`: Minimum change threshold (0.02)
- `MUTE_ON/OFF`: Mute activation thresholds (0.15/0.20)
- `UPDATE_INTERVAL`: Volume update frequency (0.05s)
- `GESTURE_COOLDOWN`: Action repeat prevention (1.0s)
- `VOLUME_ACTIVATION_THRESHOLD`: Mode switch trigger (0.55)
- `MODE_SWITCH_DELAY`: Mode switch delay (0.6s)

## Troubleshooting

- **Camera not working**: Ensure no other applications are using the webcam
- **Permission issues**: Run the script as administrator
- **Volume control not working**: Verify Windows audio devices are functional
- **Poor tracking**: Improve lighting conditions and ensure hand is clearly visible
- **First run slow**: MediaPipe downloads models on initial startup

## Performance Tips

- Maintain consistent hand distance from camera for best tracking
- Use good, even lighting without strong shadows
- Keep hand gestures clear and deliberate
- Avoid rapid movements for better gesture recognition

## License

This project is open source and available under the MIT License.
