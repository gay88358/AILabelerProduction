::#!bin/bash

@echo off
set prefix=###########################
set newline=^& echo.

echo %prefix%%newline%# load all related images %newline%%prefix%
for /r %%i in (..\image\*.tar) do (
docker load < %%i
)
echo load all related images done

echo %prefix%%newline%# start all services %newline%%prefix%
docker-compose down
docker-compose up
echo start all services done
