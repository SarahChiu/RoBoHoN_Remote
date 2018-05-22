# RoBoHoN\_Romote

RoBoHoN\_Remote is a project to control RoBoHoN's speech remotely through WiFi. It contains a server part written in python and the client part written as an Android Studio project, and the server can read input sentences or a file and send those sentences to RoBoHoN.

## Getting Started

### Prerequisites

1. RoBoHoN robot
2. python-grpc v1.10.0 (see [here](https://grpc.io/docs/quickstart/python.html) for the installation and more information)

### Run the Program

First clone the project and install the android app RemoteControl into RoBoHoN.

1. Manually Typing Mode
* Go to folder [server](server), and run `python server.py`.
* Execute the app RemoteControl on RoBoHoN, set the ip (default: 127.0.0.1), port (default: 50051) for the server and transmission duration (default: 1000 ms).
* Press the button CONNECT, and you can start typing any sentence and press enter, then RoBoHoN will speak what you just typed.

2. File Reading Mode
* Go to folder [server](server), and run `python server.py --mode read_file --file_name sentences.txt` for reading test file written in Chinese.
* Execute the app RemoteControl on RoBoHoN, set the ip (default: 127.0.0.1), port (default: 50051) for the server and transmission duration (default: 1000 ms).
* Press the button CONNECT, and RoBoHoN will start reading the sentences in the file.

3. URL Parsing Mode
* Go to folder [server](server), and run `python server.py --mode url --url http://technews.tw/2018/05/22/nvidia-new-ai-technique-helps-robots-work-alongside-humans/` for reading the article on the Internet.
* Execute the app RemoteControl on RoBoHoN, set the ip (default: 127.0.0.1), port (default: 50051) for the server and transmission duration (default: 1000 ms).
* Press the button CONNECT, and RoBoHoN will start reading the sentences of the article.

4. To disconnect, simply press the button DISCONNECT on RoBoHoN and shut down the server if you are not going to connect anymore.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

