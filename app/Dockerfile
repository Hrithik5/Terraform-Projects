FROM python:3.9-slim

WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files
COPY templates/ templates/
COPY static/ static/
COPY app.py .
COPY .env .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 8000

CMD ["python", "app.py"]