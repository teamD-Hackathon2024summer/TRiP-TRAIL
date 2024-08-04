FROM python:3.9

WORKDIR /home/appuser/devcon

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
