import serial
import time

# Configuration
UART_PORT = "/dev/ttyAMA0"  # Update to your UART port
BAUD_RATE = 38400  # Ensure this matches the GNSS configuration

class GNSS:
    def __init__(self):
        self.ser = None

    def initialize(self):
        """Initialize GNSS module for NMEA communication."""
        try:
            self.ser = serial.Serial(UART_PORT, baudrate=BAUD_RATE, timeout=1)
            time.sleep(2)  # Allow time for GNSS to stabilize
            print(f"Connected to GNSS module at {BAUD_RATE} baud.")
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to GNSS module: {e}")
            return False

    def read_nmea(self):
        """Read NMEA sentence from GNSS module."""
        if not self.ser:
            return {"error": "Serial connection not initialized"}
        try:
            line = self.ser.readline().decode('ascii', errors='ignore').strip()
            if line.startswith("$"):
                return {"nmea": line}
            return {"error": "Invalid NMEA sentence"}
        except Exception as e:
            return {"error": str(e)}

    def parse_gngga(self, nmea_sentence):
        """Parse a GNGGA NMEA sentence for latitude, longitude, and altitude."""
        if not nmea_sentence.startswith("$GNGGA"):
            return {"error": "Not a GNGGA sentence"}
        
        fields = nmea_sentence.split(",")
        if len(fields) < 15:
            return {"error": "Incomplete GNGGA sentence"}
        
        try:
            # Parse latitude and longitude
            lat = self._parse_latitude(fields[2], fields[3])
            lon = self._parse_longitude(fields[4], fields[5])
            alt = float(fields[9]) if fields[9] else 0.0  # Altitude in meters
            return {"latitude": lat, "longitude": lon, "altitude": alt}
        except Exception as e:
            return {"error": f"Parsing error: {e}"}

    def _parse_latitude(self, value, hemisphere):
        """Convert latitude from NMEA format to decimal degrees."""
        if not value or not hemisphere:
            return None
        degrees = int(value[:2])
        minutes = float(value[2:])
        decimal = degrees + (minutes / 60.0)
        return decimal if hemisphere == "N" else -decimal

    def _parse_longitude(self, value, hemisphere):
        """Convert longitude from NMEA format to decimal degrees."""
        if not value or not hemisphere:
            return None
        degrees = int(value[:3])
        minutes = float(value[3:])
        decimal = degrees + (minutes / 60.0)
        return decimal if hemisphere == "E" else -decimal

    def close(self):
        if self.ser:
            self.ser.close()
