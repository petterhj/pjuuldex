# pokédex

Pokémon TCG collection database.


## Running

### Backend

```sh
$ make init-backend

$ python manage.py makemigrations pokedex
$ python manage.py migrate
$ python manage.py createsuperuser

$ make run-backend # Run development server locally
```

### Frontend

```sh
$ make init-frontend
$ make run-frontend
```

## Build

```sh
# ./.env.build
VITE_APP_BASE_PATH=/path/
VITE_API_BASE_URL=http://localhost:8000/api/
```
```sh
# ./.env.local
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DEBUG=true
DJANGO_MEDIA_PATH=/app/media/
DJANGO_MEDIA_URL=/pjuuldex/media/
DJANGO_SECRET_KEY="some-secret-key-for-django"
DJANGO_SQLITE_DB_FILE=/app/data/db.sqlite3
DJANGO_STATIC_ROOT=/app/dist/assets/
DJANGO_STATIC_URL=/pjuuldex/assets/
POKEMONTCG_IO_API_KEY=
```


```sh
$ yarn build
$ docker-compose build # and/or
$ docker-compose up [--build]

$ docker save -o pjuuldex.tar pjuuldex
```

## Deploy

```sh
$ scp pjuuldex.tar vps:/path/to/pjuuldex.tar
# --
$ docker load < pjuuldex.tar
$ docker run \
    --env-file .env \
    -p 8081:8000 \
    -v data:/app/data/ \
    -v media:/app/media/ \
    -v dist:/app/dist/ \
    --name pjuuldex pjuuldex
```

### Reverse proxy

```nginx
# TODO
```

### Data import

```sh
PYTHONPATH=. python scripts/import_set.py -s base1 -p BS-Base-Set
```

### Resources

* https://florianwoelki.github.io/vue-cirrus
* https://cirrus-ui.netlify.app
* https://pkmncards.com
* https://pokemontcg.io/ (Pokémon TCG Developers)
* https://github.com/PokemonTCG/pokemon-tcg-sdk-python
