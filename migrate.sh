#! /usr/bin/env sh

migrate init sqlite
sleep 2
migrate run sqlite
