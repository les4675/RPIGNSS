import serial
import time

# Configuration for GNSS input UART (e.g., Galileo-capable receiver)
GNSS_UART_PORT = "/dev/ttyAMA0"
GNSS_BAUD_RATE = 9600

# Configuration for second UART output
OUTPUT_UART_PORT = "/dev/ttyS0"  # Change as needed
OUTPUT_BAUD_RATE = 9600

class GNSS:
    def __init__(self, port: str, baud: int):
        self.uart_port = port
        self.baud = baud
        self.ser = None

    def initialize(self) -> bool:
        """Initialize GNSS module for NMEA communication."""
        try:
            self.ser = serial.Serial(self.uart_port, baudrate=self.baud, timeout=1)
            time.sleep(2)  # Allow time for GNSS to stabilize
            print(f"Connected to GNSS on {self.uart_port} at {self.baud} baud.")
            return True
        except serial.SerialException as e:
            print(f"Failed to open GNSS serial port: {e}")
            return False

    def read_nmea(self) -> dict:
        """Read an NMEA sentence from the GNSS module."""
        if not self.ser or not self.ser.is_open:
            return {"error": "GNSS serial not initialized"}
        try:
            raw = self.ser.readline().decode('ascii', errors='ignore').strip()
            if raw.startswith("$"):
                return {"nmea": raw}
            else:
                return {"error": "No valid NMEA sentence"}
        except Exception as e:
            return {"error": str(e)}

    def parse_gngga(self, nmea: str) -> dict:
        """Parse GNGGA sentence for time, lat, lon, and alt."""
        if not nmea.startswith("$GNGGA"):
            return {"error": "Not GNGGA"}
        fields = nmea.split(',')
        if len(fields) < 15:
            return {"error": "Incomplete GNGGA"}
        try:
            time_utc = self._parse_time(fields[1])
            lat = self._parse_latitude(fields[2], fields[3])
            lon = self._parse_longitude(fields[4], fields[5])
            alt = float(fields[9]) if fields[9] else 0.0
            return {"time_utc": time_utc, "latitude": lat, "longitude": lon, "altitude": alt}
        except Exception as e:
            return {"error": f"Parse error: {e}"}

    def _parse_time(self, value: str) -> str:
        if not value:
            return ""
        try:
            hour = int(value[0:2])
            minute = int(value[2:4])
            second = float(value[4:])
            return f"{hour:02}:{minute:02}:{second:06.3f} UTC"
        except:
            return "Invalid UTC time"

    def _parse_latitude(self, value: str, hemi: str) -> float:
        if not value or not hemi:
            return 0.0
        degrees = int(value[:2])
        minutes = float(value[2:])
        decimal = degrees + minutes / 60.0
        return decimal if hemi == 'N' else -decimal

    def _parse_longitude(self, value: str, hemi: str) -> float:
        if not value or not hemi:
            return 0.0
        degrees = int(value[:3])
        minutes = float(value[3:])
        decimal = degrees + minutes / 60.0
        return decimal if hemi == 'E' else -decimal

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()


def forward_to_uart2(data: dict, out_ser: serial.Serial) -> None:
    """Format, send parsed data over the second UART, and print to console."""
    try:
        msg = f"TIME:{data['time_utc']}, LAT:{data['latitude']:.6f}, LON:{data['longitude']:.6f}, ALT:{data['altitude']:.2f}\r\n"
        out_ser.write(msg.encode('utf-8'))
        print(f"Galileo Data: {msg.strip()}")
    except Exception as e:
        print(f"UART2 send error: {e}")


def main():
    # Initialize GNSS serial
    gnss = GNSS(GNSS_UART_PORT, GNSS_BAUD_RATE)
    if not gnss.initialize():
        return

    # Initialize output serial
    try:
        out_ser = serial.Serial(OUTPUT_UART_PORT, baudrate=OUTPUT_BAUD_RATE, timeout=1)
        print(f"Output UART ready on {OUTPUT_UART_PORT} at {OUTPUT_BAUD_RATE} baud.")
    except serial.SerialException as e:
        print(f"Failed to open output UART: {e}")
        gnss.close()
        return

    try:
        print("Starting GNSS data forwarding loop. Press Ctrl+C to exit.")
        while True:
            res = gnss.read_nmea()
            if 'nmea' in res:
                sentence = res['nmea']
                parsed = gnss.parse_gngga(sentence)
                if 'latitude' in parsed and 'time_utc' in parsed:
                    forward_to_uart2(parsed, out_ser)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        gnss.close()
        out_ser.close()


if __name__ == "__main__":
    main()
