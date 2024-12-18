# Import necessary Django modules and models
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import AgentCode
from .forms import LoginForm, RegistrationForm, ListingForm
import random
import string
from django.db import transaction, IntegrityError
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from cart.models import Listing

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Listing  # Assuming Listing is the cart_listing model
from django.contrib import messages

@staff_member_required
def admin_dashboard(request):
    listings = Listing.objects.all()  # Fetch all listings
    return render(request, 'admin_dashboard.html', {'listings': listings})

@staff_member_required
def remove_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.delete()
    messages.success(request, 'Listing removed successfully.')
    return redirect('admin_dashboard')
# Custom login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            admin_code = form.cleaned_data.get('admin_code')  # Allow admin_code to be optional

            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_superuser:  # Allow superuser to log in without admin_code
                    login(request, user)
                    return redirect('admin_dashboard')  # Redirect superusers to admin_dashboard
                else:
                    try:
                        # Check if the user has a valid and approved admin_code
                        agent_code = AgentCode.objects.get(user=user, code=admin_code, approved=True)
                        login(request, user)
                        return redirect('hello_world')
                    except AgentCode.DoesNotExist:
                        form.add_error(None, 'Invalid admin code or unapproved user.')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
# User registration view
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            AgentCode.objects.create(user=user, code='PendingApproval', approved=False)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Function to generate a unique admin code
def generate_unique_code():
    """Generates a unique 10-character admin code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@user_passes_test(lambda u: u.is_superuser)
def approve_users(request):
    pending_users = AgentCode.objects.filter(approved=False)

    if request.method == 'POST':
        user_id = request.POST.get("user_id")

        if user_id:
            try:
                with transaction.atomic():
                    # Lock the related User row for update
                    user = User.objects.select_for_update().get(id=user_id)

                    # Get or create the AgentCode instance for this user
                    agent_code, created = AgentCode.objects.get_or_create(user=user)

                    # Ensure the generated code is unique
                    code_is_unique = False
                    while not code_is_unique:
                        unique_code = generate_unique_code()

                        # Check uniqueness in the database
                        if not AgentCode.objects.filter(code=unique_code).exists():
                            agent_code.code = unique_code
                            agent_code.approved = True
                            agent_code.save()
                            code_is_unique = True

                    # Send the email to the user
                    send_mail(
                        subject='Your Admin Code Approval',
                        message=f'Hello {user.username},\n\n'
                                f'Your account has been approved. Here is your admin code: {unique_code}\n\n'
                                'Please use this code for login.\n\n'
                                'Best regards,\nAdmin Team',
                        from_email= 'footballoutlash@gmail.com',
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    print(f"Generated unique admin code for {user.username}: {unique_code}")

            except User.DoesNotExist:
                print("User not found.")
            except IntegrityError as e:
                print(f"Integrity error occurred: {e}")

    return render(request, 'approve_users.html', {'pending_users': pending_users})

# Placeholder for hello world view
@login_required
def hello_world(request):
    return render(request, 'hello_world.html')


from django.shortcuts import render, redirect
from django.contrib import messages  # Add for displaying messages to the user
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ListingForm

@staff_member_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()  # Save the data if the form is valid
            messages.success(request, 'Listing added successfully!')  # Success message
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
        else:
            # Log the form errors to help debug the issue
            print(form.errors)  # Print errors to the console for debugging
            messages.error(request, 'Please correct the errors below.')  # Display an error message in the form
    else:
        form = ListingForm()

    return render(request, 'add_listing.html', {'form': form})
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout