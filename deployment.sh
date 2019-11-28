# Get current directory
dir=$(pwd)
# Config directory
configDIR="${dir}/django-vue/.config"

# Change configuration of .config files. Invalid path is exists
# gunicorn.service
# WorkingDirectory, ExecStart should be changed 
# nginx.service
# access_log, error_log, proxy_pass, alias should be changed

# Register Gunicorn as a daemon
sudo ln -s "${configDIR}/gunicorn/gunicorn.service" /etc/systemd/system/
mkdir "${djangoDIR}/run/"

# Register nginx app, youflix
sudo cp -f "${configDIR}/nginx/youflix.conf" /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/youflix.conf /etc/nginx/sites-enabled/
touch "${djangoDIR}/logs/nginx-access.log"
touch "${djangoDIR}/logs/nginx-error.log"

# Start gunicorn, nginx
sudo systemctl start gunicorn.service
sudo systemctl start nginx.service
