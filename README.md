# FastAPI URL Shortener

## Develop

### Setup:

Right click `app` -> Mark directory as -> Sources Root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install

Install packages:
```shell
uv install
```

### Run

Go to workdir:
```shell
cd app
```

Run dev server:
```shell
fastapi dev
```

## Snippets
Generate random token for unsafe methods
```shell
python -c "import secrets; print(secrets.token_urlsafe(16))"
```
