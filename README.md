# pokédex

Pokémon TCG collection database.


## Backend

```sh
# .env
POKEDEX_SECRET_KEY=""
POKEDEX_DEBUG=true
POKEDEX_ALLOWED_HOSTS=localhost,127.0.0.1
POKEDEX_SQLITE_DB_FILE="../data/db.sqlite3"
POKEDEX_MEDIA_PATH="../media/"
```

```sh
$ cd backend/
$ pipenv install [--dev]

$ pipenv shell
$ python manage.py makemigrations pokedex
$ python manage.py migrate
$ python manage.py createsuperuser

$ pipenv run api # Run development server locally
```

## Frontend

```sh
# .env.development
VITE_API_BASE_URL=http://localhost:8000
```

```sh
$ yarn install
$ yarn dev
$ yarn build
```

### Resources

* https://florianwoelki.github.io/vue-cirrus
* https://cirrus-ui.netlify.app
* https://pkmncards.com
* https://pokemontcg.io/ (Pokémon TCG Developers)
* https://github.com/PokemonTCG/pokemon-tcg-sdk-python
