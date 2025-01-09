import serial

UART_PORT = "/dev/ttyAMA0"  # Use ttyAMA0 for Raspberry Pi UART
BAUD_RATE = 9600  # GNSS configured baud rate

def read_gnss_data(ser):
    """
    Reads GNSS data from the serial port.
    """
    if ser.in_waiting > 0:  # Check if there's data to read
        raw_data = ser.readline()  # Read a single line
        return raw_data
    return None

def main():
    # Initialize UART
    ser = serial.Serial(UART_PORT, baudrate=BAUD_RATE, timeout=1)
    print("UART server initialized. Listening for commands...")

    try:
        while True:
            if ser.in_waiting > 0:  # Check if there's incoming data
                raw_data = ser.readline()  # Read input command
                try:
                    command = raw_data.decode('utf-8', errors='ignore').strip()
                    print(f"Received command: {command}")
                except UnicodeDecodeError as e:
                    print(f"Error decoding command: {e}")
                    continue
                
                # Process the command
                if command == "get_nmea":
                    print("Fetching GNSS data...")
                    gnss_data = read_gnss_data(ser)
                    if gnss_data:
                        try:
                            gnss_sentence = gnss_data.decode('ascii', errors='ignore').strip()
                            print(f"GNSS Data: {gnss_sentence}")
                        except Exception as e:
                            print(f"Error decoding GNSS data: {e}")
                    else:
                        print("No GNSS data available.")
                    ser.write(b"GNSS data fetched.\n")
                else:
                    print("Unknown command received.")
                    ser.write(b"Unknown command.\n")

    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
