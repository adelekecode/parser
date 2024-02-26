#!/bin/bash

# Get the project folder from the first command-line argument
PROJECT_FOLDER="$1"

# Check if the project folder argument is provided
if [ -z "$PROJECT_FOLDER" ]; then
  echo "Error: Project folder not provided."
  echo "Usage: ./myscript.sh <project_folder>"
  exit 1
fi

# Generate the contents of the gunicorn.service file
SERVICE_CONTENT="[Unit]
Description=Gunicorn
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/${PROJECT_FOLDER}
ExecStart=/home/${PROJECT_FOLDER}/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock config.wsgi:application

[Install]
WantedBy=multi-user.target"

# Create the gunicorn.service file with the generated contents
echo "$SERVICE_CONTENT" | sudo tee /etc/systemd/system/gunicorn.service > /dev/null

# Reload systemd to pick up the changes
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl restart gunicorn

echo "Gunicorn service file created successfully!"