FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /code

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Force python3 to explicitly run pip so dependencies land in its exact environment path
RUN python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY . .

# Run uvicorn as a module from the exact same python3 executable
CMD ["sh", "-c", "python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT"]
