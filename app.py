# Use this as a building block for app.py. For my Cryptography
from cryptography import CryptographyManager

# Initialize once (use environment variable for secret key!)
security = CryptographyManager(secret_key=os.environ.get('SECRET_KEY'))

# SPOOFING: Hash passwords before storing
hashed_password = security.hash_password(user_password)

# SPOOFING: Verify login
if security.verify_password(input_password, stored_hash):
    token = security.generate_jwt_token(user_id, user_role)

# TAMPERING: Verify request integrity
if not security.verify_hmac(request_data, provided_signature):
    return "Data tampered with!", 400

# REPUDIATION: Log everything
security.audit_log(user_id, "USER_ACTION", {"details": "what they did"})

# INFO DISCLOSURE: Encrypt sensitive data
encrypted_ssn = security.encrypt_sensitive_data(user_ssn)

# DOS: Check request sizes
if not security.validate_request_size(request.json):
    return "Request too large", 413

# ELEVATION: Check permissions
if not security.check_permission(user_role, "admin"):
    return "Unauthorized", 403
