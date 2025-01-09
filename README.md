uart_server_project/
├── src/
│   ├── uart_server.py       # The main server program
│   ├── gnss_module.py       # New GNSS module with GNSS interaction functions
├── requirements.txt         # Include pyserial and any other dependencies
├── README.md                   # Documentation for the project
└── .gitignore                  # Git ignore file for unnecessary files (e.g., .pyc, __pycache__)


Use the following line to install all dependancies onto your Raspberry Pi 
pip install -r requirements.txt

Receiver: https://www.digikey.com/en/products/detail/sparkfun-electronics/GPS-18037/16719314

Antenna: https://www.digikey.com/en/products/detail/sparkfun-electronics/GPS-14986/9682235

1. Set Up the Raspberry Pi

    Install Raspberry Pi OS:
        Use the Raspberry Pi Imager tool to flash Raspberry Pi OS (Lite or Desktop) onto a microSD card.
        Configure SSH and Wi-Fi during the flashing process if needed.

    Enable UART:

        Open the Raspberry Pi configuration tool:

sudo raspi-config

Navigate to Interface Options > Serial Port.

    Disable login shell over serial.
    Enable hardware serial.

Add enable_uart=1 to /boot/config.txt if not already present:

sudo nano /boot/firmware/config.txt

Add this line at the end:

enable_uart=1

Save and reboot:

    sudo reboot

Verify UART Ports: Check the available serial ports:

ls /dev/serial*

    /dev/serial0 is usually the default hardware UART.
