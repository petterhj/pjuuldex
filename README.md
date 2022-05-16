# pokédex

Pokémon TCG collection database.


## Running

```sh
# ./.env.development
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DEBUG=true # default false
DJANGO_SECRET_KEY="some-secret-key-for-django"
DJANGO_SQLITE_DB_FILE=../data/db.sqlite3
DJANGO_MEDIA_ROOT=../media/
DJANGO_MEDIA_URL=/media/
DJANGO_STATIC_ROOT=
DJANGO_STATIC_URL=/static/
DJANGO_ACCESS_TOKEN_LIFETIME_MIN=1 # default 5
DJANGO_REFRESH_TOKEN_LIFETIME_MIN=3 # default 1440
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

# Run development server locally
$ python manage.py runserver
```

### Frontend

```sh
$ cd frontend/
$ npm install

$ npm run dev
```

### Docker

```sh
# ./.env.build
VITE_APP_BASE_PATH=/pjuuldex/
VITE_API_BASE_URL=http://localhost:1337/pjuuldex/api/
```

```sh
$ docker-compose build
$ docker-compose up # Test locally
```

### Data import

```sh
$ python -m scripts/import_set -s base1 -p BS-Base-Set
```

### Resources

* https://florianwoelki.github.io/vue-cirrus
* https://cirrus-ui.netlify.app
* https://pkmncards.com
* https://pokemontcg.io/ (Pokémon TCG Developers)
* https://github.com/PokemonTCG/pokemon-tcg-sdk-python
