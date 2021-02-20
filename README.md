# FastAPI USER SERVICE

This application handles user authentication (using JWT) and verification (using numeric token sent to registered users email).

## Dependencies

- Python3
- PostgreSQL

## Create and Activate Virtual Environment

```shell
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```shell
pip install -r requirements.txt
```

### Run application

```shell
uvicorn main:app
```

- Environment variables are read from the `.env` file at the root folder
- default host is `127.0.0.1`
- default port is `8000`

### Documentation

The swagger documentation is located at `localhost:8000/docs`
