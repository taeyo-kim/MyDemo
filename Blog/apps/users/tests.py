from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class SignUpViewTest(TestCase):
    """회원가입 테스트"""
    
    def setUp(self):
        self.client = Client()
    
    def test_signup_view_get(self):
        """회원가입 페이지 접근 테스트"""
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')
    
    def test_signup_success(self):
        """회원가입 성공 테스트"""
        response = self.client.post(
            reverse('users:signup'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'testpass123!@#',
                'password2': 'testpass123!@#'
            }
        )
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_signup_invalid_password(self):
        """잘못된 비밀번호로 회원가입 시도 테스트"""
        response = self.client.post(
            reverse('users:signup'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'testpass123!@#',
                'password2': 'differentpass'
            }
        )
        self.assertEqual(response.status_code, 200)  # 폼 에러로 같은 페이지
        self.assertFalse(User.objects.filter(username='newuser').exists())


class LoginViewTest(TestCase):
    """로그인 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """로그인 페이지 접근 테스트"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_login_success(self):
        """로그인 성공 테스트"""
        response = self.client.post(
            reverse('users:login'),
            {
                'username': 'testuser',
                'password': 'testpass123'
            }
        )
        self.assertEqual(response.status_code, 302)  # 홈페이지로 리다이렉트
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_invalid_credentials(self):
        """잘못된 인증 정보로 로그인 시도 테스트"""
        response = self.client.post(
            reverse('users:login'),
            {
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )
        self.assertEqual(response.status_code, 200)  # 폼 에러로 같은 페이지
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutViewTest(TestCase):
    """로그아웃 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_logout(self):
        """로그아웃 테스트"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # 홈페이지로 리다이렉트
        # 로그아웃 후 인증 상태 확인
        response = self.client.get(reverse('posts:post_list'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

