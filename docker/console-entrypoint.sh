#!/bin/sh
# SoVa Desk Console — Docker Entrypoint Wrapper
# Fixes volume file permissions before dropping to non-root user
set -e

# Fix ownership of volume-mounted data directories.
# Docker volumes preserve UID/GID from the host or previous container,
# which may not match the sova user (10001) in this container.
if [ "$(id -u)" = "0" ]; then
    chown -R sova:sova /app/data 2>/dev/null || true
    # Fix permissions on sensitive files
    if [ -f /app/data/.session_secret ]; then
        chmod 600 /app/data/.session_secret
        chown sova:sova /app/data/.session_secret
    fi
    if [ -f /app/data/auth.db ]; then
        chown sova:sova /app/data/auth.db
    fi
    # /opt/rustdesk may be mounted read-only from server volume — only fix if writable
    chown -R sova:sova /opt/rustdesk 2>/dev/null || true
    # Drop privileges and run the actual entrypoint
    exec su-exec sova /app/docker-entrypoint.sh
else
    exec /app/docker-entrypoint.sh
fi
