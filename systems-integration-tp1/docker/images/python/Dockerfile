FROM python:3.9.18-alpine

WORKDIR /app

# install nodemon
RUN apk add nodejs npm
RUN npm install -g npm@10.2.1
RUN npm install -g nodemon

# upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies for lxml
RUN apk add --no-cache libxml2-dev libxslt-dev gcc musl-dev

# dependencies from requirements.txt
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Add lxml to your requirements.txt or install it here
RUN pip install lxml

RUN mkdir /data

ENTRYPOINT python main.py