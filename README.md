# Telegram Stickers Organizer Bot

A versatile Telegram bot for managing and organizing sticker packs.

## Features

- Rename sticker packs
- Merge multiple sticker packs
- Remove last N stickers from a pack
- Edit individual stickers in a pack (change emoji, delete)
- Duplicate sticker packs with a new name and link
- Convenient way to add stickers to renamed stolen sticker pack
- Move stickers between packs from web interface

## Prerequisites

- Python 3.12 or higher
- `uv` package manager
- `ngrok` and `jq` for local development

## Installation

Clone the repository:

```sh
git clone https://github.com/yourusername/telegram-stickers-organizer.git
cd telegram-stickers-organizer
```

Install dependencies and copy `.env` config:

```sh
make provision
```

Edit the `.env` file and add your Telegram Bot Token and other required
variables.

## Usage

To start the bot locally:

```sh
make start
```

This command will start ngrok and run the bot.

## Development

### Linting

To lint the code:

```sh
make lint
```

This will run both `ruff` and `flake8`.

## Project Structure

- `makefiles/`: Makefile recipes
- `frontend/`: Web interface for managing sticker packs (NextJS)
- `src/telegram_stickers_organizer/`: Main application code
  - `handlers/`: Command handlers
  - `interactors/`: Business logic
  - `utils/`: Utility functions
  - `keyboard/`: Keyboard layouts
  - `middlewares/`: Middleware components
  - `repositories/`: Data storage and retrieval

## Things to think

- Instead of user_id I should display username. Though, it may be renamed
- When user renames sticker pack, code is broken, I should find ways to fix it
- There has to be a lot more of async operations in code, lots of operations
  might be done in background. Will make them if I would need more python
  experience
- There has to be another, more mature way to store data — to refresh and cache
  a lot of info in the database
- Think about Telegram API limitations
