# pokédex

Pokémon TCG collection database.


## Running

```sh
# ./.env.development
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DEBUG=true
DJANGO_SECRET_KEY="some-secret-key-for-django"
DJANGO_SQLITE_DB_FILE=../data/db.sqlite3
DJANGO_MEDIA_ROOT=../media/
DJANGO_MEDIA_URL=/media/
DJANGO_STATIC_ROOT=
DJANGO_STATIC_URL=/static/
POKEMONTCG_IO_API_KEY=
VITE_API_BASE_URL=http://localhost:8000/
```

### Backend

```sh
$ cd backend/
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

$ python manage.py makemigrations pokedex
$ python manage.py migrate
$ python manage.py createsuperuser

$ python manage.py runserver # Run development server locally
```

### Frontend

```sh
$ cd frontend/
$ yarn install

$ yarn dev
```

## Build

```sh
# ./.env.build
VITE_APP_BASE_PATH=/pjuuldex/
VITE_API_BASE_URL=http://localhost:1337/pjuuldex/api/
```

```sh
$ docker-compose build
```

## Test locally

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
$ docker-compose up # Test locally
```

## Deploy

```sh
$ docker save -o pjuuldex.tar pjuuldex
$ scp pjuuldex.tar vps:/path/to/pjuuldex.tar
# --
$ docker load < pjuuldex.tar
$ docker run \
    --env-file .env.production \
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
