from django.db import models

from patient.models import PatientComeHistory
from user.models import Clinic, User


# Create your models here.

class Params0To20(models.Model):
    param = models.CharField(max_length=6)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.param


OD = 0
OS = 1

EYE_CHOICES = (
    (OD, "OD"),
    (OS, "OS"),
)


class Visus(models.Model):
    bk = models.ForeignKey(Params0To20, on_delete=models.CASCADE, related_name='bk_set')
    eye = models.IntegerField(verbose_name="Qaysi ko'z?", choices=EYE_CHOICES, default=OD, null=True, blank=True)
    cd = models.ForeignKey(Params0To20, on_delete=models.CASCADE, related_name='cd_set')
    sph = models.FloatField(default=0)
    cyl = models.FloatField(default=0)
    ax = models.IntegerField(default=0)
    bliz = models.CharField(max_length=20)
    ck = models.ForeignKey(Params0To20, on_delete=models.CASCADE, related_name='ck_set')
    patient_come_history = models.ForeignKey(PatientComeHistory, on_delete=models.CASCADE,
                                             related_name='visus_to_patient_come_history')
    created_date = models.DateTimeField(auto_now_add=True)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.patient_come_history} | {self.get_eye_display()}"


class Complaint(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Eyelids(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Eyeball(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Conjunctiva(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Сornea(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class FrontCamera(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PupilOfTheEye(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Lens(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class VitreousBody(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class OcularFundus(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Diagnosis(models.Model):
    title = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class OphthalmologyStatus(models.Model):
    patient_come_history = models.ForeignKey(PatientComeHistory, on_delete=models.CASCADE,
                                             related_name='ophth_to_patient_come_history')
    eye = models.IntegerField(verbose_name="Qaysi ko'z?", choices=EYE_CHOICES, default=OD, null=True, blank=True)
    anamnesis = models.CharField(max_length=255)
    allergy = models.BooleanField(default=False)
    complaints = models.ManyToManyField(Complaint)
    eyelids = models.ManyToManyField(Eyelids)
    eyeball = models.ManyToManyField(Eyeball)
    conjunctiva = models.ManyToManyField(Conjunctiva)
    cornea = models.ManyToManyField(Сornea)
    front_camera = models.ManyToManyField(FrontCamera)
    zrachok = models.ManyToManyField(PupilOfTheEye)
    lens = models.ManyToManyField(Lens)
    vitreous_body = models.ManyToManyField(VitreousBody)
    ocular_fundus = models.ManyToManyField(OcularFundus)
    hour_indicator = models.CharField(max_length=2, default='0')
    diagnosis = models.ManyToManyField(Diagnosis)
    is_operation = models.BooleanField(default=False)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient_come_history}"
