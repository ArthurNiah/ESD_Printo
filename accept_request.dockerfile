FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt 
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt
#COPY ./accept_request.py ./invokes.py ./amqp_setup.py ./
COPY ./invokes.py ./accept_request.py ./provider.py ./payment.py ./request.py ./notification.py ./request.py ./amqp_setup.py ./
CMD [ "python", "./accept_request.py"]
#CMD [ "python", "./accept_request.py", "invokes.py" ]
