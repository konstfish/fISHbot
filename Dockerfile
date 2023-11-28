
FROM golang:1.21-alpine as builder

WORKDIR /app

# required for sql
RUN apk add --no-cache gcc musl-dev

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN CGO_ENABLED=1 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest  

RUN apk --no-cache add ca-certificates

WORKDIR /

RUN mkdir -p db

COPY --from=builder /app/main .

CMD ["./main"]