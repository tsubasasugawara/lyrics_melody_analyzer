FROM python:latest

RUN apt update

ARG USERNAME=user
ARG GROUPNAME=user
ARG UID=1000
ARG GID=1000
ARG WORKDIR=/jupyter

ENV PYTHONPATH $WORKDIR

RUN groupadd -g $GID $GROUPNAME && \
	useradd -m -s /bin/bash -u $UID -g $GID $USERNAME

RUN mkdir -p $WORKDIR
RUN chown -R $UID:$GID $WORKDIR

ENV PATH /home/$USERNAME/.local/bin:$PATH

USER $USERNAME

COPY . $WORKDIR
WORKDIR $WORKDIR/src

RUN pip install --upgrade --user pip
RUN pip install --upgrade --user setuptools

RUN pip install --user -r ../requirements.txt

EXPOSE 8888
