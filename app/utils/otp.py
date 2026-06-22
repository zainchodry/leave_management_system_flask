import random


def generate_otp() -> str:
    """Return a 6-digit OTP as a string."""
    return str(random.randint(100000, 999999))
