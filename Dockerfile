FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /code

# 1. Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# 2. Install packages using the active image environment
RUN python -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 3. Create an environment variable pointing to the *true* python binary location
RUN echo "export REAL_PYTHON=$(which python)" >> /etc/profile

# 4. Copy the rest of your application code
COPY . .

# 5. Execute uvicorn via the absolute python binary path we discovered
CMD ["sh", "-c", ". /etc/profile && $REAL_PYTHON -m uvicorn main:app --host 0.0.0.0 --port $PORT"]
