import subprocess
import sys
import time

# Parent class for all devices
class RobotDevice:
    # Generic definition of a device
    def __init__(self, name, device_id):
        self.name = name
        self.device_id = device_id
        self.process = None # Holds the subprocess handle

    def start(self):
        # Launches the background process for the device
        print(f"[self.name] System Request: START")

        # Using Popen to start the process in the background
        # Assuming 'mock_device.py' is the script that simulates the device
        self.process = subprocess.Popen(
            [sys.executable, "mock_device.py", self.name],
            stdout=subprocess.PIPE, # Capture the output pipe
            stderr=subprocess.PIPE, # Capture the error pipe
            text=True               # Ensure the output is in text format
            )
        
    def stop(self):
        # Terminates the background process for the device
        if self.process:
            print(f"[self.name] System Request: STOP")
            self.process.terminate() # Terminate the process
            self.process = None      # Clear the process handle
        else:
            print(f"[self.name] No active process to stop.")


# Child class for a specific type of device, e.g., a motor
class Motor(RobotDevice):
    # A specific type of device that can move. Inherits from RobotDevice
    def set_speed(self, speed):
        print(f"[self.name] Setting target speed to {speed} RPM.")


# Test the implementation
if __name__ == "__main__":

    print("Testing device management...")

    # Create an instance of the Motor class
    arm_motor = Motor("Elbow_Joint", 101)

    # Use the start method to launch the background process
    arm_motor.start()

    # Use methods specific to the Motor class
    arm_motor.set_speed(150)

    time.sleep(5) # Let the process run for a while

    arm_motor.stop() # Stop the background process
    print("Device management test completed.")