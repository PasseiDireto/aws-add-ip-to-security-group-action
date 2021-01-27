FROM python:3.9-alpine AS builder

COPY requirements/run.txt /action_workspace/run.txt

ENV TERM "xterm-256color"
RUN pip install -r /action_workspace/run.txt

COPY . /action_workspace
RUN chmod +x /action_workspace/cleanup.sh
ENV PYTHONPATH /action_workspace

ENTRYPOINT ["python", "/action_workspace/action/start.py"]

