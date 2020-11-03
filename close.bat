::#!bin/bash

@echo off
set prefix=###########################
set newline=^& echo.

echo %prefix%%newline%# close all services %newline%%prefix%
docker-compose down
