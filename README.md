
# Home Media Server

Turning my old laptop into a home media server to store images 


## Tech Stack

**Client:** HTML, CSS, Javascript

**Server:** FastAPI, docker, nginx, github action runner, Virtual Machine


## Environment Variables

To run this project, you will need to add the following environment variables to your github actions secrets

`DOCKER_USERNAME`

`DOCKER_TOKEN`

Setup github actions runner in you VM or the device you want your server to stay on ,
if you were to use public cloud , ssh feature documented in appleboy/ssh-action . Since I contected this project on private home network , github action runner was used.

Copy the .env.example as .env and enter your database variable values

```bash
  cp .env.example .env
```
`DB_HOST`
`DB_PORT`
`DB_NAME`
`DB_USER`
`DB_PASSWORD`


## Deployment

To deploy this project prepare a VM [I am using debian cli] or have a machine with linux ready

- Set up netplan to give you machine a static ip
```bash
 /etc/netplan/00-installer-config.yaml

network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.254    /* Run ifconfig in wifi connected device to check your default route*/
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
      dhcp6: true
```

- Set up docker
- Install github action runner 
[Installation Guide](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)

- Write up a docker-compose-prod.yml file 

```bash
prod@home-server-prod:~/home-media-server$ cat docker-compose-prod.yml
services:

    frontend:
        image: manhumann/home-media-frontend:latest
        restart: unless-stopped
        ports:
            - "80:80"
        volumes:
            - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    backend:
        image: manhumann/home-media-backend:latest
        restart: unless-stopped
        ports:
            - "8000:8000"
        env_file:
            - .env
        depends_on:
            - postgres
        volumes:
            - /home/admin/home-media-data/uploads:/server/uploads

    postgres:
        image: manhumann/home-media-postgres:latest
        restart: unless-stopped
        environment:
            POSTGRES_DB: ${DB_NAME}
            POSTGRES_USER: ${DB_USER}
            POSTGRES_PASSWORD: ${DB_PASSWORD}
        volumes:
            - /home/admin/home-media-data/postgres:/var/lib/postgresql/data


```

- I setup nginx file in prod server too , there could be a better way of doing it , but I chose this
```bash
prod@home-server-prod:~/home-media-server/nginx$ cat nginx.conf
server {

    listen 80;

    client_max_body_size 50M;

    location / {

        root /usr/share/nginx/html;

        index index.html;

    }

    location /api/ {

        proxy_pass http://backend:8000/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;

    }
}
```

Overall , the prod server sould look something like this 
```bash
prod@home-server-prod:~$ ls -l
total 12
drwxr-xr-x 6 prod prod   4096 Aug  7 11:01 actions-runner
drwxr-x--- 7 prod prod 4096 Aug  7 10:25 ..
```

- deploy.sh is executed by github actions to pull the image and start the container
```bash
prod@home-server-prod:~$ cat deploy.sh
#!/bin/bash

set -e

echo "====== Starting Deployment ======="

docker compose -f docker-compose-prod.yml pull

echo "Starting Containers ...."
docker compose -f docker-compose-prod.yml up -d

echo "Checking Services ...."
docker compose -f docker-compose-prod.yml ps

echo "=== Deployment complete ==="
```
make sure to make the script executable by ```chmod +x deploy.sh``` cd /home/prod/home-media-server

echo  "Pulling latest image ..... "
-rw-r--r-- 1 prod prod  132 Aug  6 14:31 .env
-rw-r--r-- 1 prod prod  898 Aug  7 11:26 docker-compose-prod.yml
drwxr-xr-x 2 prod prod 4096 Aug  8 04:57 nginx
-rwxrwxr-x 1 prod docker  373 Aug  7 10:25 deploy.sh

drwxrwxr-x 3 prod prod 4096 Aug  7 11:26 .
```bash
prod@home-server-prod:~/home-media-server$ ls -la
total 20

