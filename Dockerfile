FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY . .
CMD ["python", "bot.py"]