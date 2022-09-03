#!/usr/bin/env bash
python manage.py makemigrations
echo "............Apply database migrations............"
python manage.py migrate
echo "...................Fetching......................"
nohup /bin/sh -c "sh /code/fetch.sh &" && sleep 2
echo "................Starting server.................."
python manage.py runserver 0.0.0.0:8000