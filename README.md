# Supervisor Spoof

A multi-process device management simulation built with Python. This project demonstrates a **Supervisor/Driver architecture** where a central Terminal User Interface (TUI) manages independent child processes representing hardware devices.

<img width="780" height="431" alt="image" src="https://github.com/user-attachments/assets/471128b6-44e2-411b-8a3f-a76dcc0eec73" />

## Key Features

* **Asynchronous UI:** Built with [Textual](https://textual.textualize.io/), providing a responsive TUI that does not freeze during background operations.
* **Multiprocessing:** Uses `subprocess.Popen` to spawn completely independent worker processes (simulating hardware drivers).
* **Non-Blocking I/O:** Implements a dedicated background thread to read `stdout` from child processes in real-time.
* **Graceful Shutdowns:** Child processes are designed to handle `SIGTERM` signals for safe termination.

## Architecture

* **`app.py` (The Supervisor):** The main entry point. It renders the UI, handles user input events, and spawns background threads to monitor device logs.
* **`devices.py` (The Driver Layer):** A wrapper class that abstracts the `subprocess` logic. It handles the startup (`Popen`) and teardown (`terminate`) of the worker scripts.
* **`mock_device.py` (The Worker):** A standalone script that simulates hardware. It runs in an infinite loop, printing status updates to `stdout` and listening for kill signals.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/andrewtrin/supervisor-spoof.git](https://github.com/andrewtrin/supervisor-spoof.git)
    cd supervisor-spoof
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Windows (PowerShell)
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    ```bash
    pip install textual
    ```

## Usage

Run the main application from the virtual environment:

```bash
python app.py
