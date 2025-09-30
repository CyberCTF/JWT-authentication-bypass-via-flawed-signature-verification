# JWT Authentication Bypass via Flawed Signature Verification
Docker Flask Python

Difficulty: APPRENTICE | Category: Authentication | Estimated Time: 15-30 minutes

## Challenge Overview
This lab demonstrates a vulnerability in a corporate asset management system where JWT authentication can be bypassed through the acceptance of the none algorithm. The application accepts unsigned JWT tokens, allowing attackers to forge administrator privileges and access sensitive corporate data.

## Quick Start
### Using Docker
```bash
docker pull cyberctf/jwt-authentication-bypass:latest
docker run -d -p 3206:3206 cyberctf/jwt-authentication-bypass:latest
```
### Using Docker Compose
```bash
docker-compose up -d
```
Access: http://localhost:3206/

## Learning Objectives
- Understand JWT structure and security mechanisms
- Identify JWT none algorithm acceptance vulnerabilities
- Forge malicious JWT tokens to bypass authentication
- Escalate privileges to administrator level
- Access sensitive corporate data and system controls

## Prerequisites
- Basic understanding of JWT tokens and web authentication
- Familiarity with Burp Suite or similar tools
- Knowledge of base64 encoding/decoding
- Understanding of HTTP cookies and session management

## Tools Recommended
- Burp Suite Community/Professional
- Web browser with developer tools
- JWT debugger (jwt.io)
- Base64 decoder/encoder

## Default Credentials
- Employee Account: mitchell.parker / corporate2024
- Finance Account: sarah.johnson / finance789

## CyberCTF - Cybersecurity Training Platform
