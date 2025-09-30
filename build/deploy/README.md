# JWT Authentication Bypass via Flawed Signature Verification# 🚀 Deployment Guide



Docker image for a cybersecurity training challenge demonstrating JWT authentication bypass vulnerabilities.## Overview



## Quick StartThis guide covers deployment and development setup for the JWT Authentication Bypass Challenge.



```bash## 🐳 Production Deployment

docker run -d -p 3206:3206 cyberctf/jwt-authentication-bypass:latest

```### Quick Start

```bash

**Access:** http://localhost:3206/# From repository root

docker-compose up -d

## Challenge Description

# Verify deployment

This challenge simulates a corporate asset management system with a critical JWT vulnerability. The application incorrectly accepts JWT tokens with the 'none' algorithm, allowing complete authentication bypass.curl http://localhost:3206

```

## Learning Objectives

### Environment Configuration

- Understand JWT security mechanismsThe production deployment uses:

- Identify 'none' algorithm vulnerabilities- **Image**: `cyberctf/jwt-auth-bypass:latest`

- Practice authentication bypass techniques- **Port**: 3206

- Learn privilege escalation methods- **Environment**: Production

- **Persistence**: Docker volume for database

## Default Credentials

### Health Checks

- Employee: `mitchell.parker` / `corporate2024`The application includes health checks that verify:

- Finance: `sarah.johnson` / `finance789`- HTTP endpoint accessibility

- Application responsiveness

## Target- Container health status



Bypass authentication to access the administrator panel without valid credentials.## 🛠️ Development Environment



## Requirements### Setup

```bash

- Dockercd build/deploy

- Web browserdocker-compose -f docker-compose.dev.yml up

- Basic understanding of JWT tokens```



**Difficulty:** Apprentice | **Category:** Authentication | **Time:** 15-30 minutes### Development Features

- **Hot Reload**: Code changes reflected immediately

---- **Debug Mode**: Enhanced error reporting

- **Volume Mounting**: Live code editing

**CyberCTF - Cybersecurity Training Platform**- **Development Environment Variables**

### Local Development (No Docker)
```bash
cd build/app
pip install -r requirements.txt
python app.py
```

## 🧪 Testing

### Running Tests
```bash
# Ensure application is running
docker-compose up -d

# Run test suite
python build/app/tests/main.py
```

### Test Coverage
The test suite covers:
- ✅ Application startup and health
- ✅ Authentication mechanisms  
- ✅ JWT vulnerability verification
- ✅ Privilege escalation testing
- ✅ Sensitive data exposure validation
- ✅ Administrative function access

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: `production` or `development`
- `FLASK_DEBUG`: `0` or `1`
- `FLASK_APP`: `app.py`
- `PYTHONPATH`: `/app`

### Ports and Networking
- **Application Port**: 3206
- **Container Internal**: 3206
- **Health Check**: HTTP GET /

### Data Persistence
- **Production**: Named volume `jwt_challenge_data`
- **Development**: Named volume `jwt_dev_data`
- **Database**: SQLite in `/app/data/`

## 🐛 Troubleshooting

### Common Issues

**Application not starting:**
```bash
# Check container logs
docker-compose logs jwt-challenge-app

# Verify port availability
netstat -tulpn | grep 3206
```

**Database issues:**
```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

**Permission issues:**
```bash
# Fix file permissions (Linux/Mac)
sudo chown -R $USER:$USER .
chmod -R 755 build/app/
```

### Debug Mode
Enable debug mode for detailed error information:
```bash
# Development environment (debug enabled by default)
cd build/deploy
docker-compose -f docker-compose.dev.yml up
```

## 📊 Monitoring

### Health Check Endpoint
```bash
curl http://localhost:3206/
```

### Application Logs
```bash
# View real-time logs
docker-compose logs -f jwt-challenge-app

# View last 50 lines
docker-compose logs --tail=50 jwt-challenge-app
```

### Container Status
```bash
# Check container health
docker-compose ps

# Container resource usage
docker stats jwt-challenge-app
```

## 🔒 Security Considerations

### Development Environment
- **Isolation**: Use only in isolated environments
- **Network**: Bind to localhost only in production
- **Secrets**: No hardcoded secrets in production

### Challenge Security
- ⚠️ **Intentional Vulnerabilities**: Do not deploy on public networks
- 🔒 **Educational Use**: For training purposes only
- 🏠 **Local Development**: Recommended deployment approach

## 📋 Deployment Checklist

### Pre-deployment
- [ ] Docker and Docker Compose installed
- [ ] Port 3206 available
- [ ] Sufficient disk space (100MB+)
- [ ] Network connectivity

### Post-deployment
- [ ] Application accessible at http://localhost:3206
- [ ] Login page loads correctly
- [ ] Health check passing
- [ ] Test suite execution successful

### Validation
- [ ] Normal authentication works
- [ ] JWT bypass vulnerability present
- [ ] Admin panel accessible via exploit
- [ ] Sensitive data exposure confirmed

## 🎯 Development Workflow

1. **Code Changes**: Edit files in `build/app/`
2. **Testing**: Run `python build/app/tests/main.py`
3. **Development**: Use `docker-compose.dev.yml` for live reload
4. **Production Test**: Use root `docker-compose.yml`
5. **Validation**: Verify challenge functionality

---

**🔧 For technical support or questions about deployment, consult the main project documentation.**