#!/bin/bash

# Run the command with sudo and redirect the input to the file
sudo bash -c "echo '
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
' > /etc/systemd/system/gunicorn.socket"


echo "Gunicorn socket file created successfully!"