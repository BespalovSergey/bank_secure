from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    non_closed_visits = []
    visits = Visit.objects.filter(leaved_at= None)

    for visit in visits:
        duration = visit.format_duration()
        not_closed_visit = {
            "who_entered": visit.passcard.owner_name,
            "entered_at": visit.entered_at,
            "duration": duration
        }
        non_closed_visits.append(not_closed_visit)

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }

    return render(request, 'storage_information.html', context)
