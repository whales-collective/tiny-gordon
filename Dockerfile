# Build the MCP Server
FROM golang:1.24.0-alpine AS builder
WORKDIR /app

COPY . .
RUN <<EOF
cd talk-to-moby
go mod tidy 
go build
EOF

RUN <<EOF
cd similarity-search
go mod tidy 
go build
EOF



FROM python:3.10.12-slim

WORKDIR /app

COPY --from=builder /app/talk-to-moby/talk-to-moby ./mcp-talk-to-moby
COPY --from=builder /app/similarity-search/similarity-search ./mcp-similarity-search
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

COPY /tiny-gordon ./tiny-gordon 

EXPOSE 8000

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]