# Set the base image.
FROM node

# Create and define the working directory.
RUN mkdir /usr/src/app2
WORKDIR /usr/src/app2

# Install the application's dependencies.
COPY package.json ./
COPY package-lock.json ./
COPY app2.js ./
COPY temp_files/ /usr/src/app/temp_files
COPY container-ui/ /usr/src/app/container-ui

RUN npm install
CMD [ "node", "./app2.js" ]