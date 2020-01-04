import configparser, time, sys, os

pwd = str(sys.argv[1])
os.system("echo "+pwd+" | sudo -S apt update")
os.system("echo "+pwd+" | sudo -S apt install git -y")
os.system("echo "+pwd+" | sudo -S apt install python3-pip -y")
os.system("echo "+pwd+" | sudo -S apt install python3-tk -y")
os.system("echo "+pwd+" | sudo -S apt install ffmpeg -y")
os.system("echo "+pwd+" | sudo -S apt install vlc -y")
os.system("echo "+pwd+" | sudo -S apt install xtrlock -y")
os.system("echo "+pwd+" | sudo -S apt install xfce4 -y")

os.system("pip3 install pyserial")
os.system("pip3 install psutil")
os.system("pip3 install python-vlc")
os.system("pip3 install pillow")
os.system("pip3 install aiohttp")
os.system("pip3 install opencv-python")
os.system("pip3 install PySimpleGUI")

os.system("echo "+pwd+" | sudo -S dpkg -i /home/xirioxinf/Documentos/descarte_xiriox/config-os/libwxbase3.0-0v5_3.0.4+dfsg-3_amd64.deb")
os.system("echo "+pwd+" | sudo -S dpkg -i /home/xirioxinf/Documentos/descarte_xiriox/config-os/libwxgtk3.0-gtk3-0v5_3.0.4+dfsg-3_amd64.deb")
os.system("echo "+pwd+" | sudo -S dpkg -i /home/xirioxinf/Documentos/descarte_xiriox/config-os/veracrypt-console-1.24-Hotfix1-Ubuntu-18.04-amd64.deb")

