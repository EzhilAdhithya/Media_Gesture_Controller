# Gesture-Based Volume and Media Control

A Python application that allows you to control your system's volume and media playback using hand gestures captured through your webcam.

## Features

- **Volume Control**: Adjust system volume by changing the distance between your thumb and index finger
- **Mute/Unmute**: Touch your thumb and index finger to mute/unmute the system audio
- **Play/Pause Media**: Make a fist to play/pause media playback
- **Visual Feedback**: Real-time display of hand tracking and control status
- **Smooth Controls**: Built-in smoothing algorithm for stable volume adjustments

## Prerequisites

- Python 3.7 or higher
- Webcam
- Windows OS (for volume control functionality)
- Internet connection (for downloading models)

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python gesture_volume_control.py
   ```

2. Position your hand in front of the camera:
   - **Volume Control**: Show your hand with thumb and index finger extended
   - **Mute/Unmute**: Touch your thumb and index finger together
   - **Play/Pause**: Make a fist

3. Press 'q' to exit the application

## Controls

- Move your thumb and index finger apart to increase volume
- Bring them closer to decrease volume
- Touch them together to mute/unmute
- Make a fist to play/pause media

## Dependencies

- OpenCV: For camera capture and image processing
- MediaPipe: For hand tracking and gesture recognition
- NumPy: For numerical operations
- PyAutoGUI: For system media controls
- PyCaw: For Windows volume control
- Comtypes: Required for PyCaw to interface with Windows Core Audio

## Troubleshooting

- If the camera doesn't start, ensure no other application is using it
- For permission issues, run the script as administrator
- If volume control doesn't work, ensure you're on Windows and have working audio devices
- Make sure you're in a well-lit environment for better hand tracking

## Notes

- The application works best with good lighting conditions
- Keep your hand within the camera frame for optimal tracking
- The first run might take longer as it downloads the hand tracking model

## License

This project is open source and available under the MIT License.
