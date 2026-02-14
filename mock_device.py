import sys
import time
import signal

# This script simulates a device process. It will print messages to the console to indicate that it is running.
def handle_stop_signal(signum, frame):
    print(f"[{device_name}] Received STOP signal. Shutting down.")
    time.sleep(0.5) # Simulate stopping motor safely
    print(f"[{device_name}] Motor stopped safely.")
    sys.exit(0)

# Register signals so we can catch them
signal.signal(signal.SIGINT, handle_stop_signal)
signal.signal(signal.SIGTERM, handle_stop_signal)

# The supervisor launches us with a name
device_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown_Device"

print(f"[Device] {device_name} is starting up...")
sys.stdout.flush() # Force text to the Supervisor immediately

# Simulate device activity
cycle = 0
while True:
    print(f"[{device_name}] Running cycle {cycle}...")
    sys.stdout.flush() # Ensure output is sent to Supervisor
    cycle += 1
    time.sleep(1) # Simulate work being done
