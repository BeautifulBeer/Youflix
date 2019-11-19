# Get current directory
dir=$(pwd)
# Django directory
djangoDIR="${dir}/django-vue/djangoAPI"
# Front directory
frontDIR="${dir}/frontend"
# Config directory
configDIR="${dir}/django-vue/.config"

# Delete prev database, pycache
rm "${djangoDIR}/db.sqlite3"
rm "${djangoDIR}/api/migrations/*_initial.py"
 
# Activate virtualenv
cd "${djangoDIR}"
pyenv activate youflix

# Install all packages
pip3 install -r requirements.txt

# Django database setup
python "${djangoDIR}/manage.py" makemigrations
python "${djangoDIR}/manage.py" migrate
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/collection.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/company.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/country.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/genre.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/keyword.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/language.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/movie.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/crew.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/cast.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/user_profile_cluster.json"
python "${djangoDIR}/manage.py" loaddata "${djangoDIR}/json/rating.json"

# Create static root of youflix, for nginx
mkdir "${dir}/django-vue/.static_root"

# Gunicorn installation
sudo apt-get -y install gunicorn

# Nginx installation
sudo apt-get -y install nginx

# Register Gunicorn as a daemon
sudo ln -s "${configDIR}/gunicorn/gunicorn.service" /etc/systemd/system/
mkdir "${djangoDIR}/run/"

# Register nginx app, youflix
sudo cp -f "${configDIR}/nginx/youflix.conf" /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/youflix.conf /etc/nginx/sites-enabled/
touch "${djangoDIR}/logs/nginx-access.log"
touch "${djangoDIR}/logs/nginx-error.log"

# Nodejs
sudo apt-get -y install nodejs
sudo apt-get -y install npm

# NPM build
cd "${frontDIR}"
npm install
npm run build

# Django 
yes | python "${djangoDIR}/manage.py" collectstatic

# Reload daemon serivce (apply gunicorn.service)
sudo systemctl daemon-reload

# Start gunicorn, nginx
sudo systemctl start gunicorn.service
sudo systemctl start nginx.service
