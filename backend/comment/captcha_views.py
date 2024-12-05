from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

@api_view(http_method_names=["GET"])
def get_captcha(request) -> Response:
    new_key = CaptchaStore.generate_key()
    image_url = captcha_image_url(new_key)
    return Response({"key": new_key, "image_url": image_url})


@api_view(http_method_names=["POST"])
def validate_captcha(request: Request) -> Response:
    captcha_key = request.data.get("captcha_0")
    captcha_response = request.data.get("captcha_1").lower()
    print(captcha_response)
    if not CaptchaStore.objects.filter(
        hashkey=captcha_key, response=captcha_response
    ).exists():
        return Response({"captcha": "Invalid CAPTCHA"}, status=400)

    return Response({"messages": "CAPCHA is valid"})
