# Backend home task
**Async HTTP web service with FAST API**
-

Run database with `docker run --name postgres-fastapi -e POSTGRES_PASSWORD=postgres-fastapi --rm -p 5432:5432 postgres`

Run server with `fastapi dev source/` or `fastapi run source/`

**Use Docker**
-
Create `db/password.txt` and make sure your `.env` have `DB_HOST=db`

Run 
- 
- `docker-compose build`
- `docker-compose up`