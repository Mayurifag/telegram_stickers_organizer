.PHONY: run
run:
	uv run $(ARGS)

.PHONY: install
install:
	uv add $(ARGS)

.PHONY: add
add: install

.PHONY: remove
remove:
	uv remove $(ARGS)

.PHONY: provision
provision:
	uv sync
	cp .env.example .env

.PHONY: start
start: start-ngrok
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file, edit it and run "make start" again"; exit 1; fi
	uv run src/telegram_stickers_organizer/main.py

.PHONY: lint
lint:
	uvx ruff
	uvx flake8
