import bcrypt
import psycopg2
import psycopg2.extras
from config import Config

def create_admin():
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        cursor = conn.cursor()
        
        email = 'admin@example.com'
        password = 'Admin123!'
        full_name = 'System Administrator'
        role = 'admin'
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET role = 'admin'
            RETURNING id, email, full_name, role
        """, (email, password_hash, full_name, role))
        
        conn.commit()
        result = cursor.fetchone()
        
        print("Admin user created/updated:", dict(result))
        print("Email: admin@example.com")
        print("Password: Admin123!")
        
        cursor.close()
        conn.close()
        
    except Exception as error:
        print("Error creating admin:", error)

if __name__ == '__main__':
    create_admin()
