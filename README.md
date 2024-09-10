# Telegram Stickers Organizer Bot

A versatile Telegram bot for managing and organizing sticker packs.

## Features

- Rename sticker packs
- Merge multiple sticker packs
- Remove last N stickers from a pack
- Edit individual stickers in a pack (change emoji, delete)
- Duplicate sticker packs with a new name and link

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

- `src/telegram_stickers_organizer/`: Main application code
  - `handlers/`: Command handlers
  - `interactors/`: Business logic
  - `utils/`: Utility functions
  - `keyboard/`: Keyboard layouts
