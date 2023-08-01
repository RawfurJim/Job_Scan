FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app


# FROM python:3.8
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# EXPOSE 6000
# CMD python ./app.py


