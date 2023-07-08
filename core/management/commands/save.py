import os
import django
from django.core.files import File
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from .pdf_creater import full_info_pastel
from datetime import datetime
current_time  = datetime.now()
from ...models import Pastel,Rulon

#file = File(open(latest_rulon, 'rb'))

def save_obj(data):
    latest_rulon = Rulon.objects.last().information_pastel.path
    obj = Pastel.model_field_attr(data)
    sana = f"{current_time.day}.{current_time.month}.{current_time.year}"
    if obj:
        full_info_pastel(latest_rulon,sana,data['big_pastel'],data['small_pastel'],data['nalichka'],data['gastiniy'],data['kunlik_pul'])
        return "✅"
    else:
        return "Saqlanmadi"
    

