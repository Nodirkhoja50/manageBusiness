from django.shortcuts import render
from django.http import HttpResponse
from .models import Rulon
from .models import Pastel
# Create your views here.


def son(request):
        """
        Returns a UUID-based 'random' and unique username.

        This is required data for user models with a username field.
        """
        
        obj = Rulon.create_rulon_obj(30)
        '''obj = Pastel.model_field_attr('big_pastel')'''
        return HttpResponse(obj)

def _togri_kiritildimi(ht):
       pass
    






