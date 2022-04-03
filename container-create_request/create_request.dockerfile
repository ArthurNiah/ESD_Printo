FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./invokes.py ./request.py ./google_maps.py ./master_file.py ./
COPY ./package.json ./package-lock.json ./create_request.py ./
COPY ./container-gdrive/app.js ./
CMD [ "python", "./create_request.py" ]
