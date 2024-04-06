from django.shortcuts import redirect
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from django.shortcuts import render
from .forms import BreastDataForm
from django.http import HttpResponse
from .models import BreastCancerData 
csv_file_path = 'data/breast_cancer_dataset.csv'
csv_file_path1 = os.path.join(os.path.dirname(__file__), csv_file_path)
data = pd.read_csv(csv_file_path1)
# tables is created using pandas data frame
doctor_table = pd.DataFrame(columns=['name', 'Did', 'speciality'])
patient_table = pd.DataFrame(columns=['patient_id', 'most_likely_diagnosis', 'date'])
patient_doctor_table = pd.DataFrame(columns=['Pid', 'Did', 'Prescribed_test', 'Test_date'])
breast_scan_test_table = pd.DataFrame(columns=['Test_id', 'Did', 'Pid', 'Test_Type', 'date'])
patient_breast_scan_table = pd.DataFrame(columns=['Pid', 'Did', 'Test_id', 'Breast_attributes', 'Test_Status'])

def standardize_data(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    standardized_X = (X - mean) / std
    return standardized_X

# first Standardize the attributes of the breast dataset and we have to drop diagnosis column
X = data.drop(columns=['diagnosis'])
X_standardized = standardize_data(X)


# use sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, learning_rate=0.01, num_iterations=1000):
    num_samples, num_features = X.shape
       
    theta = np.zeros(num_features)
    
    for _ in range(num_iterations):
        # Calculate the hypothesis and the gradient
        z = np.dot(X, theta)
        h = sigmoid(z)
        gradient = np.dot(X.T, (h - y)) / num_samples
        
        # Update the parameters (theta)
        theta -= learning_rate * gradient
    
    return theta

# Add bias term to the input features
X_bias = np.c_[np.ones((X_standardized.shape[0], 1)), X_standardized]

# Convert diagnosis labels to binary (0: Benign, 1: Malignant)
y = data['diagnosis'].map({'M': 1, 'B': 0}).values

# Train the logistic regression model
coefficients = logistic_regression(X_bias, y)

def predict(X, coefficients):
    X_bias = np.c_[np.ones((X.shape[0], 1)), X]
    z = np.dot(X_bias, coefficients)
    return sigmoid(z)

def logistic_regression_model(X, coefficients):
    X_bias = np.c_[np.ones((X.shape[0], 1)), X]
    z = np.dot(X_bias, coefficients)
    return sigmoid(z)

def predict_diagnosis(request,id):
    data = BreastCancerData.objects.get(id=id)
   
    input_data = {
        'id':data.id,
        'radius_mean': data.radius_mean,
        'texture_mean':data.texture_mean,
        'perimeter_mean': data.perimeter_mean,
         'area_mean':data.area_mean, 
         'smoothness_mean':data.smoothness_mean,
        'compactness_mean':data.compactness_mean, 
        'concavity_mean':data.concavity_mean, 
        'concave_points_mean':data.concave_points_mean, 
        'symmetry_mean':data.symmetry_mean,
        'fractal_dimension_mean':data.fractal_dimension_mean, 
        'radius_se':data.radius_se, 
        'texture_se':data.texture_se, 
        'perimeter_se':data.perimeter_se, 
        'area_se':data.area_se,
        'smoothness_se':data.smoothness_se, 
        'compactness_se':data.compactness_se, 
        'concavity_se':data.concavity_se, 
        'concave_points_se':data.concave_points_se, 
        'symmetry_se':data.symmetry_se,
        'fractal_dimension_se':data.fractal_dimension_se, 
        'radius_worst':data.radius_worst,
        'texture_worst':data.texture_worst, 
        'perimeter_worst':data.perimeter_worst, 
        'area_worst':data.area_worst,
        'smoothness_worst':data.smoothness_worst, 
        'compactness_worst':data.compactness_worst,
        'concavity_worst':data.concavity_worst,
        'concave_points_worst':data.concave_points_worst,
        'symmetry_worst':data.symmetry_worst, 
        'fractal_dimension_worst':data.fractal_dimension_worst
    }
    # Create a DataFrame from the input data
    input_df = pd.DataFrame([input_data])

    # Standardize the input data using the same mean and std as the training data
    input_standardized = standardize_data(input_df)

    # Get the logistic regression prediction
    prediction = predict(input_standardized, coefficients)[0]
    print(f"Prediction: {prediction}")

    # Convert the prediction to a diagnosis label
    predicted_diagnosis = 'The case is Malignant(M)' if prediction >= 0.5 else  'The case is Benign(B)'
    
    # Render the template with the prediction result
    return render(request, 'result_template.html', {'predicted_diagnosis': predicted_diagnosis})


def data_input(request):
    if request.method == 'POST':
        form = BreastDataForm(request.POST)
        if form.is_valid():
            data1 = form.cleaned_data['radius_mean']
            # Save the form data to the database
            form.save()
            return redirect('check_status')
    else:
        form = BreastDataForm()

    return render(request, 'data.html', {'form': form})


def check_status(request):
    all_data = BreastCancerData.objects.all()
    return render(request,'patient_records.html',{'all_data':all_data})