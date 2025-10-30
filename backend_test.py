#!/usr/bin/env python3
"""
Backend API Testing for Lakeside Indian Restaurant
Tests banner image upload feature and related functionality
"""

import requests
import json
import os
import tempfile
from PIL import Image
import io
import uuid

# Configuration
BASE_URL = "https://lakeside-menu-app.preview.emergentagent.com/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

class GalleryUploadTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.test_results = []
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def authenticate(self):
        """Authenticate and get admin token"""
        print("\n=== AUTHENTICATION TEST ===")
        try:
            response = requests.post(
                f"{self.base_url}/admin/login",
                json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.log_result(
                    "Admin Authentication", 
                    True, 
                    "Successfully authenticated",
                    {"username": data.get("username"), "token_type": data.get("token_type")}
                )
                return True
            else:
                self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Authentication failed: {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Authentication error: {str(e)}")
            return False
    
    def create_test_image(self, format="PNG"):
        """Create a test image file"""
        img = Image.new('RGB', (800, 400), color='blue')
        img_buffer = io.BytesIO()
        img.save(img_buffer, format=format)
        img_buffer.seek(0)
        return img_buffer
    
    def test_gallery_file_upload_valid(self):
        """Test uploading a valid image file to gallery"""
        print("\n=== GALLERY FILE UPLOAD - VALID IMAGE TEST ===")
        
        if not self.token:
            self.log_result("Gallery File Upload - Valid Image", False, "No authentication token")
            return None
            
        try:
            # Create test image
            test_image = self.create_test_image("PNG")
            
            headers = {"Authorization": f"Bearer {self.token}"}
            files = {"file": ("test_gallery.png", test_image, "image/png")}
            
            response = requests.post(
                f"{self.base_url}/admin/gallery/upload",
                headers=headers,
                files=files,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                url = data.get("url")
                filename = data.get("filename")
                
                if url and filename:
                    self.log_result(
                        "Gallery File Upload - Valid Image", 
                        True, 
                        "Gallery image uploaded successfully",
                        {"url": url, "filename": filename}
                    )
                    return {"url": url, "filename": filename}
                else:
                    self.log_result(
                        "Gallery File Upload - Valid Image", 
                        False, 
                        "Missing URL or filename in response",
                        {"response": data}
                    )
            else:
                self.log_result(
                    "Gallery File Upload - Valid Image", 
                    False, 
                    f"Gallery upload failed: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("Gallery File Upload - Valid Image", False, f"Gallery upload error: {str(e)}")
        
        return None
    
    def test_gallery_file_upload_invalid_type(self):
        """Test uploading invalid file type to gallery"""
        print("\n=== GALLERY FILE UPLOAD - INVALID TYPE TEST ===")
        
        if not self.token:
            self.log_result("Gallery File Upload - Invalid Type", False, "No authentication token")
            return
            
        try:
            # Create text file instead of image
            text_content = b"This is not an image file"
            
            headers = {"Authorization": f"Bearer {self.token}"}
            files = {"file": ("test.txt", io.BytesIO(text_content), "text/plain")}
            
            response = requests.post(
                f"{self.base_url}/admin/gallery/upload",
                headers=headers,
                files=files,
                timeout=10
            )
            
            if response.status_code in [400, 500]:
                self.log_result(
                    "Gallery File Upload - Invalid Type", 
                    True, 
                    "Correctly rejected invalid file type",
                    {"status_code": response.status_code}
                )
            else:
                self.log_result(
                    "Gallery File Upload - Invalid Type", 
                    False, 
                    f"Should have rejected invalid file type, got: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("Gallery File Upload - Invalid Type", False, f"Test error: {str(e)}")
    
    def test_gallery_file_upload_no_auth(self):
        """Test uploading without authentication to gallery"""
        print("\n=== GALLERY FILE UPLOAD - NO AUTH TEST ===")
        
        try:
            test_image = self.create_test_image("PNG")
            files = {"file": ("test_gallery.png", test_image, "image/png")}
            
            response = requests.post(
                f"{self.base_url}/admin/gallery/upload",
                files=files,
                timeout=10
            )
            
            if response.status_code in [401, 403]:
                self.log_result(
                    "Gallery File Upload - No Auth", 
                    True, 
                    "Correctly rejected unauthorized request",
                    {"status_code": response.status_code}
                )
            else:
                self.log_result(
                    "Gallery File Upload - No Auth", 
                    False, 
                    f"Should have rejected unauthorized request, got: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("Gallery File Upload - No Auth", False, f"Test error: {str(e)}")
    
    def test_gallery_crud_with_uploaded_image(self, uploaded_file_info):
        """Test gallery CRUD operations with uploaded image"""
        print("\n=== GALLERY CRUD WITH UPLOADED IMAGE TEST ===")
        
        if not uploaded_file_info or not self.token:
            self.log_result("Gallery CRUD", False, "Missing uploaded file info or token")
            return None
            
        gallery_image_id = None
        
        try:
            # Create gallery image with uploaded image
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            gallery_data = {
                "url": uploaded_file_info["url"],
                "title": "Test Gallery Image with Upload",
                "description": "This is a test gallery image created with an uploaded file"
            }
            
            response = requests.post(
                f"{self.base_url}/admin/gallery",
                headers=headers,
                json=gallery_data,
                timeout=10
            )
            
            if response.status_code == 200:
                gallery_image = response.json()
                gallery_image_id = gallery_image.get("id")
                self.log_result(
                    "Gallery Image Creation", 
                    True, 
                    "Gallery image created with uploaded file",
                    {"gallery_id": gallery_image_id, "image_url": gallery_image.get("url")}
                )
            else:
                self.log_result(
                    "Gallery Image Creation", 
                    False, 
                    f"Failed to create gallery image: {response.status_code}",
                    {"response": response.text}
                )
                return None
            
            # Test getting public gallery images
            response = requests.get(f"{self.base_url}/gallery", timeout=10)
            
            if response.status_code == 200:
                gallery_images = response.json()
                found_image = next((img for img in gallery_images if img.get("id") == gallery_image_id), None)
                if found_image:
                    self.log_result(
                        "Gallery Public List", 
                        True, 
                        "Gallery image found in public list",
                        {"gallery_count": len(gallery_images)}
                    )
                else:
                    self.log_result("Gallery Public List", False, "Created gallery image not found in public list")
            else:
                self.log_result(
                    "Gallery Public List", 
                    False, 
                    f"Failed to get public gallery: {response.status_code}"
                )
            
            return gallery_image_id
            
        except Exception as e:
            self.log_result("Gallery CRUD", False, f"Gallery CRUD error: {str(e)}")
            return gallery_image_id
    
    def test_gallery_deletion(self, gallery_image_id):
        """Test gallery image deletion"""
        print("\n=== GALLERY IMAGE DELETION TEST ===")
        
        if not gallery_image_id or not self.token:
            self.log_result("Gallery Image Deletion", False, "Missing gallery image ID or token")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.delete(
                f"{self.base_url}/admin/gallery/{gallery_image_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_result("Gallery Image Deletion", True, "Gallery image deleted successfully")
                
                # Verify gallery image is deleted
                response = requests.get(f"{self.base_url}/gallery", timeout=10)
                
                if response.status_code == 200:
                    gallery_images = response.json()
                    found_image = next((img for img in gallery_images if img.get("id") == gallery_image_id), None)
                    if not found_image:
                        self.log_result("Gallery Deletion Verification", True, "Gallery image successfully removed from list")
                    else:
                        self.log_result("Gallery Deletion Verification", False, "Gallery image still exists after deletion")
                        
            else:
                self.log_result(
                    "Gallery Image Deletion", 
                    False, 
                    f"Failed to delete gallery image: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("Gallery Image Deletion", False, f"Gallery deletion error: {str(e)}")
    
    def test_file_storage_verification(self, uploaded_file_info):
        """Test that uploaded files are saved to uploads directory"""
        print("\n=== FILE STORAGE VERIFICATION TEST ===")
        
        if not uploaded_file_info:
            self.log_result("File Storage Verification", False, "No uploaded file to verify")
            return
            
        try:
            # Check if file exists in uploads directory
            filename = uploaded_file_info.get("filename")
            if filename:
                file_path = f"/app/backend/uploads/{filename}"
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    self.log_result(
                        "File Storage Verification", 
                        True, 
                        "Uploaded file exists in uploads directory",
                        {"file_path": file_path, "file_size": file_size}
                    )
                else:
                    self.log_result(
                        "File Storage Verification", 
                        False, 
                        "Uploaded file not found in uploads directory",
                        {"expected_path": file_path}
                    )
            else:
                self.log_result("File Storage Verification", False, "No filename provided for verification")
                
        except Exception as e:
            self.log_result("File Storage Verification", False, f"File storage verification error: {str(e)}")
    
    def run_all_tests(self):
        """Run all gallery upload tests"""
        print("🚀 Starting Gallery Image Upload Feature Tests")
        print(f"Testing against: {self.base_url}")
        
        # Step 1: Authenticate
        if not self.authenticate():
            print("\n❌ Cannot proceed without authentication")
            return self.generate_summary()
        
        # Step 2: Test gallery file upload scenarios
        uploaded_file_info = self.test_gallery_file_upload_valid()
        self.test_gallery_file_upload_invalid_type()
        self.test_gallery_file_upload_no_auth()
        
        # Step 3: Test file storage verification
        self.test_file_storage_verification(uploaded_file_info)
        
        # Step 4: Test gallery CRUD with uploaded image
        gallery_image_id = self.test_gallery_crud_with_uploaded_image(uploaded_file_info)
        
        # Step 5: Test gallery deletion
        if gallery_image_id:
            self.test_gallery_deletion(gallery_image_id)
        
        return self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "="*60)
        print("📊 GALLERY TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"  • {result['test']}: {result['message']}")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "results": self.test_results
        }

class BannerUploadTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.test_results = []
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def authenticate(self):
        """Authenticate and get admin token"""
        print("\n=== AUTHENTICATION TEST ===")
        try:
            response = requests.post(
                f"{self.base_url}/admin/login",
                json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.log_result(
                    "Admin Authentication", 
                    True, 
                    "Successfully authenticated",
                    {"username": data.get("username"), "token_type": data.get("token_type")}
                )
                return True
            else:
                self.log_result(
                    "Admin Authentication", 
                    False, 
                    f"Authentication failed: {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Authentication error: {str(e)}")
            return False
    
    def create_test_image(self, format="PNG"):
        """Create a test image file"""
        img = Image.new('RGB', (800, 400), color='red')
        img_buffer = io.BytesIO()
        img.save(img_buffer, format=format)
        img_buffer.seek(0)
        return img_buffer
    
    def test_file_upload_valid(self):
        """Test uploading a valid image file"""
        print("\n=== FILE UPLOAD - VALID IMAGE TEST ===")
        
        if not self.token:
            self.log_result("File Upload - Valid Image", False, "No authentication token")
            return None
            
        try:
            # Create test image
            test_image = self.create_test_image("PNG")
            
            headers = {"Authorization": f"Bearer {self.token}"}
            files = {"file": ("test_banner.png", test_image, "image/png")}
            
            response = requests.post(
                f"{self.base_url}/admin/banners/upload",
                headers=headers,
                files=files,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                url = data.get("url")
                filename = data.get("filename")
                
                if url and filename:
                    self.log_result(
                        "File Upload - Valid Image", 
                        True, 
                        "Image uploaded successfully",
                        {"url": url, "filename": filename}
                    )
                    return {"url": url, "filename": filename}
                else:
                    self.log_result(
                        "File Upload - Valid Image", 
                        False, 
                        "Missing URL or filename in response",
                        {"response": data}
                    )
            else:
                self.log_result(
                    "File Upload - Valid Image", 
                    False, 
                    f"Upload failed: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("File Upload - Valid Image", False, f"Upload error: {str(e)}")
        
        return None
    
    def test_file_upload_invalid_type(self):
        """Test uploading invalid file type"""
        print("\n=== FILE UPLOAD - INVALID TYPE TEST ===")
        
        if not self.token:
            self.log_result("File Upload - Invalid Type", False, "No authentication token")
            return
            
        try:
            # Create text file instead of image
            text_content = b"This is not an image file"
            
            headers = {"Authorization": f"Bearer {self.token}"}
            files = {"file": ("test.txt", io.BytesIO(text_content), "text/plain")}
            
            response = requests.post(
                f"{self.base_url}/admin/banners/upload",
                headers=headers,
                files=files,
                timeout=10
            )
            
            if response.status_code in [400, 500]:
                self.log_result(
                    "File Upload - Invalid Type", 
                    True, 
                    "Correctly rejected invalid file type",
                    {"status_code": response.status_code}
                )
            else:
                self.log_result(
                    "File Upload - Invalid Type", 
                    False, 
                    f"Should have rejected invalid file type, got: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("File Upload - Invalid Type", False, f"Test error: {str(e)}")
    
    def test_file_upload_no_auth(self):
        """Test uploading without authentication"""
        print("\n=== FILE UPLOAD - NO AUTH TEST ===")
        
        try:
            test_image = self.create_test_image("PNG")
            files = {"file": ("test_banner.png", test_image, "image/png")}
            
            response = requests.post(
                f"{self.base_url}/admin/banners/upload",
                files=files,
                timeout=10
            )
            
            if response.status_code in [401, 403]:
                self.log_result(
                    "File Upload - No Auth", 
                    True, 
                    "Correctly rejected unauthorized request",
                    {"status_code": response.status_code}
                )
            else:
                self.log_result(
                    "File Upload - No Auth", 
                    False, 
                    f"Should have rejected unauthorized request, got: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("File Upload - No Auth", False, f"Test error: {str(e)}")
    
    def test_static_file_serving(self, uploaded_file_info):
        """Test static file serving for uploaded images"""
        print("\n=== STATIC FILE SERVING TEST ===")
        
        if not uploaded_file_info:
            self.log_result("Static File Serving", False, "No uploaded file to test")
            return
            
        try:
            # Test accessing the uploaded file via backend directly (this should work)
            backend_url = f"http://localhost:8001{uploaded_file_info['url']}"
            
            response = requests.get(backend_url, timeout=10)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type:
                    self.log_result(
                        "Static File Serving (Backend)", 
                        True, 
                        "Uploaded image accessible via backend static URL",
                        {"url": backend_url, "content_type": content_type, "size": len(response.content)}
                    )
                else:
                    self.log_result(
                        "Static File Serving (Backend)", 
                        False, 
                        f"File accessible but wrong content type: {content_type}",
                        {"url": backend_url}
                    )
            else:
                self.log_result(
                    "Static File Serving (Backend)", 
                    False, 
                    f"Cannot access uploaded file via backend: {response.status_code}",
                    {"url": backend_url, "response": response.text}
                )
            
            # Test accessing via external URL (may have routing issues)
            external_url = f"https://lakeside-menu-app.preview.emergentagent.com{uploaded_file_info['url']}"
            
            response = requests.get(external_url, timeout=10)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type:
                    self.log_result(
                        "Static File Serving (External)", 
                        True, 
                        "Uploaded image accessible via external URL",
                        {"url": external_url, "content_type": content_type, "size": len(response.content)}
                    )
                else:
                    self.log_result(
                        "Static File Serving (External)", 
                        False, 
                        f"External URL routing issue - returns HTML instead of image (Kubernetes ingress configuration)",
                        {"url": external_url, "content_type": content_type}
                    )
            else:
                self.log_result(
                    "Static File Serving (External)", 
                    False, 
                    f"Cannot access uploaded file via external URL: {response.status_code}",
                    {"url": external_url}
                )
                
        except Exception as e:
            self.log_result("Static File Serving", False, f"Static file test error: {str(e)}")
    
    def test_banner_crud_with_uploaded_image(self, uploaded_file_info):
        """Test banner CRUD operations with uploaded image"""
        print("\n=== BANNER CRUD WITH UPLOADED IMAGE TEST ===")
        
        if not uploaded_file_info or not self.token:
            self.log_result("Banner CRUD", False, "Missing uploaded file info or token")
            return None
            
        banner_id = None
        
        try:
            # Create banner with uploaded image
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            banner_data = {
                "image": uploaded_file_info["url"],
                "title": "Test Banner with Uploaded Image",
                "description": "This is a test banner created with an uploaded image",
                "button_text": "Order Now",
                "button_link": "/menu",
                "order": 1,
                "active": True
            }
            
            response = requests.post(
                f"{self.base_url}/admin/banners",
                headers=headers,
                json=banner_data,
                timeout=10
            )
            
            if response.status_code == 200:
                banner = response.json()
                banner_id = banner.get("id")
                self.log_result(
                    "Banner Creation", 
                    True, 
                    "Banner created with uploaded image",
                    {"banner_id": banner_id, "image_url": banner.get("image")}
                )
            else:
                self.log_result(
                    "Banner Creation", 
                    False, 
                    f"Failed to create banner: {response.status_code}",
                    {"response": response.text}
                )
                return None
            
            # Test getting all admin banners
            response = requests.get(
                f"{self.base_url}/admin/banners",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                banners = response.json()
                found_banner = next((b for b in banners if b.get("id") == banner_id), None)
                if found_banner:
                    self.log_result(
                        "Banner Admin List", 
                        True, 
                        "Banner found in admin list",
                        {"banner_count": len(banners)}
                    )
                else:
                    self.log_result("Banner Admin List", False, "Created banner not found in admin list")
            else:
                self.log_result(
                    "Banner Admin List", 
                    False, 
                    f"Failed to get admin banners: {response.status_code}"
                )
            
            # Test getting public banners
            response = requests.get(f"{self.base_url}/banners", timeout=10)
            
            if response.status_code == 200:
                public_banners = response.json()
                found_public = next((b for b in public_banners if b.get("id") == banner_id), None)
                if found_public:
                    self.log_result(
                        "Banner Public List", 
                        True, 
                        "Banner found in public list",
                        {"public_banner_count": len(public_banners)}
                    )
                else:
                    self.log_result("Banner Public List", False, "Created banner not found in public list")
            else:
                self.log_result(
                    "Banner Public List", 
                    False, 
                    f"Failed to get public banners: {response.status_code}"
                )
            
            # Test updating banner
            update_data = {
                "title": "Updated Test Banner Title",
                "description": "Updated description for test banner"
            }
            
            response = requests.put(
                f"{self.base_url}/admin/banners/{banner_id}",
                headers=headers,
                json=update_data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_result("Banner Update", True, "Banner updated successfully")
            else:
                self.log_result(
                    "Banner Update", 
                    False, 
                    f"Failed to update banner: {response.status_code}",
                    {"response": response.text}
                )
            
            return banner_id
            
        except Exception as e:
            self.log_result("Banner CRUD", False, f"Banner CRUD error: {str(e)}")
            return banner_id
    
    def test_banner_deletion(self, banner_id):
        """Test banner deletion"""
        print("\n=== BANNER DELETION TEST ===")
        
        if not banner_id or not self.token:
            self.log_result("Banner Deletion", False, "Missing banner ID or token")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.delete(
                f"{self.base_url}/admin/banners/{banner_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_result("Banner Deletion", True, "Banner deleted successfully")
                
                # Verify banner is deleted
                response = requests.get(
                    f"{self.base_url}/admin/banners",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    banners = response.json()
                    found_banner = next((b for b in banners if b.get("id") == banner_id), None)
                    if not found_banner:
                        self.log_result("Banner Deletion Verification", True, "Banner successfully removed from list")
                    else:
                        self.log_result("Banner Deletion Verification", False, "Banner still exists after deletion")
                        
            else:
                self.log_result(
                    "Banner Deletion", 
                    False, 
                    f"Failed to delete banner: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_result("Banner Deletion", False, f"Banner deletion error: {str(e)}")
    
    def run_all_tests(self):
        """Run all banner upload tests"""
        print("🚀 Starting Banner Image Upload Feature Tests")
        print(f"Testing against: {self.base_url}")
        
        # Step 1: Authenticate
        if not self.authenticate():
            print("\n❌ Cannot proceed without authentication")
            return self.generate_summary()
        
        # Step 2: Test file upload scenarios
        uploaded_file_info = self.test_file_upload_valid()
        self.test_file_upload_invalid_type()
        self.test_file_upload_no_auth()
        
        # Step 3: Test static file serving
        self.test_static_file_serving(uploaded_file_info)
        
        # Step 4: Test banner CRUD with uploaded image
        banner_id = self.test_banner_crud_with_uploaded_image(uploaded_file_info)
        
        # Step 5: Test banner deletion
        if banner_id:
            self.test_banner_deletion(banner_id)
        
        return self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"  • {result['test']}: {result['message']}")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "results": self.test_results
        }

if __name__ == "__main__":
    print("🏛️ LAKESIDE INDIAN RESTAURANT - BACKEND API TESTING")
    print("="*60)
    
    # Run Gallery Upload Tests (Primary Focus)
    print("\n🖼️  GALLERY IMAGE UPLOAD TESTS")
    gallery_tester = GalleryUploadTester()
    gallery_summary = gallery_tester.run_all_tests()
    
    # Run Banner Upload Tests (For Regression)
    print("\n🎯 BANNER IMAGE UPLOAD TESTS (Regression)")
    banner_tester = BannerUploadTester()
    banner_summary = banner_tester.run_all_tests()
    
    # Combined Summary
    total_tests = gallery_summary["total"] + banner_summary["total"]
    total_passed = gallery_summary["passed"] + banner_summary["passed"]
    total_failed = gallery_summary["failed"] + banner_summary["failed"]
    
    print("\n" + "="*60)
    print("🎯 OVERALL TEST SUMMARY")
    print("="*60)
    print(f"Gallery Tests: {gallery_summary['passed']}/{gallery_summary['total']} passed")
    print(f"Banner Tests: {banner_summary['passed']}/{banner_summary['total']} passed")
    print(f"Total: {total_passed}/{total_tests} passed ({(total_passed/total_tests*100):.1f}%)")
    
    # Exit with error code if tests failed
    if total_failed > 0:
        print(f"\n❌ {total_failed} tests failed")
        exit(1)
    else:
        print("\n🎉 All tests passed!")
        exit(0)