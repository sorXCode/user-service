from cachetools.func import mru_cache
from random import randrange
import os

@mru_cache()
def generate_token(email):
    # generated tokens are cached, subsequent generation will give the same otp
    # thus function is used for both otp generation and verification
    otp_length = int(os.environ.get("OTP_LENGTH", 6))
    return "".join([str(randrange(0,10)) for x in range(otp_length)])
