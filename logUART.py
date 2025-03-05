import serial
import csv
from datetime import datetime

def main():
    # Configure the serial port.
    # On many Raspberry Pi models, /dev/serial0 is a symlink to the primary UART.
    ser = serial.Serial(
        port='/dev/ttyAMA0',  # Change this if your UART port is different (e.g., /dev/ttyS0 or /dev/ttyAMA0)
        baudrate=115200,      # Set the baud rate according to your device settings
        timeout=1             # Timeout in seconds for reading; adjust as needed
    )

    # Open (or create) a CSV file in append mode.
    # The CSV file will store two columns: a timestamp and the received message.
    with open('uart_log.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header if the file is empty.
        csvfile.seek(0)
        if csvfile.tell() == 0:
            csv_writer.writerow(['Timestamp', 'Message'])

        print("Listening on UART... (Press Ctrl+C to exit)")
        while True:
            # Read a line from the UART port.
            # readline() returns a bytes object, so we decode it to a string.
            try:
                line = ser.readline().decode('utf-8', errors='replace').strip()
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                continue

            if line:  # Only process non-empty lines.
                # Get the current timestamp in ISO format.
                timestamp = datetime.now().isoformat()
                # Write the timestamp and message as a new row in the CSV file.
                csv_writer.writerow([timestamp, line])
                # Flush the CSV file to make sure data is written immediately.
                csvfile.flush()
                # Optionally, print the message to the console.
                print(f"{timestamp}: {line}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
