from django.contrib import admin
admin.site.site_header = "Breast Cancer detection system"
from .models import BreastCancerData,Doctor,Patient,PatientDoctor,BreastScanTestResult,PatientBreastScan
admin.site.register([BreastCancerData,Doctor,Patient,PatientDoctor,BreastScanTestResult,PatientBreastScan])