# Description

## Docker

### Database

```bash
docker run --name my-postgres -e POSTGRES_PASSWORD=123456 -d -p 5432:5432 postgres
```

### Build Image

```bash
docker build -t fastapi-app .
```

### Run Image locally

```bash
docker run -p 8000:80 -e ENVIRONMENT=production fastapi-app
```
