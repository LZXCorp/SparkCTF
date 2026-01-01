FROM ubuntu:24.04

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update \
    && apt-get install -y \
    python3 python3-pip \
    cowsay \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv --break-system-packages

COPY sparkmcp.py /root/sparkmcp.py
COPY sparkdb_setup.py /root/sparkdb_setup.py

RUN uv run /root/sparkdb_setup.py

EXPOSE 6080

CMD ["uv", "run", "--with", "fastmcp==2.11.3,pytz", "/root/sparkmcp.py"]