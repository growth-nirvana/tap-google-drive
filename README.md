# tap-google-drive

A Meltano tap for Google Drive that reads CSV files from a specified Google Drive folder.

## Features

- OAuth2 authentication with Google Drive
- Magic folder mode - each CSV file creates a new table
- Automatic column name conversion to BigQuery-compliant format
- CSV file filtering
- Secure credential management using environment variables

## Installation

1. Clone this repository
2. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies using Poetry:
```bash
poetry install
```

## Configuration

Configure the tap using Meltano's interactive configuration:

```bash
meltano config tap-google-drive set --interactive
```

This will prompt you for:
- `client_id`: Your OAuth 2.0 Client ID
- `client_secret`: Your OAuth 2.0 Client Secret (stored securely)
- `refresh_token`: Your OAuth 2.0 Refresh Token (stored securely)
- `folder_url`: The Google Drive folder URL containing your CSV files

Note: Sensitive credentials (`client_secret` and `refresh_token`) are automatically stored securely by Meltano and will not appear in your `meltano.yml` file.

## Authentication

1. Go to the Google Cloud Console
2. Create a new project or select an existing one
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials
5. Download the client secrets file
6. Place the client secrets file in a secure location
7. Update the `.env` file with the path to your client secrets file

## Usage

Run the tap:
```bash
meltano run tap-google-drive target-jsonl
```

> Note: The CSV Stream is configured to stream all streams and fields in the catalog regardless of selection metadata

## Column Name Conversion

The tap automatically converts CSV column names to BigQuery-compliant format by:
- Removing special characters
- Converting spaces to underscores
- Ensuring the column name starts with a letter
- Converting to lowercase

Example:
- "First Name" → "first_name"
- "1st Column" → "col_1st_column"
- "User's Email" → "users_email"

## Development

### Testing

```bash
poetry run pytest
```

### Linting

```bash
poetry run black .
poetry run isort .
poetry run flake8
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run pre-commit hooks:
```bash
poetry run pre-commit run --all-files
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
