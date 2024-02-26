rebuild:
	docker-compose build --no-cache && docker-compose up -d --force-recreate

build-up:
	docker compose up --build -d --remove-orphans

build:
	docker compose build

bash:
	docker compose run app bash

up:
	docker compose up

up-d:
	docker compose up -d

down:
	docker compose down --remove-orphans

show_logs:
	docker compose logs

config:
	docker compose  config

migrate:
	docker compose run web python3 manage.py migrate

shell:
	docker compose run web python3 manage.py shell

test:
	docker compose run web python3 manage.py test

makemigrations:
	docker compose run web python3 manage.py makemigrations

collectstatic:
	docker compose run web python3 manage.py collectstatic --no-input --clear

superuser:
	docker compose run web python3 manage.py add_superuser

down-v:
	docker compose down -v

create_db:
	docker-compose exec db createdb -U postgres desmond