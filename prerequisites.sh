# Clone git repository
cd ~
git clone https://lab.ssafy.com/Jo_yongseok/youflix.git

# Install dependencies of pyenv
sudo apt-get install -y make build-essential \
 libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
 wget curl llvm libncurses5-dev libncursesw5-dev \
 xz-utils tk-dev git python-pip
 
# Install pyenv.
curl -L \
https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer \
| bash

# Setup environmental variables for pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile

# Install python 3.6.8
pyenv install 3.6.8

# Setup environmental variables for pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Create virtual environment using pyenv-virtualenv
pyenv virtualenv youflix
