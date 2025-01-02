File structure of the repo
uart_server_project/
│
├── src/
│   ├── __init__.py             # Marks this directory as a Python package
│   ├── uart_server.py          # Main script to run the server
│   ├── uart_handler.py         # Module for UART communication logic
│   ├── config.py               # Configuration settings (e.g., UART port, baud rate)
│   └── utils/
│       ├── __init__.py         # Marks this directory as a Python package
│       └── logger.py           # Utility functions for logging
│
├── tests/
│   ├── __init__.py             # Marks this directory as a Python package
│   ├── test_uart_handler.py    # Unit tests for UART handler
│   └── test_logger.py          # Unit tests for logging utilities
│
├── requirements.txt            # List of Python dependencies
├── README.md                   # Documentation for the project
└── .gitignore                  # Git ignore file for unnecessary files (e.g., .pyc, __pycache__)


Use the following line to install all dependancies onto your Raspberry Pi 
pip install -r requirements.txt

Receiver: https://www.digikey.com/en/products/detail/sparkfun-electronics/GPS-18037/16719314

Antenna: https://www.digikey.com/en/products/detail/sparkfun-electronics/GPS-14986/9682235
