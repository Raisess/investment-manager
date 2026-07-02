#! /usr/bin/env sh

rm -rf sqlite.db

migrate init sqlite
sleep 2
migrate run sqlite
