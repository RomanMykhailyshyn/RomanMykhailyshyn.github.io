import os
import sys
import time
import serial  # For communication with Arduino
from dynamixel_sdk import *  # Uses Dynamixel SDK

# Control table addresses for MX series
ADDR_TORQUE_ENABLE = 24
ADDR_GOAL_POSITION = 30
ADDR_PRESENT_POSITION = 36
ADDR_MOVING_SPEED = 32

# Data byte length
LEN_GOAL_POSITION = 2
LEN_PRESENT_POSITION = 2
LEN_MOVING_SPEED = 2

# Protocol version for MX series
PROTOCOL_VERSION = 1.0

# Default setting
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB1'  # Adjust according to your system (e.g., COM3 for Windows)
ARDUINO_PORT = '/dev/ttyACM0'  # Port for Arduino communication
ARDUINO_BAUDRATE = 9600

DXL_IDs = [2, 3, 4, 5, 6, 7, 8]  # List of Dynamixel IDs
TORQUE_ENABLE = 1  # Enable torque
TORQUE_DISABLE = 0  # Disable torque

# Establish communication with Arduino
try:
    arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE, timeout=1)
    time.sleep(2)  # Allow time for Arduino to initialize
    print("Connected to Arduino on", ARDUINO_PORT)
except Exception as e:
    print("Failed to connect to Arduino:", e)
    arduino = None

# Predefined positions and speeds for each key press
positions_speeds_dict = {
    'a': {2: (2052, 80), 3: (3630, 60), 4: (2052, 80), 5: (3630, 60), 6: (2052, 80), 7: (3630, 60), 8: (60, 80)},
    's': {2: (2052, 80), 3: (3630, 60), 4: (2052, 80), 5: (1330, 60), 6: (2052, 80), 7: (1330, 60), 8: (60, 80)},
    'd': {2: (2052, 80), 3: (3630, 60), 4: (2002, 80), 5: (1330, 60), 6: (2102, 80), 7: (1330, 60), 8: (60, 80)},
    'f': {2: (2052, 80), 3: (3630, 60), 4: (2102, 80), 5: (1330, 60), 6: (2002, 80), 7: (1330, 60), 8: (60, 80)},
    'z': {2: (2052, 80), 3: (3630, 60), 4: (2052, 80), 5: (3630, 60), 6: (2052, 80), 7: (3630, 60), 8: (1712, 80)},
    'x': {2: (2052, 80), 3: (1330, 85), 4: (2052, 80), 5: (1330, 87), 6: (2052, 80), 7: (1330, 90), 8: (1712, 80)},
    'c': {2: (2052, 80), 3: (3630, 60), 4: (2052, 80), 5: (3630, 60), 6: (2052, 80), 7: (3630, 60), 8: (3500, 80)},
    'b': {2: (2052, 80), 3: (3630, 60), 4: (2320, 80), 5: (3630, 60), 6: (1784, 80), 7: (3630, 60), 8: (3500, 80)},
    'n': {2: (2052, 80), 3: (1130, 60), 4: (2320, 80), 5: (1130, 60), 6: (1784, 80), 7: (1130, 60), 8: (3500, 80)},
    'm': {2: (2052, 80), 3: (1130, 60), 4: (2320, 80), 5: (1130, 60), 6: (1784, 80), 7: (3630, 60), 8: (3500, 80)}
}


# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if not portHandler.openPort():
    print("Failed to open the port")
    sys.exit()
print("Succeeded to open the port")

# Set port baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to set the baudrate")
    sys.exit()
print("Succeeded to set the baudrate")

# Enable torque for all servos
for dxl_id in DXL_IDs:
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    print(f"Dynamixel {dxl_id} has been successfully connected")

# Function to move motors to a given predefined position and speed
def move_motors(positions_speeds):
    for dxl_id, (position, speed) in positions_speeds.items():
        packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_MOVING_SPEED, speed)
        packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_GOAL_POSITION, position)
        print(f"Dynamixel {dxl_id} moved to {position} at speed {speed}")

# Function to control relay via Arduino
def control_relay(state):
    if arduino:
        arduino.write(state.encode())
        print(f"Relay {'ON' if state == '1' else 'OFF'} sent to Arduino")
    else:
        print("Arduino connection not established.")

print("Press 'a', 'b', or 'c' and then Enter to move motors to predefined positions, 'q' to turn relay ON, 'w' to turn relay OFF, 'e' to exit.")

while True:
    key = input("Enter command: ").strip().lower()
    if key in positions_speeds_dict:
        move_motors(positions_speeds_dict[key])
    elif key == 'q':
        control_relay('1')  # Turn relay ON
    elif key == 'w':
        control_relay('0')  # Turn relay OFF
    elif key == 'e':
        print("Exiting program...")
        break

# Disable torque after motion
for dxl_id in DXL_IDs:
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    print(f"Torque disabled for Dynamixel {dxl_id}")

# Close port
portHandler.closePort()
if arduino:
    arduino.close()
