FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y build-essential

RUN pip install --upgrade pip wheel setuptools

RUN pip install -r requirements.txt

RUN rasa train

EXPOSE 8080

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "8080"]
