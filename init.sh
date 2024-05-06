screen -dmS "mediamtx" /home/magicam/MagiCam-Server/mediamtx/mediamtx /home/magicam/MagiCam-Server/mediamtx/mediamtx.yml
screen -dmS "ffmpeg" /home/magicam/MagiCam-Server/ffmpeg.sh
screen -dmS "control" python3 /home/magicam/MagiCam-Server/control/control.py
