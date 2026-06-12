FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /code

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install packages using the default python command mapped by the Playwright image
RUN python -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY . .

# Run uvicorn using the identical 'python' command to match the installation environment
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port $PORT"]
