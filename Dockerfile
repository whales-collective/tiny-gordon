FROM python:3.10.12-slim

WORKDIR /app

# ------------------------------------
# Install Socat to use MCP Toolkit
# ------------------------------------
RUN <<EOF
apt-get update
apt-get install -y socat
apt-get clean
rm -rf /var/lib/apt/lists/*
EOF

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]