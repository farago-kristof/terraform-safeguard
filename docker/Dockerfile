ARG BASE_IMAGE

FROM ${BASE_IMAGE}

# Install dependencies
RUN apk add --no-cache curl unzip bash python3 py3-pip

# Install AWS CLI v2 using pip (more reliable on Alpine)
RUN pip3 install awscli --break-system-packages

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
