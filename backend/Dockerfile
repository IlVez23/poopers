# Dockerfile (in ./backend/)
FROM python:3.10-slim

# Use /app as the working directory
WORKDIR /app

# Copy requirements.txt from the build context (./backend) to /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code from build context (./backend) to /app
# This step is technically optional when using a volume mount for development,
# but it's good practice for creating standalone images later.
COPY . .
RUN chmod -R 755 /app  # Set read, write, and execute for owner, read and execute for others
# This CMD will now run inside /app, where main.py is located (due to the volume mount)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
