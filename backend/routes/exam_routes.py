from flask import Blueprint, request, jsonify
from models.exam_model import create_exam, get_all_exams
import jwt
from functools import wraps

exam_bp = Blueprint('exam', __name__)

SECRET_KEY = "your_secret_key"

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({"message": "Token missing!"}), 401
#         try:
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             return f(user_id=data['id'], role=data['role'], *args, **kwargs)
#         except:
#             return jsonify({"message": "Token invalid!"}), 403
#     return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f"[DEBUG] Received token: {token}")

        if not token:
            return jsonify({"message": "Token missing!"}), 401

        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(f"[DEBUG] Decoded token: {data}")

            # FIXED: use 'user_id' instead of 'id'
            return f(user_id=data['user_id'], role=data['role'], *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired!"}), 401
        except jwt.InvalidTokenError as e:
            print(f"[DEBUG] Invalid token: {e}")
            return jsonify({"message": "Token invalid!"}), 403
        except Exception as e:
            print(f"[DEBUG] Unexpected error during token decoding: {e}")
            return jsonify({"message": "Internal server error"}), 500

    return decorated



@exam_bp.route('/create_exam', methods=['POST'])
@token_required
def create_exam_route(user_id, role):
    if role != "teacher" and role != "admin":
        return jsonify({"message": "Access denied!"}), 403
    data = request.get_json()
    create_exam(data['title'], data['description'], data['date'], data['duration'], user_id)
    return jsonify({"message": "Exam created successfully!"})

@exam_bp.route('/get_exams', methods=['GET'])
@token_required
def get_exams_route(user_id, role):
    exams = get_all_exams()
    return jsonify(exams)

@exam_bp.route('/report_proctor_alert', methods=['POST'])
@token_required
def report_proctor_alert(user_id, role):
    data = request.get_json()
    print(f"[Proctoring Alert] UserID {user_id}: {data['message']} at {data['timestamp']}")
    return jsonify({"message": "Alert received"})

@exam_bp.route('/submit_exam', methods=['POST'])
@token_required
def submit_exam(user_id, role):
    data = request.get_json()
    print(f"Auto-submitting exam for User {user_id}. Reason: {data['reason']}, Time: {data['timestamp']}")
    # TODO: Save exam attempt to DB and mark it as auto-submitted
    return jsonify({"message": "Exam submitted successfully!"})
