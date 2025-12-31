from django.shortcuts import render,redirect
from .models import Expense,Category
from .forms import ExpenseForm,CategoryForm,UserForm
from django.db.models import Sum
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout


def login(request):
    errors=""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')  # or dashboard
        else:
            errors="Invalid username or password"

    return render(request, 'login.html',{'errors':errors})

def logout(request):
    if request.user:
        auth_logout(request)

    return redirect('login')

def signup(request):
    errors=""
    if request.method=="POST":        
        form=UserForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            errors=form.errors
    else:
        form=UserForm()
    return render(request,'signup.html',{'errors':errors})


def home(request):
    if request.user.is_authenticated:
        return render(request,'base.html')
    else:
        return redirect('login')

# add category view
def add_category(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            category=form.save(commit=False)
            category.user=request.user
            category.save()
        return redirect('add-category')
    categories=Category.objects.filter(user=request.user)
    message="No Categories Found"
    form=CategoryForm()
    return render(request,'Expense/add_category.html',{'form':form,'categories':categories,'message':message})

        

#add expense view
def add_expense(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        form=ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user   
            expense.save()
        return redirect('expense-list')
    else:
        form=ExpenseForm()

    form.fields['category'].queryset=Category.objects.filter(user=request.user)
    return render(request,'Expense/add_expense.html',{'form':form})


# expenses list view

def expense_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    categories=Category.objects.filter(user=request.user)
    expenses=Expense.objects.filter(user=request.user).order_by('-date')
    from_date=None
    to_date=None
    if request.method=="POST":
        selected_category=request.POST.get('category')
        from_date=request.POST.get('from_date')
        to_date=request.POST.get('to_date')
        if selected_category and selected_category != "all":
            expenses = expenses.filter(category_id=selected_category)

        if from_date and to_date:
            expenses=expenses.filter(date__range=[from_date,to_date])

        elif from_date:
            expenses = expenses.filter(date__gte=from_date)

        elif to_date:
            expenses = expenses.filter(date__lte=to_date)
  
    total= expenses.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    return render(request,'Expense/expenses.html',{'expenses':expenses,'total_amount':total,'categories':categories})

def delete_expense(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    expense = Expense.objects.filter(id=id, user=request.user).first()
    if not expense:
        return redirect('expense-list')  # or show error

    expense.delete()
    return redirect('expense-list')
