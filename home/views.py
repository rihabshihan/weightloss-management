from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import AddWeightForm
from .models import WeightEntry
from django.core.paginator import Paginator
from datetime import date
from django.http import JsonResponse

# Home page view
def home_page(request):
    return render(request, 'home.html')  # Render 'home.html' template

# About page view
def about(request):
    return render(request, 'about.html')  # Render 'about.html' template

# Signup page view (register new user)
def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            # Print form errors to the console for debugging
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login page view
def login_page(request):
    if request.method == 'POST':  # If the form is submitted
        form = AuthenticationForm(data=request.POST)  # Create form with POST data
        if form.is_valid():  # If form data is valid
            user = form.get_user()  # Get the user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home page after login
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = AuthenticationForm()  # Create an empty form if GET request
    return render(request, 'login.html', {'form': form})  # Render the login template with the form

# Logout page view (only accessible if logged in)
@login_required
def logout_page(request):
    if request.method == 'POST':  # If the form is submitted
        logout(request)  # Log the user out
        return redirect('login')  # Redirect to login page after logout
    
    return render(request, 'logout.html', {'user': request.user})  # Render logout page with the user info

# Add weight page view (only accessible if logged in)
@login_required
def addWeight(request):
    today = date.today()  # Get today's date
    existing_entry = WeightEntry.objects.filter(user=request.user, date=today).first()  # Check if the user already added weight today
    if request.method == 'POST':  # If the form is submitted
        form = AddWeightForm(request.POST)  # Create form instance with POST data
        if form.is_valid():  # If form data is valid
            if existing_entry:  # If the user already added weight today
                return render(request, 'addweight.html', {
                    'form': form,
                    'error': 'You have already added your weight for today.'  # Show error message
                })
            weight_entry = form.save(commit=False)  # Create the weight entry without saving it yet
            weight_entry.user = request.user  # Set the user
            weight_entry.date = today  # Set the date as today's date
            weight_entry.save()  # Save the weight entry
            return render(request, 'success.html', {'success': 'Your weight was added successfully'})  # Render success page
    else:
        form = AddWeightForm()  # Create an empty form if GET request
    return render(request, 'addweight.html', {'form': form, 'error': existing_entry and 'You have already added your weight for today.'})  # Render add weight page

# Retrieve all weight entries for the user
@login_required
def addedWeight(request):
    weight_list = WeightEntry.objects.filter(user=request.user)  # Get all weight entries for the logged-in user
    return render(request, 'retrieve.html', {'weight_list': weight_list})  # Render the retrieve page with the weight entries

# Update weight entry (only accessible if logged in)
@login_required
def weight_update(request, pk):
    weight = get_object_or_404(WeightEntry, pk=pk)  # Get the weight entry with the given primary key (pk), or return a 404 if not found
    
    if request.method == 'POST':  # If the form is submitted
        form = AddWeightForm(request.POST, instance=weight)  # Create form instance with POST data and existing weight entry
        if form.is_valid():  # If form data is valid
            form.save()  # Save the updated weight entry
            return redirect('home')  # Redirect to home page after successful update
    else:
        form = AddWeightForm(instance=weight)  # Create a form with the current weight entry data if GET request
    
    return render(request, 'update.html', {'form': form})  # Render the update page with the form

# Delete weight entry (only accessible if logged in)
@login_required
def weight_delete(request, pk):
    weight = get_object_or_404(WeightEntry, pk=pk)  # Get the weight entry with the given primary key (pk), or return a 404 if not found
    if request.method == 'POST':  # If the form is submitted
        weight.delete()  # Delete the weight entry
        return redirect('home')  # Redirect to home page after successful deletion
    
    return render(request, 'delete.html', {'weight': weight})  # Render the delete page with the weight entry data

# List weight entries with pagination (only accessible if logged in)
@login_required
def weight_list(request):
    weight_entries = WeightEntry.objects.filter(user=request.user)  # Get all weight entries for the logged-in user
    paginator = Paginator(weight_entries, 3)  # Paginate the weight entries, 3 entries per page
    page_number = request.GET.get('page')  # Get the current page number from the GET request
    page_obj = paginator.get_page(page_number)  # Get the page object with the paginated entries
    return render(request, 'weight_list.html', {'page_obj': page_obj})  # Render the weight list page with the paginated entries

# Weight loss calculator view (only accessible if logged in)
@login_required
def weight_loss_calculator(request):
    if request.method == 'POST':  # If the form is submitted
        start_date = request.POST.get('start_date')  # Get the start date from the form
        end_date = request.POST.get('end_date')  # Get the end date from the form

        print(f"Start Date: {start_date}")  # Print the start date for debugging
        print(f"End Date: {end_date}")  # Print the end date for debugging

        try:
            start_weight = WeightEntry.objects.get(user=request.user, date=start_date)  # Get the weight entry for the start date
            end_weight = WeightEntry.objects.get(user=request.user, date=end_date)  # Get the weight entry for the end date

            weight_loss = start_weight.weight - end_weight.weight  # Calculate the weight loss
            return JsonResponse({'weight_loss': weight_loss})  # Return the weight loss as JSON response
        except WeightEntry.DoesNotExist:
            return JsonResponse({'error': 'Weight data not available for the selected dates'}, status=400)  # Return error if data not found for the selected dates

    return render(request, 'weight_loss_calculator.html')  # Render the weight loss calculator page
