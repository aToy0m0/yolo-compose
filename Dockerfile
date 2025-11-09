FROM quay.io/jupyter/base-notebook:latest

USER root

# Install JupyterHub stack + DockerSpawner with configurable-http-proxy
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip nodejs npm && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir jupyterhub jupyterlab dockerspawner jupyterhub-nativeauthenticator docker psycopg2-binary && \
    npm install -g configurable-http-proxy && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add bundled JupyterHub config & templates
RUN mkdir -p /srv/jupyterhub /srv/jupyterhub/templates /srv/jupyterhub_data
COPY yolo-compose/jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY yolo-compose/templates/ /srv/jupyterhub/templates/
RUN chown -R jovyan:users /srv/jupyterhub /srv/jupyterhub_data

USER jovyan

WORKDIR /srv/jupyterhub

EXPOSE 8000

CMD ["bash", "-c", "jupyterhub -f /srv/jupyterhub/jupyterhub_config.py"]
