#!/bin/bash

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 SERVER_IP PROJECT_FOLDER"
  exit 1
fi

# Assign arguments to variables
SERVER_IP="$1"
PROJECT_FOLDER="$2"

# Run the command with sudo and redirect the input to the file
sudo bash -c "echo '
server {
    listen 80;
    server_name $SERVER_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/$PROJECT_FOLDER;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
' > /etc/nginx/sites-available/$PROJECT_FOLDER"

sudo ln -s /etc/nginx/sites-available/$PROJECT_FOLDER /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl restart gunicorn



echo "Nginx service file created successfully!"