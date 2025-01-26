import ctypes
import os

lib_path = os.path.join(os.path.dirname(__file__), 'libpaytr.so')
libpaytr = ctypes.CDLL(lib_path)

class PaymentRequest(ctypes.Structure):
    _fields_ = [
        ('merchant_id', ctypes.c_char_p),
        ('merchant_oid', ctypes.c_char_p),
        ('paytr_token', ctypes.c_char_p),
        ('payment_amount', ctypes.c_char_p),
        ('user_name', ctypes.c_char_p),
        ('user_address', ctypes.c_char_p),
        ('email', ctypes.c_char_p),
        ('user_phone', ctypes.c_char_p),
        ('user_ip', ctypes.c_char_p),
        ('user_basket', ctypes.c_char_p),
        ('currency', ctypes.c_char_p),
        ('no_installment', ctypes.c_char_p),
        ('max_installment', ctypes.c_char_p),
        ('lang', ctypes.c_char_p),
        ('merchant_ok_url', ctypes.c_char_p),
        ('merchant_fail_url', ctypes.c_char_p),
        ('debug_on', ctypes.c_char_p),
        ('test_mode', ctypes.c_char_p),
        ('timeout_limit', ctypes.c_char_p),
    ]


libpaytr.call_api.restype = ctypes.c_int
libpaytr.call_api.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.POINTER(PaymentRequest),
    ctypes.c_char_p,
    ctypes.c_size_t
]

def send(data):
    request = PaymentRequest(
        data.get('merchant_id', '').encode('utf-8'),
        data.get('merchant_oid', '').encode('utf-8'),
        data.get('paytr_token', '').encode('utf-8'),
        data.get('payment_amount', '').encode('utf-8'),
        data.get('user_name', '').encode('utf-8'),
        data.get('user_address', '').encode('utf-8'),
        data.get('email', '').encode('utf-8'),
        data.get('user_phone', '').encode('utf-8'),
        data.get('user_ip', '').encode('utf-8'),
        data.get('user_basket', '').encode('utf-8'),
        data.get('currency', '').encode('utf-8'),
        data.get('no_installment', '').encode('utf-8'),
        data.get('max_installment', '').encode('utf-8'),
        data.get('lang', '').encode('utf-8'),
        data.get('merchant_ok_url', '').encode('utf-8'),
        data.get('merchant_fail_url', '').encode('utf-8'),
        data.get('debug_on', '').encode('utf-8'),
        data.get('test_mode', '').encode('utf-8'),
        data.get('timeout_limit', '').encode('utf-8')
    )

    response_buffer = ctypes.create_string_buffer(4096)
    result = libpaytr.call_api(
        data.get('key', '').encode('utf-8'),
        data.get('merchant_id', '').encode('utf-8'),
        ctypes.byref(request),  # PaymentRequest yapısı
        response_buffer,  # Yanıt tamponu
        ctypes.sizeof(response_buffer)  # Tampon boyutu
    )

    return result, response_buffer.value.decode('utf-8')
