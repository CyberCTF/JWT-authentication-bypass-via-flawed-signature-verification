# JWT Authentication Bypass via Flawed Signature Verification

##Scenario
Vulnerability lab demonstrating a critical flaw in an employee management portal authentication system. The application reveals different error messages for valid vs invalid usernames, allowing attackers to enumerate valid accounts and subsequently brute force passwords.

##How to run
```bash
git clone https://github.com/CyberCTF/JWT-authentication-bypass-via-flawed-signature-verification.git
cd JWT-authentication-bypass-via-flawed-signature-verification
docker compose -f build/deploy/docker-compose.dev.yml up -d --build
Access: http://localhost:3206
```