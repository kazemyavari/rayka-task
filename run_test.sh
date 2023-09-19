#!/bin/bash
docker compose -f docker-compose-test.yml up -d
sleep 10
python manage.py test
docker compose -f docker-compose-test.yml down
