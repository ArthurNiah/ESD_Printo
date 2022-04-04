FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./invokes.py ./accept_request.py ./provider.py ./payment.py ./request.py ./notification.py ./request.py ./
COPY ./app.js ./
CMD [ "python", "./accept_request.py"]
#CMD [ "python", "./accept_request.py", "invokes.py" ]
