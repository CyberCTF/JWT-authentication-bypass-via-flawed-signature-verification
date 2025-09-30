# JWT Authentication Bypass via Flawed Signature Verification# JWT Authentication Bypass via Flawed Signature Verification# 🔐 JWT Authentication Bypass Challenge

Docker Flask Python

**Docker | Flask | Python**

Difficulty: APPRENTICE | Category: Authentication | Estimated Time: 15-30 minutes

## 📋 Overview

## Challenge Overview

This lab demonstrates a critical vulnerability in a corporate asset management system where JWT authentication can be bypassed through the acceptance of the 'none' algorithm. The application accepts unsigned JWT tokens, allowing attackers to forge administrator privileges and access sensitive corporate data.**Difficulty:** 🟡 **APPRENTICE** | **Category:** Authentication | **Estimated Time:** 15-30 minutes



## Quick StartA professional security challenge demonstrating JWT (JSON Web Token) authentication bypass vulnerabilities. This challenge simulates a **Corporate Asset Management System** with a critical security flaw that allows attackers to escalate privileges to administrator level.



### Using Docker## 🎯 Challenge Overview

```bash

docker pull cyberctf/jwt-authentication-bypass:latestThis lab demonstrates a critical vulnerability in a corporate asset management system where JWT authentication can be bypassed through the acceptance of the 'none' algorithm. The application accepts unsigned JWT tokens, allowing attackers to forge administrator privileges and access sensitive corporate data.## � Challenge Details

docker run -d -p 3206:3206 cyberctf/jwt-authentication-bypass:latest

```



### Using Docker Compose## 🚀 Quick Start- **Vulnerability**: JWT 'none' algorithm acceptance bypass

```bash

docker-compose up -d- **Difficulty**: Apprentice  

```

### Using Docker- **Category**: Web Security

Access: http://localhost:3206/

```bash- **Framework**: Flask + Python 3.11

## Learning Objectives

- Understand JWT structure and security mechanismsdocker pull cyberctf/jwt-authentication-bypass:latest- **Database**: SQLite

- Identify JWT 'none' algorithm acceptance vulnerabilities

- Forge malicious JWT tokens to bypass authenticationdocker run -d -p 3206:3206 cyberctf/jwt-authentication-bypass:latest- **Port**: 3206

- Escalate privileges to administrator level

- Access sensitive corporate data and system controls```



## Prerequisites## 🚀 Quick Start

- Basic understanding of JWT tokens and web authentication

- Familiarity with Burp Suite or similar tools### Using Docker Compose

- Knowledge of base64 encoding/decoding

- Understanding of HTTP cookies and session management```bash### Prerequisites



## Tools Recommendeddocker-compose up -d- Docker & Docker Compose

- Burp Suite Community/Professional

- Web browser with developer tools```- Python 3.11+ (for local development)

- JWT debugger (jwt.io)

- Base64 decoder/encoder- Web Browser

- Python for custom scripts

**Access:** http://localhost:3206/

## Default Credentials

- Employee Account: `mitchell.parker` / `corporate2024`### Production Deployment

- Finance Account: `sarah.johnson` / `finance789`

- Target: Bypass authentication to access admin panel without credentials## 📚 Learning Objectives```bash



## Challenge Objectives✅ Understand JWT structure and security mechanisms  # Clone and deploy

1. Reconnaissance - Analyze the JWT implementation and structure

2. Vulnerability Discovery - Identify the 'none' algorithm acceptance flaw✅ Identify JWT 'none' algorithm acceptance vulnerabilities  git clone <repository-url>

3. Token Forgery - Create a malicious JWT with administrator privileges

4. Privilege Escalation - Access the administrator panel✅ Forge malicious JWT tokens to bypass authentication  cd jwt-auth-bypass-challenge

5. Impact Demonstration - Extract sensitive data and system information

✅ Escalate privileges to administrator level  

## Success Criteria

- Access the Administrator Panel at `/admin`✅ Access sensitive corporate data and system controls  # Start the challenge

- View sensitive personal information of employees

- Demonstrate user management capabilitiesdocker-compose up -d

- Document the complete attack chain

## 🛠️ Prerequisites

## CyberCTF - Cybersecurity Training Platform

- Basic understanding of JWT tokens and web authentication# Access the application

This challenge is part of CyberCTF's comprehensive cybersecurity training program designed to teach real-world attack techniques in a safe, controlled environment.
- Familiarity with Burp Suite or similar toolsopen http://localhost:3206

- Knowledge of base64 encoding/decoding```

- Understanding of HTTP cookies and session management

### Development Environment

## 🔧 Tools Recommended```bash

- **Burp Suite** Community/Professional# For development with hot-reload

- **Web browser** with developer toolscd build/deploy

- **JWT debugger** (jwt.io)docker-compose -f docker-compose.dev.yml up

- **Base64 decoder/encoder**```

- **Python** for custom scripts

## 🎯 Challenge Objectives

## 🔐 Default Credentials

- **Employee Account**: `mitchell.parker` / `corporate2024`1. **🔍 Reconnaissance** - Analyze the JWT implementation

- **Finance Account**: `sarah.johnson` / `finance789`2. **🔓 Vulnerability Discovery** - Identify the 'none' algorithm acceptance

- **Target**: Bypass authentication to access admin panel without credentials3. **🛠️ Exploitation** - Forge a malicious JWT token

4. **⚡ Privilege Escalation** - Gain administrator access

## 🎯 Challenge Objectives5. **💥 Impact Demonstration** - Access sensitive data and system controls

1. **🔍 Reconnaissance** - Analyze the JWT implementation and structure

2. **🔓 Vulnerability Discovery** - Identify the 'none' algorithm acceptance flaw## 🔐 Default Credentials

3. **🛠️ Token Forgery** - Create a malicious JWT with administrator privileges

4. **⚡ Privilege Escalation** - Access the administrator panel- **Employee Account**: `mitchell.parker` / `corporate2024`

5. **💥 Impact Demonstration** - Extract sensitive data and system information- **Finance Account**: `sarah.johnson` / `finance789`  

- **Target**: Bypass authentication to access admin panel without credentials

## 🏆 Success Criteria

✅ Access the Administrator Panel at `/admin`  ## 🏆 Success Criteria

✅ View sensitive personal information of employees  

✅ Demonstrate user management capabilities  ✅ Access the Administrator Panel at `/admin`  

✅ Document the complete attack chain  ✅ View sensitive personal information  

✅ Demonstrate system administration capabilities  

## 🎓 CyberCTF - Cybersecurity Training Platform✅ Document the complete attack chain  



---## 🛡️ Learning Outcomes

*This challenge is part of CyberCTF's comprehensive cybersecurity training program designed to teach real-world attack techniques in a safe, controlled environment.*
- Understanding JWT structure and vulnerabilities
- Identifying authentication bypass techniques
- Exploiting 'none' algorithm acceptance flaws
- Demonstrating real-world impact of security vulnerabilities
- Security testing with industry-standard tools

## 📁 Project Structure

```
├── docker-compose.yml              # Production deployment
├── README.md                       # Main documentation
├── RULES.md                        # Project rules and conventions
├── .gitignore                      # Git ignore rules
├── .github/workflows/              # CI/CD automation
├── build/
│   ├── app/                        # Application code
│   │   ├── Dockerfile              # Container definition
│   │   ├── app.py                  # Main application
│   │   ├── requirements.txt        # Python dependencies
│   │   ├── templates/              # HTML templates
│   │   └── tests/main.py           # Test suite
│   └── deploy/
│       ├── README.md               # Deployment guide
│       └── docker-compose.dev.yml # Development environment
└── challenges/                     # Challenge-specific files
```

## 🧪 Testing

Run the complete test suite:
```bash
python build/app/tests/main.py
```

The test suite validates:
- Application startup and accessibility
- Authentication mechanisms
- JWT vulnerability presence
- Sensitive data exposure
- Administrative function access

## �️ Security Notice

**⚠️ IMPORTANT**: This application contains **intentional security vulnerabilities** for educational purposes. 

- **DO NOT** deploy in production environments
- **USE ONLY** in controlled, isolated environments
- **INTENDED FOR** security training and penetration testing practice
- **FOLLOW** responsible disclosure practices

## � Documentation

- **Main Documentation**: This README
- **Deployment Guide**: `build/deploy/README.md`
- **Challenge Rules**: `RULES.md`
- **Technical Details**: See `challenges/` directory

## 🤝 Contributing

This challenge follows professional development standards:
- All code in `build/app/`
- Single Dockerfile and requirements.txt
- Comprehensive test coverage
- CI/CD automation
- Security-focused documentation

## 📄 License

Educational use only. See LICENSE file for details.

---

**🎓 Part of CyberCTF Security Training Platform**  
*Building the next generation of cybersecurity professionals*
