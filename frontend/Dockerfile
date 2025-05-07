FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the default API_URL (will be overridden by environment variable if set)
ENV API_URL=https://poopers-backend.onrender.com

CMD ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]
