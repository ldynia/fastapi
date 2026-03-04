#!/usr/bin/env bash

set -Eeuo pipefail

# WARNING: This startup script violates "Strictly separate build and run stages" rule of the 12-factor app methodology.
# This project is never meant to be used in production.
# It serves demonstration purposes only, and is designed for testing purposes only.

print_ips() {
  APP_CONTAINER_IP=$(ip addr | grep inet | tail -n1 | awk '{print $2}' |  cut -d'/' -f1)
  PORSTGRES_CONTAINER_IP=$(ping  postgres -c 1 | grep -E -o '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1)
  REDIS_CONTAINER_IP=$(ping  redis -c 1 | grep -E -o '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1)
  echo "------------------------------------------"
  echo "App: $APP_CONTAINER_IP"
  echo "Postgress: $PORSTGRES_CONTAINER_IP"
  echo "Redis: $REDIS_CONTAINER_IP"
  echo "------------------------------------------"
}

create_self_signed_ssl_cert_with_root_ca() {
  # https://learn.microsoft.com/en-us/azure/application-gateway/self-signed-certificates

  if ! [ -f "/etc/wfs/ssl/certs/wfs.crt" ]; then
    # Generate the private key for root CA
    openssl ecparam -out /etc/wfs/ssl/private/root.key -name prime256v1 -genkey

    # Generate the certificate signing request for the root CA
    openssl req -new -sha256 -key /etc/wfs/ssl/private/root.key -out /etc/wfs/ssl/certs/root.csr -config /usr/src/config/root.ssl.conf

    # Generate self-signed certificate for root CA
    openssl x509 -req -sha256 -days 365 -in /etc/wfs/ssl/certs/root.csr -signkey /etc/wfs/ssl/private/root.key -out /etc/wfs/ssl/certs/root.crt

    # Generate the private key for the WFS
    openssl ecparam -out /etc/wfs/ssl/private/wfs.key -name prime256v1 -genkey

    # Generate the certificate signing request for the WFS
    openssl req -new -sha256 -key /etc/wfs/ssl/private/wfs.key -out /etc/wfs/ssl/certs/wfs.csr -config /usr/src/config/ssl.conf

    # Generate self-signed certificate for the WFS
    openssl x509 -req -in /etc/wfs/ssl/certs/wfs.csr -CA  /etc/wfs/ssl/certs/root.crt -CAkey /etc/wfs/ssl/private/root.key -CAcreateserial -out /etc/wfs/ssl/certs/wfs.crt

    # Verify the certificate
    openssl verify -CAfile /etc/wfs/ssl/certs/root.crt /etc/wfs/ssl/certs/wfs.crt

    chmod 444 /etc/wfs/ssl/certs/wfs.crt
    chmod 400 /etc/wfs/ssl/private/wfs.key
  fi
}

create_self_signed_ssl_cert_without_root_ca() {
  if ! [ -f "/etc/wfs/ssl/certs/wfs.crt" ]; then
    # Generate self-signed certificate X.509
    openssl req \
      -config /usr/src/config/ssl.conf \
      -keyout /etc/wfs/ssl/private/wfs.key \
      -newkey rsa:4096 \
      -out /etc/wfs/ssl/certs/wfs.crt \
      -nodes \
      -x509

    chmod 444 /etc/wfs/ssl/certs/wfs.crt
    chmod 400 /etc/wfs/ssl/private/wfs.key
  fi
}

# Execute functions
print_ips

# if args empty
if [ -z "$@" ]; then
  UVICORN_OPTIONS_COMMON="
    --host 0.0.0.0 \
    --log-config /usr/src/config/log.ini \
    --reload \
    --reload-include '*.html' \
    --reload-include '*.js' \
    --reload-include '*.py'
  "
  if [ "$TLS_ENABLE" -eq 1 ]; then
    UVICORN_OPTIONS_TLS="
      --ssl-certfile /etc/wfs/ssl/certs/wfs.crt \
      --ssl-keyfile /etc/wfs/ssl/private/wfs.key
    "
    # WARNING: DON'T GENERATE CERTIFICATES ON THE FLY!
    # REASON: We do it ONLY to have a user interaction-less setup.
    # ALTERNATIVE: Generate certificates outside of the project setup and pass them with https://docs.docker.com/compose/use-secrets/
    echo "Generating self-signed SSL certificate"
    # create_self_signed_ssl_cert_with_root_ca
    create_self_signed_ssl_cert_without_root_ca

    echo "Visit Django and Starlette application on:"
    echo "- https://localhost:${APP_PORT_HTTP}"
    echo "------------------------------------------"

    uvicorn main:app --port $APP_PORT_HTTP $UVICORN_OPTIONS_COMMON $UVICORN_OPTIONS_TLS
  else
    echo "Visit Django and Starlette application on:"
    echo "- http://localhost:${APP_PORT_HTTP}"
    echo "------------------------------------------"

    uvicorn main:app --port $APP_PORT_HTTP $UVICORN_OPTIONS_COMMON
  fi
else
  exec "$@"
fi
