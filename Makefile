generate:
	alembic revision --autogenerate -m "$(NAME)"

migrate:
	alembic upgrade head
