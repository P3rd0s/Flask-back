FROM python:3.9.16-slim-bullseye

WORKDIR /usr/src/app/FlaskBack

COPY requirements.txt /usr/src/app/FlaskBack
RUN pip install -r /usr/src/app/FlaskBack/requirements.txt
COPY . /usr/src/app/FlaskBack

EXPOSE 5000
CMD ["python3", "app.py"]