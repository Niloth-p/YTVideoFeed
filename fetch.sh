#!/usr/bin/env bash
while true
do
  sleep 60
  nohup python -u background_tasks.py > output.log &
done