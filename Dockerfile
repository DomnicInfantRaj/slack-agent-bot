FROM python:3.10-bookworm 

WORKDIR /app
 
COPY . . 

RUN pip install keyring keyrings.google-artifactregistry-auth

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#CMD ["python3","./app.py"]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app