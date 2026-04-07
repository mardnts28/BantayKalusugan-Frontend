import psycopg2
import psycopg2.extras
from datetime import datetime
import bcrypt
from config import Config

class Database:
    _instance = None
    
    @classmethod
    def get_connection(cls):
        if cls._instance is None:
            cls._instance = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
        return cls._instance

class User:
    @staticmethod
    def create(email, password, full_name, role='user'):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, full_name, role, created_at
        """, (email, password_hash, full_name, role))
        
        conn.commit()
        result = cursor.fetchone()
        cursor.close()
        return dict(result)
    
    @staticmethod
    def find_by_email(email):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None
    
    @staticmethod
    def find_by_id(user_id):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, email, full_name, role, created_at FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None
    
    @staticmethod
    def validate_password(user, password):
        return bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8'))

class VitalRecord:
    @staticmethod
    def create(data):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO vital_records (
                user_id, heart_rate, blood_pressure_systolic,
                blood_pressure_diastolic, temperature,
                oxygen_saturation, respiratory_rate, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
            RETURNING *
        """, (
            data['user_id'], data.get('heart_rate'), data.get('blood_pressure_systolic'),
            data.get('blood_pressure_diastolic'), data.get('temperature'),
            data.get('oxygen_saturation'), data.get('respiratory_rate')
        ))
        
        conn.commit()
        result = cursor.fetchone()
        cursor.close()
        return dict(result)
    
    @staticmethod
    def find_by_id(record_id, user_id=None, is_admin=False):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT vr.*, u.full_name as user_name, u.email as user_email
            FROM vital_records vr
            JOIN users u ON vr.user_id = u.id
            WHERE vr.id = %s
        """
        params = [record_id]
        
        if not is_admin and user_id:
            query += " AND vr.user_id = %s"
            params.append(user_id)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None
    
    @staticmethod
    def find_by_user(user_id, limit=50, offset=0):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM vital_records
            WHERE user_id = %s
            ORDER BY submitted_at DESC
            LIMIT %s OFFSET %s
        """, (user_id, limit, offset))
        
        results = cursor.fetchall()
        cursor.close()
        return [dict(row) for row in results]
    
    @staticmethod
    def find_all_pending(limit=100, offset=0):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT vr.*, u.full_name as user_name, u.email as user_email
            FROM vital_records vr
            JOIN users u ON vr.user_id = u.id
            WHERE vr.status = 'pending'
            ORDER BY vr.submitted_at ASC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        results = cursor.fetchall()
        cursor.close()
        return [dict(row) for row in results]
    
    @staticmethod
    def update(record_id, data, user_id=None, is_admin=False):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                         'temperature', 'oxygen_saturation', 'respiratory_rate']
        
        set_clauses = []
        values = []
        
        for field in allowed_fields:
            if field in data:
                set_clauses.append(f"{field} = %s")
                values.append(data[field])
        
        if not set_clauses:
            return None
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(record_id)
        
        query = f"UPDATE vital_records SET {', '.join(set_clauses)} WHERE id = %s"
        
        if not is_admin and user_id:
            query += " AND user_id = %s"
            values.append(user_id)
        
        query += " RETURNING *"
        
        cursor.execute(query, values)
        conn.commit()
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None
    
    @staticmethod
    def approve(record_id, admin_id, admin_notes=None):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE vital_records
            SET status = 'approved',
                reviewed_at = CURRENT_TIMESTAMP,
                reviewed_by = %s,
                admin_notes = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND status = 'pending'
            RETURNING *
        """, (admin_id, admin_notes, record_id))
        
        conn.commit()
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None
    
    @staticmethod
    def reject(record_id, admin_id, admin_notes=None):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE vital_records
            SET status = 'rejected',
                reviewed_at = CURRENT_TIMESTAMP,
                reviewed_by = %s,
                admin_notes = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND status = 'pending'
            RETURNING *
        """, (admin_id, admin_notes, record_id))
        
        conn.commit()
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None
    
    @staticmethod
    def delete(record_id, user_id=None, is_admin=False):
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM vital_records WHERE id = %s"
        params = [record_id]
        
        if not is_admin and user_id:
            query += " AND user_id = %s"
            params.append(user_id)
        
        query += " RETURNING id"
        
        cursor.execute(query, params)
        conn.commit()
        result = cursor.fetchone()
        cursor.close()
        return dict(result) if result else None
