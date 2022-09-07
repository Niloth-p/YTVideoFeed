# YTVideoFeed

YTVideoFeed is a simple REST API that gets the latest videos' details on YouTube under a pre-specified topic.  
It does not get the videos, but the details of the videos and their link - title, description, channel name, url.

## Endpoint:
```sh
/<topic>/           lists details of recent videos (most recent first)
/<topic>/?search    allows searching the details of all the collected videos
```

## Installation:

### Tech stack: 
#### Django Rest Framework, postgresql, Docker
Install the dependencies

### Clone
Before cloning, you might want to set 'git config --global core.autocrlf false' if on Windows.

### Required Environment variables
Create a .env file in the following format with these values or use flags with docker compose command:

- ```YOUTUBE_DATA_API_KEY```: Generate an API key from https://console.cloud.google.com/
To attach multiple API keys, use as `YOUTUBE_DATA_API_KEY=<KEY1>,<KEY2>,<KEY3>` without quotes or spaces
- ```DB_NAME```: postgresql database name eg: 'videodetailsdb'
- ```DB_USERNAME```: postgresql username
- ```DB_PASSWORD```: postgresql password
- ```DJANGO_SECRET_KEY```: any random string with prefix 'django-insecure-'  
eg: ```'django-insecure-r*c##r=ejiw5w@u*jdaj(gemm7gcb6w*$)*fl677@fgyr&ep8^'```
- ```TOPIC```: the only topic you want videos from eg: 'tutorial', 'chess'

### Command
`docker compose up`  
Verify the deployment by navigating to your server address in your preferred browser. `127.0.0.1:8000`  
It will take 60 seconds for the first batch of data to come in.
Once the data starts coming in, you can peruse and click on any of the URLs to view the video in youtube.

## Assumptions
- The topic is pre-specified as an environment variable
- No authentication is required

## Limitations
The API refreshes with upto 50 new videos every 60 seconds.  
An API key is limited to 100 public calls per day, as of now.

## Implemented features
- viewset - GET/POST/PUT/DELETE endpoint of YT videos
- search endpoint 
- YT videos fetched in the background continuously
- YT video details stored in PostgreSQL database
- pagination 
- videos sorted in reverse chronological order
- dockerized
- support for cycling through multiple API keys
- choose topic by setting it as an environment variable

## Design Decisions
- To run an infinite periodical background process, we would ideally need websockets. We would need Redis for that.  
We could use Celery or Huey in addition to create such scheduled jobs.
    - I have bypassed them by using Docker to host background bash and python scripts that periodically ping the YouTube API and ingests the data into my REST API using POST requests
- Limit Offset Pagination

## Working Details
1. A paginated viewset handles the endpoint along with searching and pagination features.
2. YouTube's Data API is used to fetch the video details from YouTube.
4. Given multiple API keys, the script will start using the first one. When the HTTP response returns an error, it will use the next key in the list, until all keys have been attempted. If none of the keys work, it will sleep for 60 seconds and try again from the first key.

### Scripts
1. Dockerfile calls docker-entrypoint.sh.
2. docker-entrypoint.sh runs manage.py commands.
It also calls fetch.sh.
3. fetch.sh is a background process that calls background_tasks.py every 60 seconds
4. background_tasks.py has 3 functions.
    1. get_last_time() fetches the last time video details were fetched
    2. fetch_videos() connects to the YouTube API and gets the data
    3. save_details() saves video details to the DB through POST requests

## Future enhancements
- Replace limit offset pagination with a faster pagination technique
- Use scheduled jobs for fetching videos instead
- Add user profiles and authentication
- Add support for multiple separate topics
