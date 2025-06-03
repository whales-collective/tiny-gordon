FROM golang:1.24.3-alpine AS builder

WORKDIR /app
COPY main.go .
COPY go.mod .

RUN <<EOF
go mod tidy 
go build -o data-loader
EOF

FROM scratch
WORKDIR /app
COPY docs docs
COPY --from=builder /app/data-loader .

CMD ["./data-loader"]