from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
import os

from config import Config
from models import User, VitalRecord
from auth import generate_token, get_current_user, admin_required
from validation import validate_vital_signs, validate_user_registration

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=Config.JWT_EXPIRE_DAYS)

CORS(app)
jwt = JWTManager(app)

# ========== AUTH ROUTES ==========

@app.route('/api/auth/register', methods=['POST'])
@validate_user_registration
def register():
    data = request.json
    
    existing_user = User.find_by_email(data['email'])
    if existing_user:
        return jsonify({"message": "User already exists"}), 400
    
    user = User.create(
        email=data['email'],
        password=data['password'],
        full_name=data['full_name']
    )
    
    token = generate_token(user['id'])
    
    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "full_name": user['full_name'],
            "role": user['role']
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.find_by_email(email)
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    
    if not User.validate_password(user, password):
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = generate_token(user['id'])
    
    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "full_name": user['full_name'],
            "role": user['role']
        }
    })

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_me():
    user = get_current_user()
    return jsonify({"success": True, "user": user})

# ========== VITAL RECORDS ROUTES (User) ==========

@app.route('/api/vitals/records', methods=['POST'])
@jwt_required()
@validate_vital_signs
def create_vital_record():
    user_id = int(get_jwt_identity())
    
    record = VitalRecord.create({
        'user_id': user_id,
        **request.json
    })
    
    return jsonify({
        "success": True,
        "message": "Vital signs submitted successfully. Awaiting admin approval.",
        "data": record
    }), 201

@app.route('/api/vitals/records', methods=['GET'])
@jwt_required()
def get_my_vital_records():
    user_id = int(get_jwt_identity())
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    records = VitalRecord.find_by_user(user_id, limit, offset)
    
    return jsonify({
        "success": True,
        "count": len(records),
        "data": records
    })

@app.route('/api/vitals/records/<int:record_id>', methods=['GET'])
@jwt_required()
def get_vital_record_by_id(record_id):
    user_id = int(get_jwt_identity())
    user = get_current_user()
    is_admin = user.get('role') == 'admin'
    
    record = VitalRecord.find_by_id(record_id, user_id, is_admin)
    
    if not record:
        return jsonify({"message": "Record not found"}), 404
    
    if not is_admin and record['user_id'] != user_id:
        return jsonify({"message": "Not authorized"}), 403
    
    return jsonify({"success": True, "data": record})

@app.route('/api/vitals/records/<int:record_id>', methods=['PUT'])
@jwt_required()
@validate_vital_signs
def update_vital_record(record_id):
    user_id = int(get_jwt_identity())
    
    record = VitalRecord.find_by_id(record_id, user_id, False)
    
    if not record:
        return jsonify({"message": "Record not found"}), 404
    
    if record['status'] != 'pending':
        return jsonify({"message": f"Cannot update record with status: {record['status']}. Only pending records can be updated."}), 400
    
    updated_record = VitalRecord.update(record_id, request.json, user_id, False)
    
    return jsonify({
        "success": True,
        "message": "Record updated successfully",
        "data": updated_record
    })

@app.route('/api/vitals/records/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_vital_record(record_id):
    user_id = int(get_jwt_identity())
    
    record = VitalRecord.find_by_id(record_id, user_id, False)
    
    if not record:
        return jsonify({"message": "Record not found"}), 404
    
    if record['status'] != 'pending':
        return jsonify({"message": f"Cannot delete record with status: {record['status']}. Only pending records can be deleted."}), 400
    
    VitalRecord.delete(record_id, user_id, False)
    
    return jsonify({"success": True, "message": "Record deleted successfully"})

# ========== ADMIN ROUTES ==========

@app.route('/api/vitals/admin/pending', methods=['GET'])
@jwt_required()
@admin_required()
def get_pending_records():
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    records = VitalRecord.find_all_pending(limit, offset)
    
    return jsonify({
        "success": True,
        "count": len(records),
        "data": records
    })

@app.route('/api/vitals/admin/approve/<int:record_id>', methods=['PUT'])
@jwt_required()
@admin_required()
def approve_record(record_id):
    admin_id = int(get_jwt_identity())
    admin_notes = request.json.get('admin_notes')
    
    record = VitalRecord.approve(record_id, admin_id, admin_notes)
    
    if not record:
        return jsonify({"message": "Record not found or already processed"}), 404
    
    return jsonify({
        "success": True,
        "message": "Record approved successfully",
        "data": record
    })

@app.route('/api/vitals/admin/reject/<int:record_id>', methods=['PUT'])
@jwt_required()
@admin_required()
def reject_record(record_id):
    admin_id = int(get_jwt_identity())
    admin_notes = request.json.get('admin_notes')
    
    record = VitalRecord.reject(record_id, admin_id, admin_notes)
    
    if not record:
        return jsonify({"message": "Record not found or already processed"}), 404
    
    return jsonify({
        "success": True,
        "message": "Record rejected successfully",
        "data": record
    })

@app.route('/api/vitals/admin/users/<int:user_id>/records', methods=['GET'])
@jwt_required()
@admin_required()
def get_user_records(user_id):
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    records = VitalRecord.find_by_user(user_id, limit, offset)
    
    return jsonify({
        "success": True,
        "count": len(records),
        "data": records
    })

# ========== HEALTH CHECK ==========

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "timestamp": __import__('datetime').datetime.now().isoformat()})

# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Route not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Internal server error"}), 500

if __name__ == '__main__':
    port = Config.PORT
    app.run(host='0.0.0.0', port=port, debug=True)
