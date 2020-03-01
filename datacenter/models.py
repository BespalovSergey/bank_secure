from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
    

    def get_duration(self):
        exit_out =timezone.now() 
        if self.leaved_at:
            exit_out = self.leaved_at
        duration = exit_out - self.entered_at

        return duration


    def format_duration(self):
        duration = self.get_duration()
        total = duration.total_seconds()
        hours = int( total/3600)
        minutes = int((total -( hours * 3600))/60)
        format_duration = '{}ч {}мин'.format(hours, minutes)  
        return format_duration  


    def is_visit_long(self, minutes=60):
        duration = self.get_duration()
        total = duration.total_seconds()
        visit_minutes = int(total/ 60)
        
        return visit_minutes > minutes      