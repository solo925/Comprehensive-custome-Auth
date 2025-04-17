from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import LoginHistory
from .serializers import UserSerializer, LoginHistorySerializer
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

@login_required
def login_history(request):
    history = LoginHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'accounts/login_history.html', {'history': history})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

# API Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_api(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login_history_api(request):
    history = LoginHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]
    serializer = LoginHistorySerializer(history, many=True)
    return Response(serializer.data)



@login_required
def setup_2fa(request):
    # Get or create TOTP device
    device, created = TOTPDevice.objects.get_or_create(
        user=request.user,
        name="default"
    )
    
    if request.method == 'POST':
        token = request.POST.get('token')
        
        # Verify the token
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, "Two-factor authentication enabled successfully!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Invalid token. Please try again.")
    
    # Generate QR code
    url = device.config_url
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgImage)
    buffer = BytesIO()
    img.save(buffer)
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return render(request, 'accounts/setup_2fa.html', {
        'device': device,
        'qr_code': qr_code,
    })

@login_required
def disable_2fa(request):
    if request.method == 'POST':
        # Delete all TOTP devices for this user
        TOTPDevice.objects.filter(user=request.user).delete()
        messages.success(request, "Two-factor authentication disabled successfully!")
        return redirect('accounts:profile')
    
    return render(request, 'accounts/disable_2fa.html')

