#!/bin/bash

# Variables
WORKERS=1                # Number of worker processes
PORT=80                # Port on which the app will run
HOST=0.0.0.0             # Host to bind

# Start the FastAPI application with uvicorn
exec uvicorn src.main:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --log-level info\
    --reload

