::#!bin/bash

@echo off
set prefix=###########################
set newline=^& echo.

echo %prefix%%newline%# start all services %newline%%prefix%
docker-compose down
docker-compose up
echo start all services done
