# JWT Authentication Bypass via Flawed Signature Verification

## Scenario
Vulnerability lab demonstrating a critical JWT authentication bypass flaw where the application accepts the "none" algorithm. This allows attackers to forge JWT tokens without any signature verification, bypassing authentication and gaining unauthorized access to sensitive corporate data.

## How to run
```bash
git clone https://github.com/CyberCTF/JWT-authentication-bypass-via-flawed-signature-verification.git
cd JWT-authentication-bypass-via-flawed-signature-verification
docker compose -f build/deploy/docker-compose.dev.yml up -d --build
```

**Access:** http://localhost:3206