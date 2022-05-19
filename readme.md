### Initial Setup
- `git clone`
- `cd magic-mirror-power-button`
- `python3 -m venv myvenv`
- `source myvenv/bin/activate`
- `pip3 install -r requirements.txt`
- `sudo apt-get install libasound-dev portaudio19-dev python3-pyaudio flac -y`
- `pip install pyaudio --user` - Might Fail that is fine

 # 
 ### Running the script manually
 - `source myvenv/bin/activate` (Only needs done when you open a new terminal)
 - `python3 main.py`
 
 
 #
 ### Running the script as a service
 `sudo nano /lib/systemd/system/magic-mirror-power-button.service`

Paste the contents below but change the username in ALL THREE PLACES
```
[Unit]
Description=Magic Mirror Power Button
After=multi-user.target
#Conflicts=getty@tty1.service

[Service]
Type=simple
WorkingDirectory=/home/brendan/magic-mirror-power-button
ExecStart=/home/brendan/magic-mirror-power-button/myvenv/bin/python3 /home/brendan/magic-mirror-power-button/main.py

#StandardInput=tty-force
StandardOutput=syslog
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

##### Enable the service (Creates symbolic link like apache does on enable site)
`sudo systemctl enable magic-mirror-power-button.service`

##### Start the service
`sudo systemctl start magic-mirror-power-button.service` 


#
### Other Helpful Commands (Optional)
##### Start, Stop, Restart, Kill, ...etc
- `sudo systemctl stop magic-mirror-power-button.service`          #To stop running service 
- `sudo systemctl start magic-mirror-power-button.service`         #To start running service 
- `sudo systemctl restart magic-mirror-power-button.service`       #To restart running service

##### View service in syslog (/var/log/daemon.log)
- `sudo journalctl --unit=dummyService`

##### Reload systemctl (If you change anything in service file, or just reboot)
`sudo systemctl daemon-reload`