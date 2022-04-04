FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
COPY ./invokes.py ./accept_request.py ./provider.py ./payment.py ./request.py ./notification.py ./request.py ./amqp_setup.py ./
CMD [ "python", "./accept_request.py"]
#CMD [ "python", "./accept_request.py", "invokes.py" ]
