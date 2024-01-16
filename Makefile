black:
	docker compose exec backend black .

isort:
	docker compose exec backend isort .

flake8:
	docker compose exec backend flake8 .

mypy:
	docker compose exec backend mypy .

format:
	docker compose exec backend black .
	docker compose exec backend isort .

check:
	docker compose exec backend black . --check
	docker compose exec backend isort . --check-only
	docker compose exec backend flake8 .
	docker compose exec backend mypy .

test:
	docker compose exec backend pytest ./tests

poetry_show:
	docker compose exec backend poetry show

poetry_add:
	docker compose exec backend poetry add $(LIBRARY)

poetry_add_dev:
	docker compose exec backend poetry add -G dev $(LIBRARY)

poetry_remove:
	docker compose exec backend poetry remove $(LIBRARY)

poetry_update:
	docker compose exec backend poetry update

migrate:
	alembic revision --autogenerate

db_upgrade:
	alembic upgrade head

db_downgrade:
	alembic downgrade -1
