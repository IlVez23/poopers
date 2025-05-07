FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the API_URL environment variable
ENV API_URL=https://poopers-backend.onrender.com

# Add a startup script to verify environment variables
RUN echo '#!/bin/bash\necho "API_URL is set to: $API_URL"\nstreamlit run home.py --server.port=8501 --server.address=0.0.0.0' > /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
