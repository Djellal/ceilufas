#!/bin/bash

# Configuration
APP_NAME="ceilufas"
APP_DIR="/var/www/$APP_NAME"
DOMAIN="ceilufas.univ-setif.dz"
VENV_DIR="$APP_DIR/venv"
APACHE_CONF="/etc/apache2/sites-available/$APP_NAME.conf"

echo "=== Starting Deployment of $APP_NAME ==="

# 1. Update and install dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y apache2 libapache2-mod-wsgi-py3 python3-venv python3-pip libpq-dev

# 2. Create application directory
echo "Setting up application directory at $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo chown -R $USER:$USER $APP_DIR

# 3. Copy application files
echo "Copying application files..."
cp -rv ./* $APP_DIR/
# Exclude current venv if it exists in the source
rm -rf $APP_DIR/venv

# 4. Set up Virtual Environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR
source "$VENV_DIR/bin/activate"

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"
# Install gunicorn just in case, though we use mod_wsgi
pip install gunicorn

# 5. Create wsgi.py entry point
echo "Creating wsgi.py..."
cat <<EOF > "$APP_DIR/wsgi.py"
import sys
import os

# Add the app's directory to the PYTHONPATH
sys.path.insert(0, '$APP_DIR')

# Import the create_app factory
from app import create_app

# Create the application instance for mod_wsgi
application = create_app()
EOF

# 6. Create Apache configuration
echo "Creating Apache site configuration..."
cat <<EOF | sudo tee $APACHE_CONF
<VirtualHost *:80>
    ServerName $DOMAIN
    ServerAdmin admin@$DOMAIN

    WSGIDaemonProcess $APP_NAME python-home=$VENV_DIR python-path=$APP_DIR
    WSGIProcessGroup $APP_NAME
    WSGIScriptAlias / $APP_DIR/wsgi.py

    <Directory $APP_DIR>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    Alias /static $APP_DIR/static
    <Directory $APP_DIR/static/>
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/$APP_NAME-error.log
    CustomLog \${APACHE_LOG_DIR}/$APP_NAME-access.log combined
</VirtualHost>
EOF

# 7. Set permissions
echo "Setting permissions for Apache..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 775 $APP_DIR
# Ensure instance folder is writable if it exists (for SQLite or local files)
if [ -d "$APP_DIR/instance" ]; then
    sudo chmod -R 775 "$APP_DIR/instance"
fi
# Ensure static/images/courses is writable if uploads are allowed
if [ -d "$APP_DIR/static/images/courses" ]; then
    sudo chmod -R 775 "$APP_DIR/static/images/courses"
fi

# 8. Enable site and restart Apache
echo "Enabling site and restarting Apache..."
sudo a2ensite $APP_NAME
sudo a2enmod wsgi
sudo systemctl restart apache2

echo "=== Deployment Complete ==="
echo "You can access your application at http://$DOMAIN"
echo "Note: Make sure your DNS is configured to point $DOMAIN to this server's IP."
