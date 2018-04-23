# RoBoHoN\_Romote

RoBoHoN\_Remote is a project to control RoBoHoN's speech remotely through WiFi. It contains a server part written in python and the client part written as an Android Studio project, and the server can read input sentences or a file and send those sentences to RoBoHoN.

## Getting Started

1. Clone the project and install the android app RemoteContol into RoBoHoN.
2. Go to server folder, run `python server.py` for the manually typing mode or `python server.py --mode read_file --file_name sentences.txt` for file reading mode.
3. Execute the app RemoteControl on RoBoHoN, set the ip (default: 127.0.0.1), port (default: 50051) and transmission duration (default: 5000 ms) for the server.
4. Press the button CONNECT, and the server part will output "Got a request type: sentence", which means the connection is built successfully.
5. If running manually typing mode, type any sentence and press enter, and then RoBoHoN will speak what you just typed.
6. To disconnect, first press several enter until server part do not appear "Got a request type: sentence" anymore, and then press the button DISCONNECT on RoBoHoN. 
   (This part will be fixed later to avoid this inconvenient disconnecting method.)

### Prerequisites

1. RoBoHoN robot
2. python-grpc v1.10.0 (see [here](https://grpc.io/docs/quickstart/python.html) for the installation and more information)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

