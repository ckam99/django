# Django Rest Framework

- Django Rest Framework
- Celery 
- Redis
- Docker
- Nginx
- Guvicorn

#### Set environment variables

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

