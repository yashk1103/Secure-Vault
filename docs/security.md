# Security Architecture

## Overview

Multi-layered security implementation for secure credential storage.

## Security Features

### Authentication
- **bcrypt hashing**: Salt-based password hashing
- **Session tokens**: Secure token-based authentication
- **Input validation**: Server-side request validation

### Encryption
- **AES-256**: Fernet symmetric encryption
- **PBKDF2**: 100,000 iterations for key derivation
- **Master keys**: Password-derived encryption keys

### Database Security
- **Prepared statements**: SQL injection prevention
- **Foreign keys**: Data integrity constraints
- **Indexes**: Performance optimization
- **Encrypted storage**: All sensitive data encrypted

## Cryptographic Flow

1. User password → bcrypt hash (stored)
2. User password + salt → PBKDF2 → key derivation key
3. Master key + key derivation key → encrypted master key (stored)
4. Vault data + master key → encrypted vault data (stored)

## Security Controls

### Data Protection
- No plaintext password storage
- Encrypted sensitive data at rest
- Master keys cleared on logout
- Secure session management

### Attack Mitigation
- Rainbow table attacks (salted hashes)
- Brute force attacks (bcrypt complexity)
- SQL injection (prepared statements)
- Data breaches (encrypted storage)

## Production Security

For production deployment:
- HTTPS/TLS for all communications
- Rate limiting on authentication endpoints
- Security headers (CSP, HSTS, etc.)
- Regular security audits
- Proper logging and monitoring

### Assumptions
- Secure execution environment
- PostgreSQL server security
- User follows security best practices
- No malware on execution system

## Best Practices Implemented

1. **Defense in Depth**: Multiple security layers
2. **Least Privilege**: Minimal database permissions
3. **Secure Defaults**: Strong cryptographic parameters
4. **Input Validation**: All user inputs sanitized
5. **Error Handling**: No sensitive information in error messages
