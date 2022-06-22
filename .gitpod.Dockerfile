FROM gitpod/workspace-full

USER gitpod

RUN python3 -m pip install -r https://gitlab.com/<aecollier>/<portfolio>/-/raw/master/requirements.txt