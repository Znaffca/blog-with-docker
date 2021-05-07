# pulling the official base image
FROM python:3.8-alpine

# setting up the workdir directory
WORKDIR /usr/src/blog

# set basic environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy whole project
COPY . .

# run the entrypoint script to create a basic migrations after postgres will be available
ENTRYPOINT [ "/usr/src/blog/docker-entrypoint.sh" ]