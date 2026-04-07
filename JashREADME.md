Hello, this is Jasher and this is where the Cryptography part for my Info Assurance

Sir San Andres will grade me solely for my Info Assurance Final Project and you guys are not part of it because of complications via being an irregular student and me already completing my Web System 2 Subject

# Cryptography Module for BantayKalusugan

## Platform Compatibility

> [!IMPORTANT]
> **Development Environment**: This module was developed and tested on Arch Linux.
> Since it's written in Python using cross-platform cryptographic libraries 
> (bcrypt, PyJWT, cryptography), it should work on:
> - ✅ Linux (primary development platform)
> - ✅ macOS (Python libraries are compatible)
> - ✅ Windows (with minor considerations below)

### Windows-Specific Notes
- **File Permissions**: The code sets Unix permissions (0o750, 0o600) which are 
  ignored on Windows - no impact on functionality
- **Log Directory**: Will work normally on Windows, just without Unix permissions
- **Path Handling**: Uses `pathlib` for cross-platform path compatibility

## STRIDE Threat Model Implementation

This module implements security controls addressing each STRIDE threat:

| Threat | Implementation | Code Location |
|--------|---------------|---------------|
| **Spoofing** | Password hashing (bcrypt), JWT tokens with unique IDs | `hash_password()`, `generate_jwt_token()` |
| **Tampering** | Input sanitization, HMAC signatures, CSRF tokens | `sanitize_input()`, `generate_hmac()` |
| **Repudiation** | Tamper-evident audit logging with hash chains | `audit_log()`, `verify_log_integrity()` |
| **Info Disclosure** | Fernet encryption, data masking, secure defaults | `encrypt_sensitive_data()`, `mask_sensitive_data()` |
| **Denial of Service** | Rate limiting, request size validation, WAF simulation | `check_rate_limit()`, `waf_inspect_request()` |
| **Elevation of Privilege** | Role-based access control, permission hierarchy | `check_permission()`, `validate_role_transition()` |

## Integration with Backend

```python
from crypto_module import CryptographyManager

# Initialize once (environment variable recommended)
security = CryptographyManager(
    secret_key=os.getenv('SECRET_KEY', 'fallback-for-dev-only'),
    app_name="BantayKalusugan"
)

# Example: User registration route
@app.route('/api/register', methods=['POST'])
def register():
    # Rate limiting
    allowed, headers = security.check_rate_limit(request.remote_addr)
    if not allowed:
        return {"error": "Too many requests"}, 429, headers
    
    # Input sanitization
    email = security.sanitize_input(request.json['email'], context='email')
    if not email:
        return {"error": "Invalid email"}, 400
    
    # Password hashing
    password_hash = security.hash_password(request.json['password'])
    
    # Audit log
    security.audit_log("SYSTEM", "REGISTRATION_ATTEMPT", {"email": email})
    
    return {"status": "success"}
