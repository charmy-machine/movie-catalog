# Movie Catalog

## Develop

### Setup:

Right click on `app` -> Mark directory as -> Sources Root

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