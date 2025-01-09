import serial

class UARTHandler:
    def __init__(self, port, baud_rate, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_conn = None

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print(f"Connected to {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Error connecting to UART: {e}")

    def send(self, data):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write(f"{data}\n".encode('utf-8'))

    def receive(self):
        if self.serial_conn and self.serial_conn.in_waiting > 0:
            return self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8').strip()

    def close(self):
        if self.serial_conn:
            self.serial_conn.close()
