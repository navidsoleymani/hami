FROM python:3.12

RUN apt-get update
RUN apt-get install -y gettext
# disable writing pyc and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Application work dir
WORKDIR /app
COPY ./requirements.txt .

# caching pip packages
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip \
    pip install -r requirements.txt

COPY . /app
RUN cp SAMPLE_ENV.txt .env

EXPOSE 8000

