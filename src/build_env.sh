#!bin/bash
###############################################################################
# build_docker_app
###############################################################################
echo "[build.sh] build ail_frontend"
sudo docker build -t ail_frontend:v1.0.0.0 --build-arg http_proxy=http://10.18.131.1:8080 -f ./client/Dockerfile .
echo "[build.sh] saving ail_frontend.tar"
sudo docker save ail_frontend:v1.0.0.0 > ../image/ail_frontend.tar

echo "[build.sh] build ail_backend"
sudo docker build -t ail_backend:v1.0.0.0 --build-arg http_proxy=http://10.18.131.1:8080 -f ./backend/webserver/Dockerfile .
echo "[build.sh] saving ail_backend.tar"
sudo docker save ail_backend:v1.0.0.0 > ../image/ail_backend.tar

echo "[build.sh] build ail_workers"
sudo docker build -t ail_workers:v1.0.0.0 --build-arg http_proxy=http://10.18.131.1:8080 -f ./backend/workers/Dockerfile .
echo "[build.sh] saving ail_workers.tar"
sudo docker save ail_workers:v1.0.0.0 > ../image/ail_workers.tar


