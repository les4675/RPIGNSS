import serial
import time

# Configuration
UART_PORT = "/dev/serial0"  # Update this to the correct UART port
BAUD_RATES = [38400, 9600]  # GNSS may operate at different baud rates

class GNSS:
    def __init__(self):
        self.ser = None

    def initialize(self):
        """Initialize the GNSS module by finding the correct baud rate."""
        for baud in BAUD_RATES:
            try:
                print(f"Trying {baud} baud...")
                self.ser = serial.Serial(UART_PORT, baudrate=baud, timeout=1)
                time.sleep(2)  # Allow time for initialization
                # Send a test UBX command (optional, customize as needed)
                self.ser.write(b"\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                response = self.ser.read(10)
                if response:
                    print(f"Connected at {baud} baud.")
                    if baud == 9600:
                        print("Switching GNSS to 38400 baud...")
                        self.ser.write(b"\xB5\x62\x06\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                        time.sleep(1)
                    return True
            except serial.SerialException as e:
                print(f"Failed at {baud} baud: {e}")
        raise Exception("Failed to connect to GNSS module.")

    def get_location(self):
        """Query GNSS module for position data."""
        try:
            self.ser.write(b"\xB5\x62\x01\x02\x00\x00\x03\x0A")  # UBX request command
            time.sleep(0.1)
            data = self.ser.read(36)  # Example payload size for UBX response
            if len(data) < 36:
                return {"error": "Incomplete data received"}

            # Parse data (latitude, longitude, altitude, and SIV)
            lat = int.from_bytes(data[10:14], byteorder="little", signed=True) / 10**7
            lon = int.from_bytes(data[14:18], byteorder="little", signed=True) / 10**7
            alt = int.from_bytes(data[22:26], byteorder="little", signed=True) / 1000
            siv = data[23]
            return {"latitude": lat, "longitude": lon, "altitude": alt, "siv": siv}
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        if self.ser:
            self.ser.close()
