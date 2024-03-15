# Base image with tag (version)
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set environment variable at build/run time
# APP_MODULE points to the path of FastAPI application
# Same argument used in Uvicorn/Gunicorn commands
ENV APP_MODULE app:app

# Copies local file system to the image
COPY requirements.txt /app

# Execute Unix commands
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copies rest of source code files into /app directory
COPY ./ /app