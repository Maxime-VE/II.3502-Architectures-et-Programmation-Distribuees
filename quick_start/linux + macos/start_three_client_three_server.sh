#!/bin/bash

start_python_script() {
    local script=$1
    osascript -e 'tell app "Terminal" to do script "cd ../../Python; python3 '$script'; exec bash"'
}

start_python_script "server.py"
sleep 1
start_python_script "server.py"
sleep 1
start_python_script "server.py"
sleep 2

start_python_script "client.py"
sleep 1
start_python_script "client.py"
sleep 1
start_python_script "client.py"