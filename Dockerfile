FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /code

# Copy and install Python requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN playwright install --with-deps

# Copy the rest of your application code
COPY . .

CMD ["sh", "-c", "python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT"]
