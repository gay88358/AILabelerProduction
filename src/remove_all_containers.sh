#!bin/bash
echo '####################################################'
echo 'Stopping running containers (if available)...'
echo '####################################################'
docker stop $(docker ps -aq)

echo '####################################################'
echo 'Removing containers ..'
echo '####################################################'
docker rm $(docker ps -aq)
