# Investment Manager

A investment management dashboard written in Python using my own "framework"
[mini-mvc](https://github.com/Raisess/mini-mvc), with this tool you can keep
your investments on track at one place.

![Dashboard Image](public/static/assets/dash.png)

### Setup the environment 

You only need to run these setup scripts only once:

```shell
bash ./install-deps.sh
bash ./migrate.sh
python3 -m venv __venv
```

Adding the env configuration, first of all you need to copy the `.env.example`
as the `.env` file:

```shell
cp ./.env.example ./.env
```

and then fill these variables with your Google Cloud client info:

```shell
USE_GOOGLE_OAUTH2=
GOOGLE_OAUTH2_CLIENT_ID=
GOOGLE_OAUTH2_CLIENT_SECRET=
GOOGLE_OAUTH2_SCOPES=

# App Env's
APP_REDIRECT_HOST_BASE=http://localhost:8080
GOOGLE_API_KEY=
```

check on how to do it [here](https://github.com/Raisess/mini-mvc/blob/main/docs/plugins/auth/google_oauth2.md).

### Running localy

Run these commands to start the application:

```shell
box start ./infra.json
source ./__venv/bin/activate
python3 -m ensurepip
python3 -m pip install -r ./requirements.core.txt
python3 -m pip install -r ./requirements.txt
python3 ./src/main.py
```
