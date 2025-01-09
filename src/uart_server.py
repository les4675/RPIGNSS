import serial

UART_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

def parse_nmea_sentence(sentence):
    """
    Parses various NMEA sentences and extracts relevant information.
    """
    if sentence.startswith("$GNGGA"):
        fields = sentence.split(',')
        return f"GGA Sentence - UTC: {fields[1]}, Latitude: {fields[2]} {fields[3]}, Longitude: {fields[4]} {fields[5]}, Altitude: {fields[9]} {fields[10]}"
    elif sentence.startswith("$GNGSA"):
        fields = sentence.split(',')
        return f"GSA Sentence - Mode: {fields[1]}, Fix Type: {fields[2]}, PDOP: {fields[15]}, HDOP: {fields[16]}, VDOP: {fields[17]}"
    elif sentence.startswith("$GNGLL"):
        fields = sentence.split(',')
        return f"GLL Sentence - Latitude: {fields[1]} {fields[2]}, Longitude: {fields[3]} {fields[4]}, UTC: {fields[5]}, Status: {fields[6]}"
    elif sentence.startswith("$GNRMC"):
        fields = sentence.split(',')
        return f"RMC Sentence - UTC: {fields[1]}, Status: {fields[2]}, Latitude: {fields[3]} {fields[4]}, Longitude: {fields[5]} {fields[6]}, Speed: {fields[7]} knots"
    elif sentence.startswith("$GNVTG"):
        fields = sentence.split(',')
        return f"VTG Sentence - Course: {fields[1]}° True, Speed: {fields[5]} knots, {fields[7]} km/h"
    else:
        return f"Unrecognized NMEA Sentence: {sentence}"

def read_gnss_data(ser):
    """
    Reads GNSS data from the serial port.
    """
    if ser.in_waiting > 0:
        raw_data = ser.readline()
        return raw_data.decode('ascii', errors='ignore').strip()
    return None

def main():
    ser = serial.Serial(UART_PORT, baudrate=BAUD_RATE, timeout=1)
    print("UART server initialized. Listening for commands...")

    command_mode = True

    try:
        while True:
            if ser.in_waiting > 0:
                raw_data = ser.readline()
                try:
                    data = raw_data.decode('utf-8', errors='ignore').strip()
                    print(f"Received data: {data}")
                except UnicodeDecodeError as e:
                    print(f"Error decoding data: {e}")
                    continue

                if command_mode:
                    # Process the received command
                    if data == "get_nmea":
                        print("Command received: Fetching GNSS data...")
                        nmea_data = read_gnss_data(ser)
                        if nmea_data:
                            print(f"Raw NMEA Data: {nmea_data}")
                            processed_data = parse_nmea_sentence(nmea_data)
                            print(processed_data)
                        else:
                            print("No GNSS data available.")
                        command_mode = False  # Exit command mode
                    else:
                        print("Unknown command received.")
                        command_mode = False  # Exit command mode
                else:
                    # Handle GNSS data
                    if data.startswith("$"):
                        processed_data = parse_nmea_sentence(data)
                        print(processed_data)
                    elif data == "enter_command_mode":
                        print("Entering command mode...")
                        command_mode = True
                    else:
                        print(f"Unknown data format: {data}")

    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
