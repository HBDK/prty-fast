curl --request POST \
  --url http://localhost:8000/sonarr \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnium/0.2.3-a' \
  --data '{
  "series": {
    "id": 1,
    "title": "Test Title",
    "path": "C:\\testpath",
    "tvdbId": 1234,
    "tvMazeId": 0,
    "type": "standard"
  },
  "episodes": [
    {
      "id": 123,
      "episodeNumber": 1,
      "seasonNumber": 1,
      "title": "Test title"
    },
		{
      "id": 234,
      "episodeNumber": 2,
      "seasonNumber": 1,
      "title": "Test title 2"
    }
  ],
  "eventType": "Test"
}'