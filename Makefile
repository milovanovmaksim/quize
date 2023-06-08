DOCKER_COMPOSE := deploy/dev.docker-compose.yml
DOCKER_ENV := deploy/.env.dev
DOCKER_COMPOSE_RUNNER := docker compose



.PHONY: compose-up
compose-up:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) up -d


.PHONY: compose-build
compose-build:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) build -d


.PHONY: migrate-create
migrate-create:
	python -m alembic revision --autogenerate -m "Added initial tables"

.PHONY: compose-down
compose-buidownld:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) down


.PHONY: migrate-up
migrate-up:
	python -m alembic upgrade head

