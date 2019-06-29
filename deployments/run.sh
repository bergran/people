#!/usr/bin/env bash
pip install -r requirements.txt && \
sh scripts/migrate.sh head && \
sh scripts/generate_dummy_data.sh && \
sh scripts/runserver.sh
