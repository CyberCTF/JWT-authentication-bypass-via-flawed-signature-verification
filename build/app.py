from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import jwt
import datetime
import sqlite3
import os
from functools import wraps
import urllib.parse

app = Flask(__name__)
app.secret_key = 'corporate_assets_secret_2024'

DATABASE = 'corporate_assets.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee',
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_name TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            serial_number TEXT UNIQUE,
            value REAL,
            location TEXT,
            assigned_to TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Remove existing sensitive_data table creation and inserts
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS sensitive_data (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         title TEXT NOT NULL,
    #         content TEXT NOT NULL,
    #         classification TEXT DEFAULT 'confidential',
    #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #     )
    # ''')
    
    # Default users - only these two target users
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                  ('mitchell.parker', 'corporate2024', 'employee', 'IT Support'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                  ('sarah.johnson', 'finance789', 'employee', 'Finance'))
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                  ('administrator', 'admin123!@#', 'admin', 'Management'))
    
    # Sample assets
    cursor.execute("INSERT OR IGNORE INTO assets (asset_name, asset_type, serial_number, value, location, assigned_to) VALUES (?, ?, ?, ?, ?, ?)",
                  ('Dell Laptop XPS 15', 'Computer', 'DL2024001', 1200.00, 'Office Floor 3', 'mitchell.parker'))
    cursor.execute("INSERT OR IGNORE INTO assets (asset_name, asset_type, serial_number, value, location, assigned_to) VALUES (?, ?, ?, ?, ?, ?)",
                  ('iPhone 14 Pro', 'Mobile Device', 'IP2024001', 999.00, 'Office Floor 2', 'sarah.johnson'))
    cursor.execute("INSERT OR IGNORE INTO assets (asset_name, asset_type, serial_number, value, location, assigned_to) VALUES (?, ?, ?, ?, ?, ?)",
                  ('MacBook Pro M2', 'Computer', 'MB2024001', 2500.00, 'Office Floor 2', 'sarah.johnson'))
    cursor.execute("INSERT OR IGNORE INTO assets (asset_name, asset_type, serial_number, value, location, assigned_to) VALUES (?, ?, ?, ?, ?, ?)",
                  ('iPad Pro 12.9', 'Tablet', 'IP2024002', 1100.00, 'Office Floor 3', 'mitchell.parker'))
    cursor.execute("INSERT OR IGNORE INTO assets (asset_name, asset_type, serial_number, value, location, assigned_to) VALUES (?, ?, ?, ?, ?, ?)",
                  ('Server Rack HP ProLiant', 'Server', 'HP2024001', 5000.00, 'Data Center', 'administrator'))
    
    conn.commit()
    conn.close()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check both cookie names for compatibility
        token = request.cookies.get('token') or request.cookies.get('auth_token')
        
        # Decode URL-encoded token if present
        if token:
            token = urllib.parse.unquote(token)
        
        print(f"DEBUG: Token received: {token}", flush=True)
        
        if not token:
            print("DEBUG: No token found, redirecting to login", flush=True)
            return redirect(url_for('login'))
        
        try:
            # Parse JWT parts
            parts = token.split('.')
            print(f"DEBUG: JWT parts count: {len(parts)}")
            
            if len(parts) < 2:
                print("DEBUG: JWT must have at least 2 parts")
                return redirect(url_for('login'))
            
            header, payload = parts[0], parts[1]
            signature = parts[2] if len(parts) > 2 else ""
            
            # Decode and validate header
            import base64
            import json
            
            header_padded = header + '=' * (4 - len(header) % 4)
            try:
                header_data = json.loads(base64.urlsafe_b64decode(header_padded))
                print(f"DEBUG: Header decoded: {header_data}")
            except Exception as e:
                print(f"DEBUG: Header decode failed: {e}")
                return redirect(url_for('login'))
            
            alg = header_data.get('alg', 'HS256')
            print(f"DEBUG: Algorithm detected: {alg}")
            
            # Deux modes de validation :
            if alg == 'none':
                print("DEBUG: JWT 'none' algorithm detected - checking bypass conditions")
                
                # BYPASS MODE: Conditions strictes pour l'accès admin
                # 1. Type MUST be exactly "JWT"
                if header_data.get('typ') != 'JWT':
                    print(f"DEBUG: Type must be 'JWT', got: {header_data.get('typ')}")
                    return redirect(url_for('login'))
                
                # 2. Signature MUST be empty
                if signature != '':
                    print(f"DEBUG: Signature must be empty, got: '{signature}'")
                    return redirect(url_for('login'))
                    
                # 3. Decode payload
                payload_padded = payload + '=' * (4 - len(payload) % 4)
                try:
                    data = json.loads(base64.urlsafe_b64decode(payload_padded))
                    print(f"DEBUG: Payload decoded: {data}")
                except Exception as e:
                    print(f"DEBUG: Payload decode failed: {e}")
                    return redirect(url_for('login'))
                
                # 4. Subject MUST be exactly "administrator"
                if data.get('sub') != 'administrator':
                    print(f"DEBUG: Subject must be 'administrator', got: {data.get('sub')}")
                    return redirect(url_for('login'))
                    
                # 5. Role MUST be exactly "admin"
                if data.get('role') != 'admin':
                    print(f"DEBUG: Role must be 'admin', got: {data.get('role')}")
                    return redirect(url_for('login'))
                
                print("DEBUG: ✅ JWT BYPASS SUCCESSFUL! All bypass conditions met.")
                return f(data, *args, **kwargs)
                
            else:
                print("DEBUG: Standard JWT validation (HS256)")
                
                # STANDARD MODE: Validation JWT normale
                if len(parts) != 3:
                    print("DEBUG: Standard JWT must have exactly 3 parts")
                    return redirect(url_for('login'))
                    
                # Vérification standard avec la clé secrète
                data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
                print(f"DEBUG: ✅ Standard JWT valid for user: {data.get('sub')}")
                return f(data, *args, **kwargs)
                
        except jwt.ExpiredSignatureError:
            print("DEBUG: JWT expired")
            return redirect(url_for('login'))
        except jwt.InvalidTokenError as e:
            print(f"DEBUG: Invalid JWT: {e}")
            return redirect(url_for('login'))
        except Exception as e:
            print(f"DEBUG: Exception during JWT validation: {e}")
            return redirect(url_for('login'))
    return decorated

@app.route('/')
def index():
    return redirect(url_for('my_account'))

@app.route('/my-account')
@token_required
def my_account(user_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get user's assets
    cursor.execute("SELECT * FROM assets WHERE assigned_to = ? ORDER BY created_at DESC LIMIT 5", 
                  (user_data['sub'],))
    user_assets = cursor.fetchall()
    
    # Get asset count
    cursor.execute("SELECT COUNT(*) FROM assets WHERE assigned_to = ?", (user_data['sub'],))
    asset_count = cursor.fetchone()[0]
    
    # Get total value
    cursor.execute("SELECT SUM(value) FROM assets WHERE assigned_to = ?", (user_data['sub'],))
    total_value = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return render_template('my_account.html', 
                         user=user_data, 
                         assets=user_assets,
                         asset_count=asset_count,
                         total_value=total_value)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            return render_template('register.html', error='Username and password are required')
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error='Username already exists')
        
        # Create new user account
        try:
            cursor.execute("INSERT INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
                          (username, password, 'employee', 'General'))
            conn.commit()
            
            # Vérifier que l'utilisateur a bien été créé
            cursor.execute("SELECT username, role, department FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Auto-login after registration avec JWT standard
                token = jwt.encode({
                    'sub': user[0],
                    'role': user[1],
                    'department': user[2],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }, app.secret_key, algorithm='HS256')
                
                resp = make_response(redirect(url_for('my_account')))
                resp.set_cookie('auth_token', token, httponly=True)
                return resp
            else:
                return render_template('register.html', error='Registration failed - user not created')
        except Exception as e:
            conn.close()
            return render_template('register.html', error=f'Registration failed: {str(e)}')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT username, role, department FROM users WHERE username = ? AND password = ?", 
                      (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            token = jwt.encode({
                'sub': user[0],
                'role': user[1],
                'department': user[2],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.secret_key, algorithm='HS256')
            
            resp = make_response(redirect(url_for('my_account')))
            resp.set_cookie('auth_token', token, httponly=True)
            return resp
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
@token_required
def dashboard(user_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if user_data['role'] == 'admin':
        cursor.execute("SELECT COUNT(*) FROM assets")
        total_assets = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(value) FROM assets")
        total_value = cursor.fetchone()[0] or 0
    else:
        cursor.execute("SELECT COUNT(*) FROM assets WHERE assigned_to = ?", (user_data['sub'],))
        total_assets = cursor.fetchone()[0]
        total_users = 0
        cursor.execute("SELECT SUM(value) FROM assets WHERE assigned_to = ?", (user_data['sub'],))
        total_value = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT * FROM assets WHERE assigned_to = ? ORDER BY created_at DESC LIMIT 5", 
                  (user_data['sub'],))
    recent_assets = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         user=user_data, 
                         total_assets=total_assets,
                         total_users=total_users,
                         total_value=total_value,
                         recent_assets=recent_assets)

@app.route('/assets')
@token_required
def assets(user_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if user_data['role'] == 'admin':
        cursor.execute("SELECT * FROM assets ORDER BY created_at DESC")
    else:
        cursor.execute("SELECT * FROM assets WHERE assigned_to = ? ORDER BY created_at DESC", 
                      (user_data['sub'],))
    
    assets_list = cursor.fetchall()
    conn.close()
    
    return render_template('assets.html', user=user_data, assets=assets_list)

@app.route('/admin')
@token_required
def admin_panel(user_data):
    if user_data['role'] != 'admin':
        return render_template('error.html', 
                             error="Access Denied", 
                             message="Administrator privileges required to access this section."), 403
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get all users except admin
    cursor.execute("SELECT * FROM users WHERE role != 'admin' ORDER BY created_at DESC")
    users = cursor.fetchall()
    
    # Get system statistics
    cursor.execute("SELECT COUNT(*) FROM users WHERE role != 'admin'")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM assets")
    total_assets = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(value) FROM assets")
    total_value = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return render_template('admin.html', 
                         user=user_data, 
                         users=users,
                         total_users=total_users,
                         total_assets=total_assets,
                         total_value=total_value)

@app.route('/admin/delete', methods=['GET'])
@token_required
def delete_user(user_data):
    if user_data['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username parameter required'}), 400
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Prevent deletion of admin user
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        user_role = cursor.fetchone()
        
        if not user_role:
            conn.close()
            return jsonify({'error': 'User not found'}), 404
        
        if user_role[0] == 'admin':
            conn.close()
            return jsonify({'error': 'Cannot delete administrator account'}), 403
        
        # Delete the user
        cursor.execute("DELETE FROM users WHERE username = ? AND role != 'admin'", (username,))
        deleted_count = cursor.rowcount  # Capturer AVANT l'UPDATE
        
        # Also remove their asset assignments
        cursor.execute("UPDATE assets SET assigned_to = NULL WHERE assigned_to = ?", (username,))
        
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"DEBUG: Successfully deleted user {username}", flush=True)
            return jsonify({'success': True, 'message': f'User {username} has been deleted successfully'})
        else:
            print(f"DEBUG: No rows affected when trying to delete {username}", flush=True)
            return jsonify({'error': 'User deletion failed'}), 500
            
    except Exception as e:
        print(f"DEBUG: Error deleting user {username}: {str(e)}", flush=True)
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/profile')
@token_required
def profile(user_data):
    return render_template('profile.html', user=user_data)

@app.route('/users')
def users_list():
    """Page publique pour voir la liste des utilisateurs (pour observer les suppressions)"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get all users except admin with basic info
    cursor.execute("SELECT username, role, department, created_at FROM users WHERE role != 'admin' ORDER BY created_at DESC")
    users = cursor.fetchall()
    
    # Get user count
    cursor.execute("SELECT COUNT(*) FROM users WHERE role != 'admin'")
    user_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('users_list.html', users=users, user_count=user_count)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('auth_token', '', expires=0)
    return resp

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3206, debug=True)
