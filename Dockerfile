# Use Python 3.10 (Rasa 3.6 only supports up to Python 3.10)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Train the Rasa model
RUN rasa train

# Expose Rasa port
EXPOSE 8080

# Start Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "8080"]
