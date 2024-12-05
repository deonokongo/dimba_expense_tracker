from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import logging
from .models import Expense
from .models import Savings
from .models import Loan
from .models import UploadedImage
from django.db.models import Sum
import json
from django.contrib.auth import logout




# Create your views here.
def home(request):
    context = {}
    return render(request,"base.html", context)

def features(request):
    context = {}
    return render(request,"features.html", context)

# @login_required
def track_expenses(request):
    
    all_expenses = Expense.objects.all()
    all_savings = Savings.objects.all()
    all_loans = Loan.objects.all()
    
    context = {'expenses': all_expenses,
               'savings': all_savings,
               'loans': all_loans 
               }
    
    return render(request,'dashboard.html',context)


#About Us Page

def about(request):
    context = {}
    return render(request,"about.html", context)

#Contact Us  Page

def contact(request):
    context = {}
    return render(request,"contact.html", context)

#Team Members Page

def team(request):
    context = {}
    return render(request,"team.html", context)

def expenses(request):
    context ={}
    return render(request,"expenses.html", context)


def savings(request):
    context ={}
    return render(request,"savings.html", context)

# def dashboard(request):
#     context ={}
#     return render(request,"dashboard.html", context)

def profile(request):
    context ={}
    return render(request,"profiles.html", context)

def loans(request):
    context ={}
    return render(request,"loans.html", context)
   

def finance_management(request):
    context = {}
    return render(request, "finance_management.html", context)

def finance_literacy(request):
    context = {}
    return render(request, "finance_literacy.html", context)

#Register a user

def register(request):
    ''' Show the registration form '''
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password == confirm_password:
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                # Create user
                try:
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password
                    )
                    # Log the user in immediately after registration
                    login(request, user)
                    messages.success(request, "Your account has been registered successfully.")
                    return redirect('dimba_app:expenses')  # Adjust redirection as needed
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Your passwords do not match!")

    return render(request, 'accounts/register.html')

#Login Page
# Set up logging
logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
import logging

# Set up logger
logger = logging.getLogger(__name__)

def login_page(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('dimba_app:dashboard')  # Or any page you want to redirect to if already logged in

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Log the inputs being passed
        logger.debug(f"Received username: {username} and password for authentication.")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        logger.debug(f"Trying to authenticate user: {username}")

        if user is not None:
            logger.info(f"Authentication successful for user: {username}")
            # Log in the user
            login(request, user)
            messages.success(request, "Login successful! Welcome back.")
            
            # Get the 'next' parameter from the URL and redirect to that page
            next_url = request.GET.get('next', 'dimba_app:dashboard')  # Default to dashboard if no next URL
            return redirect(next_url)
        else:
            logger.warning(f"Authentication failed for user: {username}")
            messages.error(request, "Invalid email or password. Please try again.")
    
    return render(request, 'accounts/login.html')



#Function to POST data to DB
def add_expense(request):
    
    if request.method == 'POST':
        
        expenses = Expense(
            name = request.POST['name'],
            category = request.POST['category'],
            amount = request.POST['amount'],
            date = request.POST['date'],
            description = request.POST['description'],
        )
        
        expenses.save()

        
        return redirect('dimba_app:dashboard')
        
    else:
        expenses = Expense.objects.all()
        return render(request, 'expense.html')

def add_saving(request):
    
    if request.method == 'POST':
        
        savings = Savings(
            name = request.POST['name'],
            type = request.POST['type'],
            amount = request.POST['amount'],
            date = request.POST['date'],
            description = request.POST['description'],
        )
        
        savings.save()
        
        return redirect('dimba_app:dashboard')
        
    else:
        return render(request, 'savings.html')


def add_loan(request):
    
    if request.method == 'POST':
        
        loans = Loan(
            name = request.POST['name'],
            category = request.POST['category'],
            amount = request.POST['amount'],
            date = request.POST['date'],
            description = request.POST['description'],
            status = request.POST['status'],
        )
        
        loans.save()
        
        return redirect('dimba_app:dashboard')
        
    else:
        return render(request, 'loans.html')
    
    #CRUD Operations

def dashboard(request):
    expenses = Expense.objects.all()
    savings = Savings.objects.all()
    loans = Loan.objects.all()
    
    # Grouped data for expenses
    all_expenses = Expense.objects.values('category').annotate(total=Sum('amount'))
    expenses_labels = [item['category'] for item in all_expenses]
    expenses_data = [item['total'] for item in all_expenses]

    # Grouped data for savings
    all_savings = Savings.objects.values('type').annotate(total=Sum('amount'))
    savings_labels = [item['type'] for item in all_savings]
    savings_data = [item['total'] for item in all_savings]

    # Grouped data for loans
    all_loans = Loan.objects.values('category').annotate(total=Sum('amount'))
    loans_labels = [item['category'] for item in all_loans]
    loans_data = [item['total'] for item in all_loans]

    # Context data for the template

    context = {
        'expenses':expenses,
        'savings': savings,
        'loans': loans,
        'expenses_labels': json.dumps(expenses_labels),
        'expenses_data': json.dumps(expenses_data),
        'savings_labels': json.dumps(savings_labels),
        'savings_data': json.dumps(savings_data),
        'loans_labels': json.dumps(loans_labels),
        'loans_data': json.dumps(loans_data),
    }
    
    return render(request, 'dashboard.html', context)



# Function to update data in the database
def update_expense(request, id):

    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':
        # Update fields with values submitted in the POST request
        expense.name = request.POST.get('name')
        expense.category = request.POST.get('category')
        expense.amount = request.POST.get('amount')
        expense.date = request.POST.get('date')
        expense.description = request.POST.get('description')
        expense.image = request.POST.get('image')
        
        # Save the updated object to the database
        expense.save()

        # Redirect to the "dashboard" page after updating
        return redirect("dimba_app:dashboard")

    # Render the update template with the expense data for GET requests
    return render(request, "update_expense.html", context={'expense': expense})


# Function to update data in the database
def update_saving(request, id):

    saving = get_object_or_404(Savings, id=id)

    if request.method == 'POST':
        # Update fields with values submitted in the POST request
        saving.name = request.POST.get('name')
        saving.type = request.POST.get('type')
        saving.amount = request.POST.get('amount')
        saving.date = request.POST.get('date')
        saving.description = request.POST.get('description')

        # Save the updated object to the database
        saving.save()

        # Redirect to the "savings" page after updating
        return redirect("dimba_app:dashboard")

    # Render the update template with the saving data for GET requests
    return render(request, "update_saving.html", context={'saving': saving})



# Function to update data in the database
def update_loan(request, id):

    loan = get_object_or_404(Loan, id=id)

    if request.method == 'POST':
        # Update fields with values submitted in the POST request
        loan.name = request.POST.get('name')
        loan.category = request.POST.get('category')
        loan.amount = request.POST.get('amount')
        loan.date = request.POST.get('date')
        loan.description = request.POST.get('description')

        # Save the updated object to the database
        loan.save()

        # Redirect to the "show_loans" page after updating
        return redirect("dimba_app:dashboard")

    # Render the update template with the loan data for GET requests
    return render(request, "update_loan.html", context={'loan': loan})



#delete data

def delete_expense(request, id):
                
    expense = Expense.objects.get(id=id)
    
    expense.delete()
        
    return redirect('dimba_app:dashboard')

def delete_saving(request, id):
                
    saving = Savings.objects.get(id=id)
    
    saving.delete()
        
    return redirect('dimba_app:dashboard')


def delete_loan(request, id):
                
    loan = Loan.objects.get(id=id)
    
    loan.delete()
        
    return redirect('dimba_app:dashboard')


def upload_image(request):
    
    if request.method == 'POST':
        
        print(request.POST)  
        print(request.FILES)
        
        uploaded_file = request.FILES['image']
        
        if not uploaded_file:
            print("Error: File is missing")
        
        if  uploaded_file:
            
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file, uploaded_file)  # Now 'uploaded_file' should be the correct file object
            file_url = fs.url(filename)
            
            image = UploadedImage.objects.create( image=filename)
            image.save()
            
            return render(request, 'upload_success.html', {'file_url': file_url})
    return render(request, 'upload_image.html')

# @login_required
def reports(request):
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_savings = Savings.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_loans = Loan.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_expenses': total_expenses,
        'total_savings': total_savings,
        'total_loans': total_loans
    }
    return render(request, 'reports.html', context)


def logout_view(request):
    logout(request)
    return redirect('dimba_app:login')