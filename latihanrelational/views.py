from django.shortcuts import render,redirect
from course.models import *
from course.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from latihanrelational.decorators import allowed_users, unauthenticated_user,admin_only
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

@login_required(login_url='login')
@admin_only
def index(request):
    context={
        "title" : "Latihan Relational",
        "subtitle" : "latihan relational database untuk CRM"
    }

    return render(request,"index.html",context)

@unauthenticated_user
def registerPage(request):
    form = createUserForm()
    course = Course.objects.all()

    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            #print(user.email)
            customer=Customer.objects.create(
                user=user,
                email=user.email,
                name=user.fullname,
                linkedin=user.linkedin,
                age=user.age
            )
            course_id=[6,3,4,7]
            for i in course_id:
                order = Order(customer=customer,product=course[i],status="On Progress")
                print(i)
                order.save()

            return redirect('login')
                #customer = Customer.objects.all()


    context={
        "form" : form,
    }
    return render(request,'course/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username or password is incorrect")

    context={}
    return render(request,'course/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def userPage(request):
    user = request.user.customer
    orders = request.user.customer.order_set.all()
    p = Paginator(orders.all(),5)
    page = request.GET.get('page')
    orderpage = p.get_page(page)
    context={
        "orders":orderpage,
        "user" :user
    }
    return render(request,"course/user.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def createOrder(request,course_id):
     courses = Course.objects.get(id=course_id)
     all_courses = Course.objects.all()
     user = request.user.customer
     orders = request.user.customer.order_set.all()
     data={
         "customer" : user,
         "product" : courses,
         "status" : "On Progress"
     }
     form = orderForm(request.POST or None, initial=data)

     order_name=[]
     for k in range(len(orders)):
        order_name.append(orders[k].product.name)
     if request.method == 'POST':
        if courses.name in order_name:
            return redirect(request.path_info)
        if form.is_valid():
            form.save()
        return redirect('allCourses')

     context = {
         'form' : form,
         'user' : user,
         "all_courses":all_courses,
         "orders":orders,
         "courses":courses,
         "action" : "take",
     }
     return render(request,'course/order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def updateOrder(request,update_id):
    order_update= Order.objects.get(id=update_id)
    user = request.user.customer
    data={
        "status":"Finished",

    }
    form = orderForm(request.POST or None ,initial=data,instance=order_update)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/user/courses')

    context = {
        'form' : form,
        'action' : "finish",
        'user' :user,
     }
    return render(request,'course/order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def allCourses(request):
    user = request.user.customer
    orders = request.user.customer.order_set.all()
    p = Paginator(orders.all(),5)
    page = request.GET.get('page')
    orderpage = p.get_page(page)
    p2 = Paginator(Course.objects.all(),5)
    coursepage = p2.get_page(page)
    order_list=[]

    for k in range(len(orders)):
        order_name = orders[k].product.name
        order_list.append(order_name)
    print(order_list)
        
    context={
        "user" : user,
        "courses" : coursepage,
        "user_courses" : orderpage,
        "order_list" :order_list,
    }
    return render(request,"course/course.html",context)