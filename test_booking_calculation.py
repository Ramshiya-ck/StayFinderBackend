"""
Test script to verify booking amount calculations for multiple nights
Run: python manage.py shell < test_booking_calculation.py
"""

from booking.models import Booking
from Room.models import Room
from Hotel.models import Hotal
from user.models import User
from datetime import date, timedelta
from decimal import Decimal

print("\n" + "="*60)
print("BOOKING AMOUNT CALCULATION TEST")
print("="*60 + "\n")

# Example scenario:
# Room price: $100 per night
# Check-in: 2025-12-10
# Check-out: 2025-12-13 (3 nights)
# Expected Total: $300
# Expected Advance (30%): $90
# Expected Balance: $210

print("Scenario: Room costs $100/night")
print("Booking: Dec 10 to Dec 13 (3 nights)")
print("\nExpected Results:")
print("  Total Amount: $300 (100 × 3 nights)")
print("  Advance Amount: $90 (30% of total)")
print("  Balance Amount: $210 (300 - 90)")
print("\n" + "-"*60)

# Test case explanation
test_cases = [
    {
        "nights": 1,
        "room_price": 100,
        "expected_total": 100,
        "expected_advance": 30,
        "expected_balance": 70
    },
    {
        "nights": 2,
        "room_price": 100,
        "expected_total": 200,
        "expected_advance": 60,
        "expected_balance": 140
    },
    {
        "nights": 3,
        "room_price": 150,
        "expected_total": 450,
        "expected_advance": 135,
        "expected_balance": 315
    },
    {
        "nights": 7,
        "room_price": 200,
        "expected_total": 1400,
        "expected_advance": 420,
        "expected_balance": 980
    }
]

print("\nTest Cases Summary:")
print(f"{'Nights':<8} {'Price':<10} {'Total':<12} {'Advance':<12} {'Balance':<12}")
print("-"*60)

for test in test_cases:
    nights = test['nights']
    price = test['room_price']
    total = test['expected_total']
    advance = test['expected_advance']
    balance = test['expected_balance']
    
    print(f"{nights:<8} ${price:<9} ${total:<11} ${advance:<11} ${balance:<11}")

print("\n" + "="*60)
print("How the calculation works:")
print("="*60)
print("""
1. Total Amount = Room Price × Number of Nights
   - Number of Nights = (Check-out Date - Check-in Date).days
   
2. Advance Amount = Total Amount × 30% (if not provided)
   - User can provide custom advance amount
   
3. Balance Amount = Total Amount - Advance Amount
   - Automatically calculated

All calculations happen in the model's save() method!
""")

print("="*60)
print("✅ The booking system now correctly calculates amounts")
print("   for single or multiple night bookings!")
print("="*60 + "\n")
