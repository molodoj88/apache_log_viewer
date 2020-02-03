# Viewer for apache logs
## Prerequisites
To get started, you need [Docker](https://docs.docker.com/install/) and [Docker-compose](https://docs.docker.com/compose/install/) installed.

## Install
1. Clone or download project:
```bash
git clone https://github.com/molodoj88/apache_log_viewer.git
```
2. Go to project root directory:
```bash
cd apache_log_viewer
```
3. Build docker images:
```bash
sudo docker-compose build
```
4. Start services:
```bash
sudo docker-compose up -d
```
_________
Nginx is used as a web server.  
  
After start service parses test log file (link is in *app/entrypoint.sh*). You may provide your own link to parse.
