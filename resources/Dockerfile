FROM python:3.11 AS builder

RUN pip install --user pipenv

RUN useradd -ms /bin/bash cleanup

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile.lock Pipfile /home/cleanup/

WORKDIR /home/cleanup
RUN /root/.local/bin/pipenv sync

FROM python:3.11 AS runtime

RUN useradd -ms /bin/bash cleanup

COPY --from=builder /home/cleanup/.venv /home/cleanup/.venv

WORKDIR /home/cleanup
RUN mkdir ./cleanup

COPY scripts/*.py  resources/start.sh ./

RUN chmod +x start.sh


USER cleanup

ENTRYPOINT ["./start.sh"]