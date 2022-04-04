FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./invokes.py ./tele_setup.py ./api.py ./ 
CMD [ "python", "./tele_setup.py" ]
