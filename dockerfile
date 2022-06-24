FROM python:3.9.13-slim

COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py"]