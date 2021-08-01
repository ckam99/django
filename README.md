# Django Celery Redis using Docker, Nginx and Guvicorn

- Set environment variables

```
cp .env.example .env
```

#### Dev environment
```
docker-compose up --build
```

#### Production environment

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up  --build
```

