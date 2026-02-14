from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Log, Static
from textual.containers import Container
from devices import Motor
import threading

class RobotControlCenter(App):
    # This is the main application class for the Robot Control Center. It manages the UI and device interactions.

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-gutter: 1;
        padding: 1;
    }

    #controls {
        column-span: 1;
        height: 100%;
        border: solid blue;
    }

    #log_window {
        column-span: 1;
        height: 100%;
        border: solid green;
        background: $surface;
    }

    Button {
        width: 100%;
        margin-bottom: 1;
    }
    """

    def __init__(self):
        super().__init__()
        #Initialize hardware connection
        self.arm_motor = Motor("Elbow_Joint", 101) # Create an instance of the Motor device

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True) # Add a header to the UI

        #Left side controls
        with Container(id="controls"):
            yield Static("--- COMMANDS ---", id="label")
            yield Button("Start Motor", id="start", variant="success")
            yield Button("E-Stop", id="stop", variant="error")
            yield Button("Speed: LOW", id="speed_low", variant="primary")
            yield Button("Speed: HIGH", id="speed_high", variant="warning")

        #Right side log window
        yield Log(id="log_window") # Add a log widget to display messages
        yield Footer() # Add a footer to the UI

    def monitor_motor_output(self):
        # This function runs in a separate thread to monitor the output of the motor device and log it in the UI.
        log = self.query_one("#log_window", Log) # Get the log widget to display
        proc = self.arm_motor.process # Get the subprocess handle for the motor device

        while proc and proc.poll() is None: # While the process is still running
            line = proc.stdout.readline() # Read a line of output from the motor device

            if line:
                self.call_from_thread(log.write_line, line.strip()) # Log the output in the UI

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Event handler for button presses. It checks which button was pressed and performs the corresponding action.
        log = self.query_one("#log_window", Log) # Get the log widget to display messages
        button_id = event.button.id

        if button_id == "start":
            log.write_line(f"[System] Initializing {self.arm_motor.name}...")
            self.arm_motor.start() # Start the motor device
            threading.Thread(target=self.monitor_motor_output, daemon=True).start() # Start a thread to monitor the motor output
            log.write_line(f"[System] {self.arm_motor.name} started.")

        elif button_id == "stop":
            log.write_line(f"[System] Stopping {self.arm_motor.name}...")
            self.arm_motor.stop() # Stop the motor device
            log.write_line(f"[System] {self.arm_motor.name} stopped.")

        elif button_id == "speed_low":
            log.write_line(f"[System] Setting {self.arm_motor.name} speed to LOW...")
            self.arm_motor.set_speed(50) # Set motor speed to low
            log.write_line(f"[System] {self.arm_motor.name} speed set to LOW.")

        elif button_id == "speed_high":
            log.write_line(f"[System] Setting {self.arm_motor.name} speed to HIGH...")
            self.arm_motor.set_speed(150) # Set motor speed to high
            log.write_line(f"[System] {self.arm_motor.name} speed set to HIGH.")

if __name__ == "__main__":
    app = RobotControlCenter() # Create an instance of the RobotControlCenter app
    app.run() # Run the application