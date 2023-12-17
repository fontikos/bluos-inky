#!/bin/sh
# Set up as a system service

PWD=`pwd`
ME=`whoami`

cat > bluos-inky.service << EOF
FILE="[Unit]
Description=BluOS Inky
After=multi-user.target

[Service]
Type=simple
Restart=always
Environment=PYTHONUNBUFFERED=1
User=$ME
WorkingDirectory=$PWD
ExecStart=/usr/bin/python3 $PWD/bluos-inky.py
StandardOutput=journal+console
StandardError=journal+console

[Install]
WantedBy=multi-user.target
EOF

sudo cp bluos-inky.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bluos-inky.service
sudo systemctl restart bluos-inky.service

rm bluos-inky.service

# To follow the output:
# journalctl -f -u bluos-inky.service
