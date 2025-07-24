FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better cache usage
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Install Gunicorn
RUN pip install gunicorn

# Run the application
CMD exec gunicorn --bind :$PORT main:app --workers 1 --threads 8 --timeout 0 