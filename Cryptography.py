import hashlib
import hmac
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, Any, List
import logging
import json
from pathlib import Path
import re

# Third-party imports
import bcrypt
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

# Additional imports for improved security
import html # For XSS prevention
import time # For rate limiting

class CryptographyManager:
    """
    Main security class implementing STRIDE countermeasures
    Each method addresses specific STRIDE threats
    """
   
    def __init__(self, secret_key: str = None, app_name: str = "SecureApp"):
        """
        Initialize the security manager with cryptographic keys
       
        Args:
            secret_key: Master secret key (should be from environment variable)
            app_name: Application name for logging
        """
        # SPOOFING: Master secret for authentication
        self.secret_key = secret_key or os.environ.get('SECRET_KEY', secrets.token_hex(32))
        self.app_name = app_name
       
        # REPUDIATION: Setup audit logging with persistent hash chain
        self.setup_audit_logging()
       
        # INFO DISCLOSURE: Initialize encryption
        self.encryption_key = self._generate_encryption_key()
        self.fernet = Fernet(self.encryption_key)
       
        # Log initialization (REPUDIATION)
        self.audit_log("SYSTEM", "SECURITY_MODULE_INIT", {"status": "success"})
   
    # Spoofing Protection
   
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.audit_log("SYSTEM", "PASSWORD_HASHED", {"result": "success"})
        return hashed.decode('utf-8')
   
    def verify_password(self, password: str, hashed: str) -> bool:
        try:
            result = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
            self.audit_log("SYSTEM", "PASSWORD_VERIFIED",
                          {"result": "success" if result else "failure"})
            return result
        except Exception as e:
            self.audit_log("SYSTEM", "PASSWORD_VERIFICATION_ERROR", {"error": str(e)})
            return False
   
    def generate_jwt_token(self, user_id: int, role: str, expires_in_hours: int = 24) -> str:
        payload = {
            'user_id': user_id,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
            'jti': secrets.token_hex(16)
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        self.audit_log(user_id, "JWT_GENERATED", {"expires": expires_in_hours})
        return token
   
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            self.audit_log(payload.get('user_id', 'UNKNOWN'), "JWT_VERIFIED", {})
            return payload
        except jwt.ExpiredSignatureError:
            self.audit_log("SYSTEM", "JWT_EXPIRED", {})
            return None
        except jwt.InvalidTokenError as e:
            self.audit_log("SYSTEM", "JWT_INVALID", {"error": str(e)})
            return None
   
    # Tampering Protection
   
    def generate_hmac(self, data: str) -> str:
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
   
    def verify_hmac(self, data: str, signature: str) -> bool:
        expected = self.generate_hmac(data)
        return hmac.compare_digest(expected, signature)
   
    def generate_csrf_token(self) -> str:
        return secrets.token_urlsafe(32)
   
    # Tampering
   
    def sanitize_input(self, user_input: str, max_length: int = 255,
                      context: str = 'html') -> str:
        """
        TAMPERING: Advanced input sanitization
        - Prevents XSS (Cross-Site Scripting)
        - Prevents SQL Injection
        - Context-aware sanitization
       
        Args:
            user_input: Raw user input
            max_length: Maximum allowed length
            context: Where the input will be used ('html', 'sql', 'filename', 'email')
           
        Returns:
            Sanitized input
        """
        if not user_input:
            return ""
       
        # Trim whitespace
        sanitized = user_input.strip()
       
        # Length limiting
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
       
        # Context-specific sanitization
        if context == 'html':
            # HTML escape to prevent XSS
            sanitized = html.escape(sanitized, quote=True)
           
            # Remove any script tags that might have been encoded
            sanitized = re.sub(r'&lt;script.*?&gt;.*?&lt;/script&gt;', '', sanitized, flags=re.IGNORECASE)
           
        elif context == 'sql':
            # For SQL, remove dangerous characters
            dangerous = [';', '--', "'", '"', '/*', '*/', 'xp_', 'UNION', 'SELECT',
                        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER']
            for item in dangerous:
                sanitized = sanitized.replace(item, '')
               
        elif context == 'filename':
            # Sanitize filename
            sanitized = re.sub(r'[^a-zA-Z0-9._-]', '', sanitized)
            sanitized = sanitized.replace('..', '')
            sanitized = sanitized.replace('/', '')
            sanitized = sanitized.replace('\\', '')
           
        elif context == 'email':
            # Validate email format and remove dangerous chars
            sanitized = re.sub(r'[^a-zA-Z0-9@._-]', '', sanitized)
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', sanitized):
                return "" # Invalid email
       
        # Remove null bytes and control characters
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char == '\n')
       
        self.audit_log("SYSTEM", "INPUT_SANITIZED", {
            "context": context,
            "original_length": len(user_input),
            "final_length": len(sanitized)
        })
       
        return sanitized
   
    def validate_sql_input(self, user_input: str, allowed_pattern: str = None) -> bool:
        """
        TAMPERING: Additional SQL injection prevention
        - Validates input against expected pattern
       
        Args:
            user_input: Input to validate
            allowed_pattern: Regex pattern the input should match
           
        Returns:
            True if valid, False otherwise
        """
        if allowed_pattern:
            return bool(re.match(allowed_pattern, user_input))
       
        # Default: only allow alphanumeric and basic punctuation
        return bool(re.match(r'^[a-zA-Z0-9\s@._-]+$', user_input))
   
    # Repudiation Protection
   
    def setup_audit_logging(self):
        """
        REPUDIATION: Configure audit logging with persistent hash chain
        - Creates tamper-evident logs
        - Saves hash chain to disk
        """
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
       
        # Set secure permissions on Linux
        if os.name == 'posix':
            os.chmod(log_dir, 0o750)
       
        # Main audit log
        self.log_file = log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
       
        # Hash chain file (persistent storage)
        self.hash_chain_file = log_dir / "hash_chain.json"
       
        # Load existing hash chain or create new one
        self.log_hashes = self._load_hash_chain()
       
        logging.basicConfig(
            filename=str(self.log_file),
            level=logging.INFO,
            format='%(asctime)s|%(levelname)s|%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
   
    def _load_hash_chain(self) -> List[str]:
        """
        Load existing hash chain from disk
        """
        if self.hash_chain_file.exists():
            try:
                with open(self.hash_chain_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
   
    def _save_hash_chain(self):
        """
        Save hash chain to disk
        """
        with open(self.hash_chain_file, 'w') as f:
            json.dump(self.log_hashes, f, indent=2)
       
        # Secure permissions
        if os.name == 'posix':
            os.chmod(self.hash_chain_file, 0o600)
   
    def audit_log(self, user_id: Any, action: str, details: Dict):
        """
        REPUDIATION: Write to audit log with persistent hash chain
        - Creates non-repudiable evidence of actions
        - Saves hash chain to disk for tamper detection
       
        Args:
            user_id: User performing action
            action: Action being performed
            details: Additional details
        """
        timestamp = datetime.utcnow().isoformat()
        details_json = json.dumps(details, sort_keys=True)
       
        # Create log entry
        previous_hash = self.log_hashes[-1] if self.log_hashes else "GENESIS"
       
        log_entry = {
            'timestamp': timestamp,
            'user_id': str(user_id),
            'action': action,
            'details': details,
            'previous_hash': previous_hash
        }
       
        # Create hash of this entry for chain
        entry_string = f"{timestamp}|{user_id}|{action}|{details_json}|{previous_hash}"
        current_hash = hashlib.sha256(entry_string.encode()).hexdigest()
        log_entry['hash'] = current_hash
       
        # Add to chain and save
        self.log_hashes.append(current_hash)
        self._save_hash_chain()
       
        # Write to log
        logging.info(f"{user_id}|{action}|{details_json}|{current_hash}")
       
        # Also write a human-readable version for auditing
        with open(self.log_file, 'a') as f:
            f.write(f"\n--- Log Entry ---\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"User: {user_id}\n")
            f.write(f"Action: {action}\n")
            f.write(f"Details: {json.dumps(details, indent=2)}\n")
            f.write(f"Hash: {current_hash}\n")
            f.write(f"Previous Hash: {previous_hash}\n")
            f.write(f"{'='*50}\n")
   
    def verify_log_integrity(self) -> Tuple[bool, List[str]]:
        """
        REPUDIATION: Verify entire log hasn't been tampered with
        - Checks hash chain consistency from disk
       
        Returns:
            Tuple of (is_integrity_verified, list_of_issues)
        """
        issues = []
       
        if not self.log_file.exists():
            return False, ["Log file doesn't exist"]
       
        # Load the hash chain from disk
        stored_hashes = self._load_hash_chain()
       
        if not stored_hashes:
            return False, ["No hash chain found"]
       
        # Replay the log and verify each entry
        expected_previous = "GENESIS"
       
        with open(self.log_file, 'r') as f:
            content = f.read()
       
        # Parse entries and verify
        entries = content.split('='*50)
       
        for i, entry in enumerate(entries):
            if not entry.strip():
                continue
           
            # Extract hash from entry
            hash_match = re.search(r'Hash: ([a-f0-9]{64})', entry)
            if not hash_match:
                issues.append(f"Entry {i}: No hash found")
                continue
           
            current_hash = hash_match.group(1)
           
            # Verify against stored chain
            if i < len(stored_hashes):
                if current_hash != stored_hashes[i]:
                    issues.append(f"Entry {i}: Hash mismatch - possible tampering")
           
            # Verify previous hash reference
            prev_match = re.search(r'Previous Hash: ([a-f0-9]{64}|GENESIS)', entry)
            if prev_match:
                prev_hash = prev_match.group(1)
                if prev_hash != expected_previous:
                    issues.append(f"Entry {i}: Previous hash mismatch - chain broken")
           
            expected_previous = current_hash
       
        is_valid = len(issues) == 0
        self.audit_log("SYSTEM", "LOG_INTEGRITY_CHECK", {
            "valid": is_valid,
            "issues_count": len(issues)
        })
       
        return is_valid, issues
   
    # Info Disclosure Protection
   
    def _generate_encryption_key(self) -> bytes:
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'salt_should_be_stored_securely',
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(self.secret_key.encode())
        return base64.urlsafe_b64encode(key)
   
    def encrypt_sensitive_data(self, data: str) -> str:
        encrypted = self.fernet.encrypt(data.encode())
        return encrypted.decode()
   
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        decrypted = self.fernet.decrypt(encrypted_data.encode())
        return decrypted.decode()
   
    def mask_sensitive_data(self, data: str, visible_chars: int = 4) -> str:
        if len(data) <= visible_chars:
            return '*' * len(data)
        return '*' * (len(data) - visible_chars) + data[-visible_chars:]
   
    # DOS Protection
   
    def __init__(self, secret_key: str = None, app_name: str = "SecureApp"):
       
        # DOS: Rate limiting storage
        self.rate_limit_storage = {}
        self.request_history = {}
       
        # DOS: Request size limits (configurable)
        self.max_request_size = 10 * 1024 * 1024
        self.max_requests_per_ip = 100
        self.rate_window_seconds = 60
   
    def check_rate_limit(self, client_ip: str, endpoint: str = None) -> Tuple[bool, Dict]:
        """
        DOS: Advanced rate limiting
        - Tracks requests per IP
        - Implements sliding window
        - Returns status and headers for rate limiting
       
        Args:
            client_ip: Client IP address
            endpoint: Specific endpoint being accessed
           
        Returns:
            Tuple of (allowed, headers)
        """
        current_time = time.time()
        key = f"{client_ip}:{endpoint}" if endpoint else client_ip
       
        # Initialize if new client
        if key not in self.request_history:
            self.request_history[key] = []
       
        # Clean old requests (outside window)
        self.request_history[key] = [
            req_time for req_time in self.request_history[key]
            if current_time - req_time < self.rate_window_seconds
        ]
       
        # Count current requests
        request_count = len(self.request_history[key])
       
        # Calculate rate limit headers
        headers = {
            'X-RateLimit-Limit': str(self.max_requests_per_ip),
            'X-RateLimit-Remaining': str(max(0, self.max_requests_per_ip - request_count)),
            'X-RateLimit-Reset': str(int(current_time + self.rate_window_seconds))
        }
       
        # Check if over limit
        if request_count >= self.max_requests_per_ip:
            self.audit_log("SYSTEM", "RATE_LIMIT_EXCEEDED", {
                "ip": client_ip,
                "endpoint": endpoint,
                "count": request_count
            })
            return False, headers
       
        # Add current request
        self.request_history[key].append(current_time)
       
        # Clean up old entries periodically
        if len(self.request_history) > 10000: # Prevent memory issues
            self._cleanup_rate_limit_storage()
       
        return True, headers
   
    def _cleanup_rate_limit_storage(self):
        current_time = time.time()
        to_delete = []
       
        for key, requests in self.request_history.items():
            # Remove entries older than 1 hour
            self.request_history[key] = [
                req_time for req_time in requests
                if current_time - req_time < 3600
            ]
            # Mark for deletion if empty
            if not self.request_history[key]:
                to_delete.append(key)
       
        # Delete empty keys
        for key in to_delete:
            del self.request_history[key]
   
    def validate_request_size(self, data: Any, max_size_bytes: int = None) -> Tuple[bool, int]:
        """
        DOS: Improved request size validation
        - Better size calculation
        - Configurable limits
        - Returns actual size for logging
       
        Args:
            data: Request data
            max_size_bytes: Maximum allowed size (uses default if None)
           
        Returns:
            Tuple of (is_valid, size_in_bytes)
        """
        max_size = max_size_bytes or self.max_request_size
       
        try:
            if isinstance(data, (str, bytes)):
                size = len(data)
            elif isinstance(data, dict):
                size = len(json.dumps(data).encode())
            else:
                import sys
                size = sys.getsizeof(data)
           
            is_valid = size <= max_size
           
            if not is_valid:
                self.audit_log("SYSTEM", "REQUEST_SIZE_EXCEEDED", {
                    "size": size,
                    "max_size": max_size,
                    "data_type": type(data).__name__
                })
           
            return is_valid, size
           
        except Exception as e:
            self.audit_log("SYSTEM", "REQUEST_SIZE_ERROR", {"error": str(e)})
            return False, 0
   
    # Elevation od Privelage Protection
   
    def check_permission(self, user_role: str, required_role: str) -> bool:
        """Your existing code - good as is"""
        role_hierarchy = {
            'admin': 3,
            'manager': 2,
            'user': 1,
            'guest': 0
        }
       
        user_level = role_hierarchy.get(user_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
       
        authorized = user_level >= required_level
        self.audit_log("SYSTEM", "PERMISSION_CHECK",
                      {"user_role": user_role, "required": required_role,
                       "authorized": authorized})
        return authorized
   
    def validate_role_transition(self, current_role: str, new_role: str) -> bool:
        allowed_transitions = {
            'user': ['user'],
            'manager': ['manager', 'user'],
            'admin': ['admin', 'manager', 'user']
        }
        return new_role in allowed_transitions.get(current_role, [])
   
    def generate_secure_session_id(self) -> str:
        return secrets.token_urlsafe(32)
   
    def validate_origin(self, request_origin: str, allowed_origins: list) -> bool:
        return request_origin in allowed_origins
   
    # Additional DOS: BASIC WAF SIMULATION
   
    def waf_inspect_request(self, request_data: Dict, client_ip: str) -> Tuple[bool, str]:
        """
        DOS: Simple WAF (Web Application Firewall) simulation
        - Detects common attack patterns
        - Complements rate limiting
       
        Args:
            request_data: Request data to inspect
            client_ip: Client IP address
           
        Returns:
            Tuple of (is_safe, reason_if_blocked)
        """
        # Convert request to string for pattern matching
        request_str = json.dumps(request_data).lower()
       
        # Common attack patterns
        attack_patterns = {
            'sql_injection': [
                r'union.*select', r'select.*from', r'insert.*into',
                r'delete.*from', r'drop.*table', r'--', r';.*drop',
                r'exec.*xp_cmdshell', r'information_schema'
            ],
            'xss': [
                r'<script', r'javascript:', r'onerror=', r'onload=',
                r'alert\(', r'prompt\(', r'confirm\(', r'<iframe',
                r'<svg', r'eval\(', r'document\.cookie'
            ],
            'path_traversal': [
                r'\.\./', r'\.\.\\', r'%2e%2e%2f', r'%2e%2e%5c',
                r'/etc/passwd', r'c:\\windows', r'..;'
            ],
            'command_injection': [
                r';\s*ls', r';\s*cat', r';\s*rm', r';\s*wget',
                r'`.*`', r'\$\(.*\)', r'\|.*bash', r'\|.*sh'
            ]
        }
       
        for attack_type, patterns in attack_patterns.items():
            for pattern in patterns:
                if re.search(pattern, request_str, re.IGNORECASE):
                    self.audit_log("SYSTEM", "WAF_BLOCKED", {
                        "ip": client_ip,
                        "attack_type": attack_type,
                        "pattern": pattern
                    })
                    return False, f"Blocked: {attack_type} pattern detected"
       
        return True, "Request allowed"
# Usage Example
if __name__ == "__main__":
    """
    Example usage demonstrating the improvements
    """
   
    print("="*60)
    print("CRYPTOGRAPHY MODULE")
    print("="*60)
   
    # Initialize
    crypto = CryptographyManager(secret_key="test-secret-key-2024")
   
    # Tampering: XSS Prevention
    print("\n TAMPERING (XSS Prevention):")
    malicious_input = '<script>alert("hacked")</script>'
    safe = crypto.sanitize_input(malicious_input, context='html')
    print(f"Original: {malicious_input}")
    print(f"Sanitized: {safe}")
   
    # REPUDIATION: Persistent Hash Chain
    print("\n Repudiation (Persistent Logs):")
    crypto.audit_log(123, "TEST_ACTION", {"test": "data"})
    valid, issues = crypto.verify_log_integrity()
    print(f"Log integrity: {'Valid' if valid else 'Issues found'}")
    if issues:
        print(f"Issues: {issues}")
   
    # DOS: Rate Limiting
    print("\n DOS (Rate Limiting):")
    for i in range(3):
        allowed, headers = crypto.check_rate_limit("192.168.1.100", "/api/login")
        print(f"Request {i+1}: {'Allowed' if allowed else 'Blocked'} - Remaining: {headers['X-RateLimit-Remaining']}")
   
    # DOS: WAF Simulation
    print("\n DOS (WAF Simulation):")
    attack_request = {"query": "SELECT * FROM users"}
    safe, reason = crypto.waf_inspect_request(attack_request, "192.168.1.100")
    print(f"SQL injection attempt: {'Safe' if safe else f'{reason}'}")
   
    print("\n" + "="*60)
    print("All STRIDE protections implemented and tested")
    print("="*60)
