from django.urls import path
from diagnostic.views import VisusCreateView, VisusPatientDetailView, PatientComeListActiveView, ComplaintCreateView, \
    OphthalmologyStatusCreateView, EyelidsCreateView, ComplaintListView, ComplaintUpdateView, ComplaintDeleteView, \
    EyelidsListView, EyelidsUpdateView, EyelidsDeleteView, EyeballListView, EyeballCreateView, EyeballUpdateView, \
    EyeballDeleteView, ConjunctivaListView, ConjunctivaCreateView, ConjunctivaUpdateView, ConjunctivaDeleteView, \
    СorneaListView, СorneaCreateView, СorneaUpdateView, СorneaDeleteView, FrontCameraListView, FrontCameraCreateView, \
    FrontCameraUpdateView, FrontCameraDeleteView, PupilOfTheEyeListView, PupilOfTheEyeCreateView, \
    PupilOfTheEyeUpdateView, PupilOfTheEyeDeleteView, LensListView, LensCreateView, LensUpdateView, LensDeleteView, \
    VitreousBodyListView, VitreousBodyCreateView, VitreousBodyUpdateView, VitreousBodyDeleteView, OcularFundusListView, \
    OcularFundusCreateView, OcularFundusUpdateView, OcularFundusDeleteView, DiagnosisListView, DiagnosisCreateView, \
    DiagnosisUpdateView, DiagnosisDeleteView, OphthalmologyStatusDetailView, OperationView, \
    OphthalmologyStatusListNowHave

app_name = 'diagnostic'

urlpatterns = [
    path('patient-come/', PatientComeListActiveView.as_view(), name='patient-come'),
    path('patient-come-now-doctor/', OphthalmologyStatusListNowHave.as_view(), name='patient-come-now-doctor'),
    path('create-optic/<int:come_history_id>', OphthalmologyStatusCreateView.as_view(), name='create-optic'),
    path('create-visus/<int:come_history_id>', VisusCreateView.as_view(), name='create-visus'),
    path('detail-visus/<int:pk>', VisusPatientDetailView.as_view(), name='detail-visus'),
    path('detail-optic/<int:pk>', OphthalmologyStatusDetailView.as_view(), name='detail-optic'),
    path('operation/', OperationView.as_view(), name='operation'),

    path('complaints/', ComplaintListView.as_view(), name='complaints'),
    path('complaint-create/', ComplaintCreateView.as_view(), name='complaint-create'),
    path('complaint-update/<int:pk>', ComplaintUpdateView.as_view(), name='complaint-update'),
    path('complaint-delete/<int:pk>', ComplaintDeleteView.as_view(), name='complaint-delete'),

    path('eyelids/', EyelidsListView.as_view(), name='eyelids'),
    path('eyelid-create/', EyelidsCreateView.as_view(), name='eyelid-create'),
    path('eyelid-update/<int:pk>', EyelidsUpdateView.as_view(), name='eyelid-update'),
    path('eyelid-delete/<int:pk>', EyelidsDeleteView.as_view(), name='eyelid-delete'),

    path('eyeballs/', EyeballListView.as_view(), name='eyeballs'),
    path('eyeball-create/', EyeballCreateView.as_view(), name='eyeball-create'),
    path('eyeball-update/<int:pk>', EyeballUpdateView.as_view(), name='eyeball-update'),
    path('eyeball-delete/<int:pk>', EyeballDeleteView.as_view(), name='eyeball-delete'),

    path('conjunctiva/', ConjunctivaListView.as_view(), name='conjunctivas'),
    path('conjunctiva-create/', ConjunctivaCreateView.as_view(), name='conjunctiva-create'),
    path('conjunctiva-update/<int:pk>', ConjunctivaUpdateView.as_view(), name='conjunctiva-update'),
    path('conjunctiva-delete/<int:pk>', ConjunctivaDeleteView.as_view(), name='conjunctiva-delete'),

    path('corneas/', СorneaListView.as_view(), name='corneas'),
    path('cornea-create/', СorneaCreateView.as_view(), name='cornea-create'),
    path('cornea-update/<int:pk>', СorneaUpdateView.as_view(), name='cornea-update'),
    path('cornea-delete/<int:pk>', СorneaDeleteView.as_view(), name='cornea-delete'),

    path('front-cameras/', FrontCameraListView.as_view(), name='front-cameras'),
    path('front-camera-create/', FrontCameraCreateView.as_view(), name='front-camera-create'),
    path('front-camera-update/<int:pk>', FrontCameraUpdateView.as_view(), name='front-camera-update'),
    path('front-camera-delete/<int:pk>', FrontCameraDeleteView.as_view(), name='front-camera-delete'),

    path('pupil-of-the-eye/', PupilOfTheEyeListView.as_view(), name='pupil-of-the-eye'),
    path('pupil-of-the-eye-create/', PupilOfTheEyeCreateView.as_view(), name='pupil-of-the-eye-create'),
    path('pupil-of-the-eye-update/<int:pk>', PupilOfTheEyeUpdateView.as_view(), name='pupil-of-the-eye-update'),
    path('pupil-of-the-eye-delete/<int:pk>', PupilOfTheEyeDeleteView.as_view(), name='pupil-of-the-eye-delete'),

    path('lens/', LensListView.as_view(), name='lens'),
    path('lens-create/', LensCreateView.as_view(), name='lens-create'),
    path('lens-update/<int:pk>', LensUpdateView.as_view(), name='lens-update'),
    path('lens-delete/<int:pk>', LensDeleteView.as_view(), name='lens-delete'),

    path('vitreous-body/', VitreousBodyListView.as_view(), name='vitreous-body'),
    path('vitreous-body-create/', VitreousBodyCreateView.as_view(), name='vitreous-body-create'),
    path('vitreous-body-update/<int:pk>', VitreousBodyUpdateView.as_view(), name='vitreous-body-update'),
    path('vitreous-body-delete/<int:pk>', VitreousBodyDeleteView.as_view(), name='vitreous-body-delete'),

    path('ocular-fundus/', OcularFundusListView.as_view(), name='ocular-fundus'),
    path('ocular-fundus-create/', OcularFundusCreateView.as_view(), name='ocular-fundus-create'),
    path('ocular-fundus-update/<int:pk>', OcularFundusUpdateView.as_view(), name='ocular-fundus-update'),
    path('ocular-fundus-delete/<int:pk>', OcularFundusDeleteView.as_view(), name='ocular-fundus-delete'),

    path('diagnosis/', DiagnosisListView.as_view(), name='diagnosis'),
    path('diagnosis-create/', DiagnosisCreateView.as_view(), name='diagnosis-create'),
    path('diagnosis-update/<int:pk>', DiagnosisUpdateView.as_view(), name='diagnosis-update'),
    path('diagnosis-delete/<int:pk>', DiagnosisDeleteView.as_view(), name='diagnosis-delete'),
]
