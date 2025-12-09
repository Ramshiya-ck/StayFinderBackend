from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


from user.models import User
from customer.models import *
from customer.models import *
from Hotel.models import *
from api.v1.customer.serializers import *
from django.contrib.auth import authenticate

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customers(request):
    user = request.user
    customers = Customer.objects.all()
    context = {
        'request':request
    }
    serializers = CustomerSerializer(customers,many=True,context=context)
    response_data = {
        'status_code' : 6000,
        'data' : serializers.data,
        'message' : 'Customers data retrieved successfully'
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)

        # Base response
        response_data = {
            "status_code": 6000,
            "data": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }

        # Check roles
        if user.is_admin:
            response_data["message"] = "Admin Authenticated successfully"
            response_data["data"]["is_admin"] = "admin"

        elif user.is_manager:
            response_data["message"] = "Manager Authenticated successfully"
            response_data["data"]["is_manager"] = "manager"

        elif user.is_customer:
            response_data["message"] = "Customer Authenticated successfully"
            response_data["data"]["is_customer"] = "website"

        else:
            response_data["message"] = "User role not assigned"
            response_data["data"]["dashboard"] = "none"

        return Response(response_data)

    else:
        response_data = {
            "status_code": 6001,
            "message": "Invalid Credential"
        }
        return Response(response_data)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    print(request.data)

    if User.objects.filter(email=email).exists():
        response_data = {
            "status_code": 6001,
            "data": {
            "message":"email already exist"
            }
        }
        return Response(response_data)
    
    user = User.objects.create_user(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password = password,
        is_customer = True
    )
    user.save()

    customer = Customer.objects.create(
        user=user
    )

    customer.save()
    refresh = RefreshToken.for_user(user)
    response_data = {
        'status_code' : 6000,
        'data':{
            'access':str(refresh.access_token)
        },
        'message':'user is registerd succssfully'
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get all profiles for the authenticated customer"""
    user = request.user
    
    try:
        customer = Customer.objects.get(user=user)
        profiles = Profile.objects.filter(customer=customer)
        
        context = {'request': request}
        serializers = ProfileSerializer(profiles, many=True, context=context)
        
        return Response({
            'status_code': 6000,
            'data': serializers.data,
            'message': 'Profile data retrieved successfully'
        }, status=200)
    except Customer.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Customer not found for this user'
        }, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_create(request):
    """Create a new profile for the authenticated customer"""
    user = request.user
    
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Customer not found for this user'
        }, status=404)
    
    context = {'request': request}
    serializer = ProfileSerializer(data=request.data, context=context)
    
    if serializer.is_valid():
        # Check if this should be the default profile
        is_default = request.data.get('is_default', False)
        
        # If no profiles exist, make this the default
        if not Profile.objects.filter(customer=customer).exists():
            is_default = True
        
        profile = serializer.save(customer=customer, is_default=is_default)
        
        return Response({
            'status_code': 6000,
            'data': ProfileSerializer(profile, context=context).data,
            'message': 'Profile created successfully'
        }, status=201)
    
    return Response({
        'status_code': 6001,
        'errors': serializer.errors,
        'message': 'Profile creation failed'
    }, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail(request, profile_id):
    """Get a single profile by ID for the authenticated customer"""
    user = request.user
    
    try:
        customer = Customer.objects.get(user=user)
        profile = Profile.objects.get(id=profile_id, customer=customer)
        
        context = {'request': request}
        serializer = ProfileSerializer(profile, context=context)
        
        return Response({
            'status_code': 6000,
            'data': serializer.data,
            'message': 'Profile retrieved successfully'
        }, status=200)
    except Customer.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Customer not found'
        }, status=404)
    except Profile.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Profile not found or does not belong to you'
        }, status=404)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_update(request, profile_id):
    """Update a profile for the authenticated customer"""
    user = request.user
    
    try:
        customer = Customer.objects.get(user=user)
        profile = Profile.objects.get(id=profile_id, customer=customer)
    except Customer.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Customer not found'
        }, status=404)
    except Profile.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Profile not found or does not belong to you'
        }, status=404)
    
    context = {'request': request}
    partial = request.method == 'PATCH'
    serializer = ProfileSerializer(profile, data=request.data, context=context, partial=partial)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status_code': 6000,
            'data': serializer.data,
            'message': 'Profile updated successfully'
        }, status=200)
    
    return Response({
        'status_code': 6001,
        'errors': serializer.errors,
        'message': 'Profile update failed'
    }, status=400)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete(request, profile_id):
    """Delete a profile for the authenticated customer"""
    user = request.user
    
    try:
        customer = Customer.objects.get(user=user)
        profile = Profile.objects.get(id=profile_id, customer=customer)
        
        # Prevent deletion if it's the only profile
        profile_count = Profile.objects.filter(customer=customer).count()
        if profile_count == 1:
            return Response({
                'status_code': 6001,
                'message': 'Cannot delete the only profile. Please create another profile first.'
            }, status=400)
        
        # If deleting default profile, set another as default
        if profile.is_default:
            other_profile = Profile.objects.filter(customer=customer).exclude(id=profile_id).first()
            if other_profile:
                other_profile.is_default = True
                other_profile.save()
        
        profile.delete()
        
        return Response({
            'status_code': 6000,
            'message': 'Profile deleted successfully'
        }, status=200)
    except Customer.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Customer not found'
        }, status=404)
    except Profile.DoesNotExist:
        return Response({
            'status_code': 6001,
            'message': 'Profile not found or does not belong to you'
        }, status=404)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    slider = Slider.objects.all()
    hotel = Hotal.objects.all()
    context = {
        'request':request
    }
    slider_serializers = SliderSerializer(slider,many=True,context=context)
    hotel_serializers = HotalSerializer(hotel,many=True,context=context)
    response_data = {
        "status_code": 6000,
        "slider": slider_serializers.data,
        "hotel": hotel_serializers.data,
        "message": "Index data retrieved successfully"
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def slider(request):
    instance = Slider.objects.all()
    context = {
        'request':request
    }
    serializers = SliderSerializer(instance, many=True, context=context)

    response_data = {
       'status_code' : 6000,
       'data' : serializers.data,
       'message' : 'Slider list retrieved successfully'
    }
    return Response(response_data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"message": "Logout successful"})
    except Exception as e:
        return Response({"error": str(e)})
    
   






    



    



   








    







        



