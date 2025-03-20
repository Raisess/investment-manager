#! /usr/bin/env sh

export DB_NAME="postgres"
export DB_USER="postgres"
export DB_PASS="postgres"

box stop ./infra.json
box delete ./infra.json
sleep 2
box create ./infra.json
box start ./infra.json

sleep 2
migrate init postgres
sleep 2
migrate run postgres

unset DB_NAME
unset DB_USER
unset DB_PASS
