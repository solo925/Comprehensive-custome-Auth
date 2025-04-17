# Django Custom Authentication System

A comprehensive authentication and authorization system built with Django 5+, featuring OAuth2 social logins, role-based permissions, and advanced security features.

## 🌟 Features

### Authentication Methods
- **Email/Password** with strong validation
- **Social Authentication**:
  - Google OAuth2
  - GitHub
  - LinkedIn
- **Two-Factor Authentication** (TOTP-based)
- **JWT Authentication** for API endpoints

### Advanced Security
- Email confirmation via token
- Login rate-limiting and brute force protection
- Strong password validation
- Session timeout management
- Security headers implementation
- CAPTCHA protection for forms
- IP-based geolocation access control

### User Management
- Custom `User` model
- Role-based permissions system
- Login activity tracking
- Audit logging for sensitive actions

## 🛠️ Tech Stack

- Django 5.0+
- `django-allauth` for social authentication
- `django-rest-framework` for API endpoints
- `djangorestframework-simplejwt` for JWT authentication
- `django-axes` for login throttling
- `django-otp` for two-factor authentication
- `django-recaptcha` for CAPTCHA protection
- `django-geoip2-extras` for geolocation features

## 📋 Prerequisites

- Python 3.9+
- pip
- PostgreSQL (recommended) or SQLite for development

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-custom-auth.git
   cd django-custom-auth
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy `.env.example` to `.env` and update with your settings:
   ```bash
   cp .env.example .env
   # Edit .env with your editor
   ```

5. **Apply migrations**
   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Social Authentication

#### Google OAuth2

1. Go to [Google Developer Console](https://console.developers.google.com/)
2. Create a new project
3. Navigate to "APIs & Services" > "Credentials"
4. Create "OAuth client ID" (Web application)
5. Add authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`
6. Save your Client ID and Client Secret in `.env` file

#### GitHub OAuth

1. Go to GitHub Settings > Developer settings > OAuth Apps > New OAuth App
2. Set callback URL to: `http://localhost:8000/accounts/github/login/callback/`
3. Save your Client ID and Client Secret in `.env` file

#### LinkedIn OAuth

1. Go to LinkedIn Developer Portal > Create App
2. Set redirect URL to: `http://localhost:8000/accounts/linkedin_oauth2/login/callback/`
3. Save your Client ID and Client Secret in `.env` file

### Two-Factor Authentication

Two-Factor Authentication is optional and can be enabled in the user profile section after login.

### CAPTCHA Protection

1. Get reCAPTCHA keys from [Google reCAPTCHA](https://www.google.com/recaptcha/admin)
2. Add the keys to `.env` file

### Geolocation Access Control

1. Download GeoLite2 database files from [MaxMind](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
2. Place the files in the `geoip2` directory
3. Configure allowed countries in settings

## 📁 Project Structure

```
auth_project/
│
├── accounts/              # Authentication app
│   ├── migrations/
│   ├── forms.py           # Custom forms including CAPTCHA
│   ├── geo.py             # Geolocation middleware
│   ├── middleware.py      # Role middleware
│   ├── models.py          # User and Role models
│   ├── permissions.py     # Permission decorators
│   ├── security.py        # Security headers middleware
│   ├── serializers.py     # API serializers
│   ├── session.py         # Session timeout middleware
│   ├── signals.py         # Auth signals for logging
│   ├── urls.py            # App URLs
│   ├── validators.py      # Password validators
│   └── views.py           # Auth views
│
├── auth_project/          # Project config
│   ├── asgi.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py
│
├── templates/             # HTML templates
│   ├── accounts/
│   ├── allauth/
│   ├── admin/
│   └── home.html
│
├── geoip2/                # GeoIP2 databases
│   ├── GeoLite2-City.mmdb
│   └── GeoLite2-Country.mmdb
│
├── .env                   # Environment variables
├── .gitignore
├── manage.py
└── requirements.txt
```

## 🖥️ Usage

### Basic Authentication Flow

1. User registers with email/password or social account
2. Confirmation email is sent for email validation
3. User confirms email and can log in
4. Optional: User enables two-factor authentication

### Role-Based Access Control

To use role-based permissions in views:

```python
from accounts.permissions import role_required, permission_required

@role_required('Admin')
def admin_only_view(request):
    # Only accessible to users with Admin role
    return render(request, 'admin_page.html')

@permission_required('accounts.add_user')
def create_user_view(request):
    # Only accessible to users with 'add_user' permission
    return render(request, 'create_user.html')
```

For DRF API views:

```python
from accounts.permissions import HasRolePermission
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([HasRolePermission('Editor')])
def editor_api_view(request):
    # Only accessible to users with Editor role
    return Response({"status": "success"})
```

### JWT Authentication for APIs

To authenticate API requests:

1. Obtain a token:
   ```bash
   curl -X POST http://localhost:8000/api/token/ \
        -d "email=user@example.com&password=yourpassword"
   ```

2. Use the token in requests:
   ```bash
   curl -H "Authorization: Bearer <your_token>" \
        http://localhost:8000/accounts/api/profile/
   ```

## 🏢 Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure a proper email backend
5. Enable HTTPS and all security settings
6. Update social authentication callback URLs to production domain
7. Set strong SECRET_KEY and JWT_SECRET_KEY
8. Consider using environment variables for sensitive settings

## 📋 API Documentation

### Authentication Endpoints

- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token
- `POST /api/auth/registration/` - Register new user
- `POST /api/auth/login/` - Log in user
- `POST /api/auth/logout/` - Log out user
- `GET /api/auth/user/` - Get current user

### User Endpoints

- `GET /accounts/api/profile/` - Get user profile
- `GET /accounts/api/login-history/` - Get login history

## 🔧 Troubleshooting

### Common Issues

1. **Social login not working**
   - Check if callback URLs match exactly
   - Verify Client ID and Secret
   - Ensure proper scopes are configured

2. **Email confirmation not sent**
   - Check email backend configuration
   - Verify SMTP settings

3. **JWT token issues**
   - Check token expiration settings
   - Verify JWT secret key

4. **Two-factor authentication problems**
   - Ensure time synchronization on device
   - Check if TOTP secret was saved correctly

## 🔄 Extending the System

This authentication system can be extended with:

1. Additional social providers
2. More sophisticated permission models
3. Advanced audit logging
4. API rate limiting
5. Alternative MFA options (SMS, email, etc.)
6. Account recovery mechanisms
7. Progressive security measures

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

