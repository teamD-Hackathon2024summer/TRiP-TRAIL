#!/bin/sh

# Ensure environment variables are loaded
export $(cat .env | xargs)

# Run the application
uvicorn main:app --host 0.0.0.0 --port ${PORT_FAST}
