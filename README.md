# 🔐 JWT Authentication Bypass Challenge

## 📋 Overview

A professional security challenge demonstrating JWT (JSON Web Token) authentication bypass vulnerabilities. This challenge simulates a **Corporate Asset Management System** with a critical security flaw that allows attackers to escalate privileges to administrator level.

## � Challenge Details

- **Vulnerability**: JWT 'none' algorithm acceptance bypass
- **Difficulty**: Apprentice  
- **Category**: Web Security
- **Framework**: Flask + Python 3.11
- **Database**: SQLite
- **Port**: 3206

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Web Browser

### Production Deployment
```bash
# Clone and deploy
git clone <repository-url>
cd jwt-auth-bypass-challenge

# Start the challenge
docker-compose up -d

# Access the application
open http://localhost:3206
```

### Development Environment
```bash
# For development with hot-reload
cd build/deploy
docker-compose -f docker-compose.dev.yml up
```

## 🎯 Challenge Objectives

1. **🔍 Reconnaissance** - Analyze the JWT implementation
2. **🔓 Vulnerability Discovery** - Identify the 'none' algorithm acceptance
3. **🛠️ Exploitation** - Forge a malicious JWT token
4. **⚡ Privilege Escalation** - Gain administrator access
5. **💥 Impact Demonstration** - Access sensitive data and system controls

## 🔐 Default Credentials

- **Employee Account**: `mitchell.parker` / `corporate2024`
- **Finance Account**: `sarah.johnson` / `finance789`  
- **Target**: Bypass authentication to access admin panel without credentials

## 🏆 Success Criteria

✅ Access the Administrator Panel at `/admin`  
✅ View sensitive personal information  
✅ Demonstrate system administration capabilities  
✅ Document the complete attack chain  

## 🛡️ Learning Outcomes

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
