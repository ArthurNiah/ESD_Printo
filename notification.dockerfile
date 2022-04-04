FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt amqp.reqs.txt
COPY ./invokes.py ./notification.py ./api.py ./amqp_setup.py ./ 
CMD [ "python", "./notification.py" ]
