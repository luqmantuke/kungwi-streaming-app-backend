import json

import requests
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def send_sms_message(phone_number, message):
    url = "https://kuzabusiness.invict.site/Api/v2"

    payload = {"code":149,
 "api":110,
 "data":{
     "operator_id": "878b8229e6b54ec08a94d399f8fd726c",
      "phone_number": f'{phone_number}',
      "message": f'{message}'
}}

    response = requests.post(url, data=json.dumps(payload))
    if response.status_code == 200:
        response_string = response.text
        print(response_string)
        return json.loads(response_string)
    else:
        print(response.status_code)
        response_string = response.text
        print(response_string)

        pass  # handle error case
