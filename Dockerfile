# Use the official Playwright Python image which comes pre-configured with all system dependencies
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy
WORKDIR /code

# Copy and install Python requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 10000

# Start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
