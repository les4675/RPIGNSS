import serial
import threading

# Initialize UART
UART_PORT = '/dev/ttyAMA0'  # Update if using a USB-to-serial adapter (e.g., '/dev/ttyUSB0')
BAUD_RATE = 9600  # Match the baud rate of the connected device

# Function to handle receiving data
def receive_data(serial_conn):
    while True:
        if serial_conn.in_waiting > 0:
            data = serial_conn.read(serial_conn.in_waiting).decode('utf-8').strip()
            print(f"Received: {data}")
            # Optionally process the data here

# Function to send data
def send_data(serial_conn):
    while True:
        message = input("Enter message to send: ")
        if message.lower() == 'exit':  # Exit condition
            print("Exiting program...")
            serial_conn.close()
            break
        serial_conn.write(f"{message}\n".encode('utf-8'))
        print("Message sent.")

# Main function
def main():
    try:
        # Open the serial connection
        with serial.Serial(UART_PORT, BAUD_RATE, timeout=1) as serial_conn:
            print(f"Connected to {UART_PORT} at {BAUD_RATE} baud.")
            
            # Start threads for receiving and sending
            receiver_thread = threading.Thread(target=receive_data, args=(serial_conn,))
            sender_thread = threading.Thread(target=send_data, args=(serial_conn,))
            
            receiver_thread.daemon = True
            sender_thread.daemon = True
            
            receiver_thread.start()
            sender_thread.start()
            
            # Keep the main thread alive
            receiver_thread.join()
            sender_thread.join()

    except serial.SerialException as e:
        print(f"Serial exception: {e}")
    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")

if __name__ == "__main__":
    main()
