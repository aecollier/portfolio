FROM gitpod/workspace-full

USER gitpod

RUN python3 -m pip install -r https://github.com/aecollier/portfolio/blob/main/requirements.txt
