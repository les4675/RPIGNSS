import serial
import csv
from datetime import datetime

def main():
    # Record the start time and create a filename from it.
    start_time = datetime.now()
    filename = start_time.strftime("uart_log_%Y-%m-%d_%H-%M-%S.csv")
    
    # Configure the serial port.
    ser = serial.Serial(
        port='/dev/ttyAMA0',  # Adjust this if your UART port is different
        baudrate=9600,      # Set the baud rate according to your device settings
        timeout=1             # Timeout in seconds; adjust as needed
    )

    # Open (or create) the CSV file in write mode.
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header row.
        csv_writer.writerow(['Timestamp', 'Message'])

        print(f"Logging to {filename}. Listening on UART... (Press Ctrl+C to exit)")
        while True:
            try:
                line = ser.readline().decode('utf-8', errors='replace').strip()
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                continue

            if line:  # Only process non-empty lines.
                timestamp = datetime.now().isoformat()
                csv_writer.writerow([timestamp, line])
                csvfile.flush()  # Ensure data is written immediately
                print(f"{timestamp}: {line}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
