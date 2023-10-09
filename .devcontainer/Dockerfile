FROM mcr.microsoft.com/devcontainers/typescript-node:1-18-bookworm

# Script copies localhost's ~/.kube/config file into the container and swaps out 
# localhost for kubernetes.default.svc then host.docker.internal on bash/zsh start to keep them in sync.
USER root
COPY --chown=node:node --chmod=777 copy-kube-config.sh /usr/local/share/
RUN echo "source /usr/local/share/copy-kube-config.sh" | tee -a /root/.bashrc /root/.zshrc /home/node/.bashrc >> /home/node/.zshrc \
     && echo "alias k=kubectl" | tee -a /root/.bashrc /root/.zshrc /home/node/.bashrc >> /home/node/.zshrc 

USER node