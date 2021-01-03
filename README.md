# wemo-auto-kotatsu
Turns on my kotatsu when the light is turned on

## Info
This is purpose built for my house. I am too lazy to turn the power on the other side of the room.

I have a belkin Wemo insight smart plug, that I monitor the power usage of. When the power usage goes higher than a specific amount I know that the light is turned on I turn on another adapter on the other side of the room. When the light turns off, I turn off the other side. Also I let the other side of the room be on for up to 15 minutes, to facilitate prewarming the kotatsu.

## Files explained
files | explanation
--- | ---
flask_prog.py | python webserver that calls open and close garage door
Dockerfile | makes the container that closes and opens garage door
docker-compose.override.yml | extends traefik_duckdns docker-compose to add this project
rules/garage.toml | traefik config file to add webserver & expose it securely to internet
pymyq-wrapper.py | example warpper for [pymyq](https://github.com/arraylabs/pymyq) that is controlled via exec
pyproject.toml | [poetry](https://python-poetry.org/) project file
poetry.lock | [poetry](https://python-poetry.org/) lock file

