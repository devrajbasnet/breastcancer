from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    Did = models.CharField(max_length=10, unique=True)
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    most_likely_diagnosis = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.patient_id} - {self.most_likely_diagnosis}"

class PatientDoctor(models.Model):
    Pid = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Did = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    prescribed_test = models.CharField(max_length=100)
    test_date = models.DateField()

    def __str__(self):
        return f"{self.Pid} - {self.Did}"

class BreastScanTestResult(models.Model):
    test_id = models.AutoField(primary_key=True)
    Did = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Pid = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.test_id} - {self.Did} - {self.Pid}"
    

class BreastCancerData(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=200,default="TestPatient")
    radius_mean = models.FloatField()
    texture_mean = models.FloatField()
    perimeter_mean = models.FloatField()
    area_mean = models.FloatField()
    smoothness_mean = models.FloatField()
    compactness_mean = models.FloatField()
    concavity_mean = models.FloatField()
    concave_points_mean = models.FloatField()
    symmetry_mean = models.FloatField()
    fractal_dimension_mean = models.FloatField()
    radius_se = models.FloatField()
    texture_se = models.FloatField()
    perimeter_se = models.FloatField()
    area_se = models.FloatField()
    smoothness_se = models.FloatField()
    compactness_se = models.FloatField()
    concavity_se = models.FloatField()
    concave_points_se = models.FloatField()
    symmetry_se = models.FloatField()
    fractal_dimension_se = models.FloatField()
    radius_worst = models.FloatField()
    texture_worst = models.FloatField()
    perimeter_worst = models.FloatField()
    area_worst = models.FloatField()
    smoothness_worst = models.FloatField()
    compactness_worst = models.FloatField()
    concavity_worst = models.FloatField()
    concave_points_worst = models.FloatField()
    symmetry_worst = models.FloatField()
    fractal_dimension_worst = models.FloatField()

    def __str__(self):
        return f"ID: {self.id}"


class PatientBreastScan(models.Model):
    Pid = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Did = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    test_id = models.ForeignKey(BreastScanTestResult, on_delete=models.CASCADE)
    breast_attributes = models.OneToOneField(BreastCancerData,on_delete=models.CASCADE)
    test_status = models.CharField(max_length=100,default=None)

    def __str__(self):
        return f"{self.Pid} - {self.Did} - {self.test_id}"
   


   