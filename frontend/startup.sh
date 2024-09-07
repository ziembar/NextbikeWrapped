#!/bin/sh

API_URL=$(cat /etc/secrets/api_url.txt)
sed -i "s|API_URL_PLACEHOLDER|${API_URL}|g" /usr/src/app/frontend/src/environments/environment.ts

exec "$@"