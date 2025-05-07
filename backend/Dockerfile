# Dockerfile (in ./backend/)
FROM python:3.10-slim

# Use /app as the working directory
WORKDIR /app

# Copy requirements.txt from the build context (./backend) to /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code from build context (./backend) to /app
COPY . .
RUN chmod -R 755 /app  # Set read, write, and execute for owner, read and execute for others

# Create a startup script
RUN echo '#!/bin/bash\npython init_db.py\nuvicorn main:app --host 0.0.0.0 --port 8000' > /app/start.sh
RUN chmod +x /app/start.sh

# Use the startup script as the entrypoint
CMD ["/app/start.sh"]
