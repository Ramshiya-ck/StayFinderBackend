
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse


from api.v1.booking.serializers import *
from booking.models import *
from django.db.models import F


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from booking.models import Booking
from Payment.models import Payment
from .serializers import BookingSerializer


import logging

logger = logging.getLogger(__name__)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_booking_list(request):
    user = request.user
    booking = Booking.objects.all()
    context = {
        'request' : request
    }
    serializer = BookingSerializer(booking,many = True,context = context) 
    return Response({
        "status_code": 6000,
        "message": "Booking list retrieved successfully",
        "data": serializer.data
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def booking_list(request, hotel_id=None, room_id=None):
    customer = request.user

    # Base filter → only customer’s bookings
    bookings = Booking.objects.filter(customer=customer)

    # Optional hotel filter
    if hotel_id:
        bookings = bookings.filter(hotel_id=hotel_id)

    # Optional room filter
    if room_id:
        bookings = bookings.filter(room_id=room_id)

    bookings = bookings.filter(
        advance_amount__gte=(0.3 * F("total_amount"))
    )

    serializer = BookingSerializer(bookings, many=True, context={"request": request})

    return Response({
        "status_code": 6000,
        "message": "Booking list retrieved successfully",
        "data": serializer.data
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def single_booking(request, booking_id):
    customer = request.user

    # Get booking for this customer or 404
    booking = get_object_or_404(Booking, id=booking_id, customer=customer)

    # # Optional: only include bookings with advance_amount >= 30% of total
    # if booking.advance_amount < 0.3 * booking.total_amount:
    #     return Response({
    #         "status_code": 4001,
    #         "message": "Booking does not meet advance payment criteria",
    #         "data": {}
    #     })

    serializer = BookingSerializer(booking, context={"request": request})

    return Response({
        "status_code": 6001,
        "message": "Booking retrieved successfully",
        "data": serializer.data
    })






@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking_create(request):
    customer = request.user
    hotel_id = request.data.get("hotel")
    room_id = request.data.get("room")
    check_in = request.data.get("check_in")
    check_out = request.data.get("check_out")
    guests = request.data.get("guest")
    address = request.data.get("address")
    phone = request.data.get("phone")
    total_amount = request.data.get("total_amount")
    advance_amount = request.data.get("advance_amount")
    balance_amount = request.data.get("balance_amount")

    # 🛑 Validation: missing required fields
    if not hotel_id or not room_id or not check_in or not check_out:
        return Response({
            "status_code": 6001,
            "message": "Hotel, Room, Check-in, and Check-out are required"
        })

    # 🛑 Validation: check if room is already booked in date range
    overlapping = Booking.objects.filter(
        hotel_id=hotel_id,
        room_id=room_id,
        booking_status__in=["pending", "confirmed"],  # only active bookings
        check_in__lt=check_out,
        check_out__gt=check_in,
        guests = guests,
        address = address,
        phone = phone,
        total_amount = total_amount,
        advance_amount = advance_amount,
        balance_amount = balance_amount,
        

    )

    if overlapping.exists():
        return Response({
            "status_code": 6002,
            "message": "This room is already booked for the selected dates"
        })

    # ✅ Create booking
    data = request.data.copy()
    data["customer"] = customer.id
    serializer = BookingSerializer(data=data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status_code": 6000,
            "message": "Booking created successfully",
            "data": serializer.data
        })
    
    return Response({
        "status_code": 6003,
        "message": "Validation failed",
        "errors": serializer.errors
    })

    
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def booking_update(request, booking_id):
    user = request.user

    # ✅ Fetch only bookings of the logged-in user
    bookings = Booking.objects.filter(customer=user, id=booking_id)

    if not bookings.exists():
        return Response({
            "status_code": 6001,
            "message": f"No booking found with ID {booking_id} for this user",
            "data": {}
        })

    booking = bookings.first()
    serializer = BookingSerializer(
        booking, data=request.data, partial=True, context={"request": request}
    )

    if serializer.is_valid():
        updated_booking = serializer.save()
        return Response({
            "status_code": 6000,
            "message": f"Booking {booking_id} updated successfully",
            "data": BookingSerializer(updated_booking, context={"request": request}).data
        })

    return Response({
        "status_code": 6001,
        "message": "Booking update failed",
        "data": serializer.errors
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def booking_deleted(request, booking_id):
    user = request.user

    # ✅ Filter bookings of the logged-in user
    bookings = Booking.objects.filter(customer=user, id=booking_id)
   

    if not bookings.exists():
        return Response({
            "status_code": 6001,
            "message": f"No booking found with ID {booking_id} for this user",
            "data": {}
        })

    booking = bookings.first()
    booking.delete()

    return Response({
        "status_code": 6000,
        "message": f"Booking {booking_id} deleted successfully",
        "data": {}
    })




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def booking_cancel(request,id):
    user = request.user
    instance = Booking.objects.get(id=id)
    instance.status = "cancelled"
    instance.save()

    response_data = {
        "status_code" : 6000,
        "data" : {
            "id" : instance.id,
            "status" : instance.status
        },
        "message" : "Booking cancelled successfully"
    }
    return Response(response_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def booking_reschedule(request,id):
    user = request.user
    instance = get_object_or_404(Booking, id=id,customer=user)

    check_in = request.data.get('check_in')
    check_out = request.data.get("check_out")
    number_of_guest = request.data.get('number_of_guest')
    status = request.data.get('status')



#  checkout must be after check-in
    if check_out <= check_in:
        response_data = {
            "status_code" : 6001,
            "message" : "Check-out date must be after check-in date."
        }
        return Response(response_data)
    
# Booking must not be cancelled/completed
    if instance.status in ["cancelled", "completed"]:
        response_data = {
            "status_code" : 6001,
            "message" : f"Cannot reschedule a {instance.status} booking."
        }
        return Response(response_data)
    

    
    instance.check_in = check_in
    instance.check_out = check_out
    instance.number_of_guest = number_of_guest

# Only owner/admin should be able to change status
    if status and status in dict(Booking.STATUS_CHOICE).keys():
        instance.status =status
    instance.save()

    response_data = {
        "status_code" : 6000,
        "data" : {
            "id" : instance.id,
            "check_in" : instance.check_in,
            "check_out" : instance.check_out,
            "status" : instance.status,
            "message" : " Booking rescheduled successfully"
        }
    }
    return Response(response_data)



# __________________________payment_________________________



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    user = request.user
    booking_id = request.data.get("booking_id")

    if not booking_id:
        return JsonResponse({"error": "booking_id is required"}, status=400)

    # Get booking
    try:
        booking = Booking.objects.get(id=booking_id, customer=user)
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Booking not found"}, status=404)

    amount = booking.advance_amount
    if amount <= 0:
        return JsonResponse({"error": "Invalid advance amount"}, status=400)

    # Create Payment record
    payment = Payment.objects.create(
        booking=booking,
        amount=amount,
        status="pending"
    )

    try:
        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": settings.STRIPE_CURRENCY,
                    "unit_amount": int(amount * 100),  # amount in cents/paise
                    "product_data": {
                        "name": f"Advance payment for booking #{booking.id}"
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            metadata={
                "payment_id": payment.id,
                "booking_id": booking.id
            },
            success_url=f"http://localhost:5173/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url="http://localhost:3000/payment/cancel",
        )

        # Save session ID to Payment
        payment.stripe_checkout_session_id = checkout_session.id
        payment.save()

        return JsonResponse({"checkout_url": checkout_session.url})

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        return JsonResponse({"error": "Failed to create Stripe checkout session"}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"error": "Internal server error"}, status=500)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)  # optional
    if not endpoint_secret:
        logger.error("STRIPE_WEBHOOK_SECRET is not configured")
        return HttpResponse(status=500)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]

        try:
            payment = Payment.objects.get(stripe_checkout_session_id=session_id)
        except Payment.DoesNotExist:
            logger.warning(f"No Payment found for session_id: {session_id}")
            return HttpResponse(status=200)  # Still return 200 to Stripe

        # Update payment and booking
        payment.status = "paid"
        payment.save()

        booking = payment.booking
        booking.advance_amount += payment.amount
        if booking.advance_amount >= booking.total_amount:
            booking.payment_status = "paid"
            booking.booking_status = "confirmed"
        booking.save()

        logger.info(f"Payment {payment.id} marked as paid for booking {booking.id}")

    return HttpResponse(status=200)


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except ValueError:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError:
#         return HttpResponse(status=400)

#     # handle event types you care about:
#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]
#         session_id = session["id"]
#         # update your Payment/Booking based on session_id
#         # ...
#     return HttpResponse(status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_payment(request,session_id):
    # session_id = request.GET.get("session_id")
    if not session_id:
        return JsonResponse({"error": "Missing session_id"}, status=400)

    try:
        payment = Payment.objects.get(stripe_checkout_session_id=session_id)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)

    booking = payment.booking
       # Retrieve the session from Stripe to confirm payment status
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid" and payment.status != "paid":
            # Update payment
            payment.status = "paid"
            payment.save()

            # Update booking
            booking.payment_status = "paid"
            booking.booking_status = "confirmed"
            booking.save()

    return JsonResponse({
        "payment_id": payment.id,
        "status": payment.status,  # pending / paid / failed
        "amount": float(payment.amount),
        "booking_id": booking.id,
        "booking_status": booking.booking_status,
        "payment_status": booking.payment_status,
    })
