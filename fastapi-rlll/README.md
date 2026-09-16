# projectPulse

## Setup

### JWT keys

The app signs access tokens with an RS256 keypair read from `certs/`. This directory is gitignored (private keys must never be committed), so it needs to be generated locally before the app or tests will start:

```bash
mkdir -p certs
openssl genrsa -out certs/jwt-private.pem 2048
openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```
