FROM ubuntu:18.04

RUN apt-get update

RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev python3-pip

# Expose port
EXPOSE 5000

# Copy code and
COPY . .

# Install deps
RUN pip3 install -r requirements.txt

#Install pipenv
RUN pip install pipenv

CMD ["python3", "manage.py", "run" ]


