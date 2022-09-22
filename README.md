# YTVideoFeed

YTVideoFeed is a simple REST API that gets the latest videos' details on YouTube under a pre-specified topic.  
It does not get the videos, but the details of the videos and their link - title, description, channel name, url.

## Tech stack
- Django Rest Framework
- PostgreSQL
- Docker
- YouTube Data API

## Endpoint
```sh
/<topic>/           lists details of recent videos (most recent first)
/<topic>/?search    allows searching the details of all the collected videos
```

## Installation

Install Docker

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
- YT videos fetched in the background continuously using YouTube Data API
- YT video details stored in PostgreSQL database
- pagination 
- videos sorted in reverse chronological order
- dockerized
- support for cycling through multiple API keys
- choose topic by setting it as an environment variable
- get the time of most recently published video in our database
    - to set as the publishedAfter field in YT API

## Design Decisions
- I have used Advanced Python Scheduler to schedule the background process that fetches the YT videos.
    - I had previously used bash and python scripts that periodically ping the YouTube API and ingests the data into my REST API using POST requests. But using the APScheduler is not only faster without using POST requests, but also simple and scalable.
- Limit Offset Pagination
- When the server is running continuously well, we know the last fetch would have occurred 60 seconds ago, but if the server is being restarted or a connection is restored after a break, we would need to set the lower bound limit to the last fetched video. Hence, I am getting the time of the most recently fetched videoo and using it as publishedAfter field to get videos published after that time.

## Working Details
1. A paginated viewset handles the endpoint along with searching and pagination features.
2. YouTube's Data API is used to fetch the video details from YouTube.
4. Given multiple API keys, the script will start using the first one. When the HTTP response returns an error, it will use the next key in the list, until all keys have been attempted. If none of the keys work, it will sleep for 60 seconds and try again from the first key.

## Files
### Fetching
- ```fetcher.py``` Schedules calls to videoFetchApi.py 
-  ```videoFetchApi.py``` The fetch logic 
    - ```get_last_time()``` gets the last time video details were fetched
    - ```fetch_videos()``` connects to the YouTube API and gets the data
    - ```save_details()``` saves the fetched video details to the DB

### Demo Images
- ```BeforeUpdate.jpeg```     Immediately before a fetch op
- ```AfterUpdate.jpeg```      Immediately after a fetch op, after the BeforeUpdate.jpeg  
- ```GET.jpeg```              GET request results
- ```SEARCH.jpeg```           SEARCH api example 
  
## Future enhancements
- Replace limit offset pagination with a faster pagination technique that can handle edge cases
    - use the next page token
- Use Redis and Celery for fetching videos instead
- Add user profiles and authentication
- Add support for multiple separate topics
- writing better tests
- add loggers
- group the docker files
- deployment
- make time duration an environment variable as well
- add feature to save videos offline
- prevent duplication of videos
- create indexes for better performance
