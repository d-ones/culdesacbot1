FROM python:3.10.5-alpine3.15

WORKDIR /app

COPY bot.py . creds.py . shufflecoords.csv . used.txt . requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./bot.py"]