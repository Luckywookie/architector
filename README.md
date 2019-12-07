# Education project - online store

## Development setup

### Prerequisites:

0) Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
1) Install Docker (Choose one of the following)
    * [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
    * [Mac OS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
    * Ubuntu
        1) [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
        2) Docker-Compose    
            1) Run `sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
            2) Run `sudo chmod +x /usr/local/bin/docker-compose`
        3) Update current user groups
            1) Run `sudo groupadd docker && sudo usermod -aG docker $USER`
2) Install [Python 3.7.4](https://www.python.org/downloads/)
3) Install pipenv
    
    Run `pip install -U pipenv` 

### Clone the Repo

Run `git clone git@github.com:Luckywookie/architector.git`


### Docker compose start

Run `docker-compose up -d`
