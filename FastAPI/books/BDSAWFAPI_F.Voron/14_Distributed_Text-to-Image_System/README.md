# Description

## Run

```bash
docker run -d --name fastapi-redis -p 6380:6379 redis

uvicorn app:app 

dramatiq -p 1 -t 1 workers.worker
```
