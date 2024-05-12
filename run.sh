#!/bin/bash
python3 MakeScreen.py &
python3 main.py &
g++ main.cpp -o compiled
./compiled
