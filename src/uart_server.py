from gnss_module import GNSS
import serial

# Server Configuration
UART_PORT = "/dev/ttyAMA0"
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
                command = ser.readline().decode('utf-8', errors='ignore').strip()
                print(f"Received command: {command}")

                if command == "get_nmea":
                    nmea_data = gnss.read_nmea()
                    if "error" in nmea_data:
                        ser.write(f"Error: {nmea_data['error']}\n".encode('utf-8'))
                    else:
                        ser.write(f"NMEA: {nmea_data['nmea']}\n".encode('utf-8'))

                elif command == "get_position":
                    nmea_data = gnss.read_nmea()
                    if "error" in nmea_data:
                        ser.write(f"Error: {nmea_data['error']}\n".encode('utf-8'))
                    else:
                        position = gnss.parse_gngga(nmea_data["nmea"])
                        if "error" in position:
                            ser.write(f"Error: {position['error']}\n".encode('utf-8'))
                        else:
                            response = (f"Lat: {position['latitude']}°, "
                                        f"Lon: {position['longitude']}°, "
                                        f"Alt: {position['altitude']}m")
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
