from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def passcard_info_view(request, passcode):
    try:
        passcard = Passcard.objects.get(passcode= passcode)
    except ObjectDoesNotExist:
        print('Объект с кодом ({}) не найден'.format(passcode)) 
    except MultipleObjectsReturned:
        print('Найдено несколько объектов с кодом ({})'.format(passcode)) 
            
    visits = Visit.objects.filter(passcard= passcard, leaved_at__isnull= False)
    this_passcard_visits = []
    
    for visit in visits:
        this_passcard_visit = {
             "entered_at": visit.entered_at,
            "duration": visit.format_duration(),
            "is_strange": visit.is_visit_long()
        }
        this_passcard_visits.append(this_passcard_visit)  

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }

    return render(request, 'passcard_info.html', context)
