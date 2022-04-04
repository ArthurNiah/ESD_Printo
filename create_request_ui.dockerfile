# Set the base image.
FROM node

# Create and define the working directory.
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Install the application's dependencies.
COPY package.json ./
COPY package-lock.json ./
COPY create_request_ui.js ./
# COPY temp_files/ /usr/src/app/temp_files
COPY temp_files/ ./

RUN npm install
CMD [ "node", "./create_request_ui.js" ]