# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .
EXPOSE 5444
ENV FLASK_APP=app.py
# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .
# command to run on container start
#CMD [ "python", "./app.py" ]

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5444"]