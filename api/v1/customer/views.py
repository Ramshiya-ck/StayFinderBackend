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
    user = request.user
    customer = Profile.objects.all()
    context = {
        'request':request
    }
    serializers = ProfileSerializer(customer,many=True,context=context)
    response_data = {
        'status_code' : 6000,
        'data' : serializers.data,
        'message' : 'Profile data retrieved successfully'
    }
    return Response(response_data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def profile_create(request):
#     user = request.user
#     customer = Customer.objects.get(user=user)

#     # Use get_or_create for existing profile
#     profile, created = Profile.objects.get_or_create(customer=customer)

#     serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
    
#     if serializer.is_valid():
#         serializer.save(customer=customer)  # Set customer here, not in request.data
#         return Response({
#             'status_code': 6000,
#             'data': serializer.data,
#             'message': 'Profile created successfully'
#         })
#     else:
#         return Response({
#             'status_code': 6001,
#             'error': serializer.errors,
#             'message': 'Profile creation failed'
#         })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request,id):
    user = request.user
    customer = Profile.objects.get(user=id)
    context = {
        'request':request   
    }
    serializers = ProfileSerializer(customer,context= context,data=request.data,partial=True)
    if serializers.is_valid():
        serializers.save()
        response_data = {
            'status_code' : 6000,
            'data' : serializers.data,
            'message' : 'Profile updated successfully'
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code' : 6001,
            'error' : serializers.errors,
            'message' : 'Profile updation failed'
        }
        return Response(response_data)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete(request,id):
    user = request.user
    customer = Customer.objects.get(user=id)
    customer.delete()
    user.delete()
    response_data = {
        'status_code' : 6000,
        'data' : {},
        'message' : 'Profile deleted successfully'
    }
    return Response(response_data)
    

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
    
   






    



    



   








    







        



