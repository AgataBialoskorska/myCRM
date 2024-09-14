FROM docker.io/python:3.11

ENV SQLALCHEMY_CONFIG='mysql://USER:PASSWORD@DATABASE_URI/DATABASE_NAME'

ADD . .

WORKDIR /

RUN apt-get update && apt-get install -y \
    npm
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt
RUN npm install

EXPOSE 8080

CMD ["npm", "run", "my-crm"]