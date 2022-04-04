FROM python:3-slim
WORKDIR /usr/src/app
COPY invokes.py ./view_requests.py ./
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./view_requests.py", "./invokes.py" ]
