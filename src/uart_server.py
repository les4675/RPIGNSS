from gnss_module import GNSS
import serial

# Server Configuration
UART_PORT = "/dev/serial0"  # Replace with the appropriate port
BAUD_RATE = 38400

def main():
    # Initialize UART server
    ser = serial.Serial(UART_PORT, baudrate=BAUD_RATE, timeout=1)
    print("UART server initialized. Listening for commands...")
    
    # Initialize GNSS
    gnss = GNSS()
    if not gnss.initialize():
        print("Failed to initialize GNSS.")
        return

    try:
        while True:
            if ser.in_waiting > 0:
                # Read command from UART
                command = ser.readline().decode('utf-8').strip()
                print(f"Received command: {command}")

                if command == "get_location":
                    location = gnss.get_location()
                    if "error" in location:
                        response = f"Error: {location['error']}"
                    else:
                        response = (f"Lat: {location['latitude']}°, "
                                    f"Lon: {location['longitude']}°, "
                                    f"Alt: {location['altitude']}m, "
                                    f"SIV: {location['siv']}")
                    ser.write((response + "\n").encode('utf-8'))
                else:
                    ser.write(b"Unknown command\n")
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        gnss.close()
        ser.close()

if __name__ == "__main__":
    main()
