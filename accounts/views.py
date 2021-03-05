from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse

# Create your views here.
from accounts.models import *
from accounts.forms import OrderForm , CreateUserForm


#Rest Framework
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from .serializers import ProductSerializer

from django.contrib.auth import authenticate , login , logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    orders=Order.objects.all()
    custumers=Custumer.objects.all()

    total_orders=orders.count()
    total_custumers=custumers.count()
    total_delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context={'orders':orders,'custumers':custumers,'total_orders':total_orders,
             'total_custumers':total_custumers,'total_delivered':total_delivered,'pending':pending}

    return render(request  ,'accounts/dashbooard.html ',context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
def custumer(request,pk_test):
    custumer= Custumer.objects.get(id=pk_test)
    orders= custumer.order_set.all()
    order_count= orders.count()

    context= {'custumer' : custumer, 'orders':orders,'order_count':order_count}
    return render(request,'accounts/custumer.html',context)

@login_required(login_url='login')
def createOrder(request):

    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return  redirect("/")

    context = {'form':form}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
def updateOrder (request,pk):
    order= Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return  redirect('/')

    context= {'form' : form}
    return render(request, 'accounts/order_form.html',context)


@login_required(login_url='login')
def deleteOrder(request,pk):
    order= Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request,'accounts/delete.html',context)



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account was created for ' + user)
                return redirect("login")

        context= {'form':form}
        return render(request,'accounts/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or password is incorrect')

        context={}
        return  render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return  render(request,'accounts/login.html')

@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'List':'/product_list',
        'Detail-View':'/product_detail/<str:pk>',
        'Create':'/product_create',
        'Update':'/product_update/<str:pk>',
        'Delete':'/product_delete/<str:pk>'
    }

    return Response(api_urls)

@api_view(['GET'])
def productList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productDetail(request,pk):
    products = Product.objects.get(id=pk)
    serializer = ProductSerializer(products, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def productCreate(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def productUpdate(request,pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance=product,data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def productDelete(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()

    return Response('Item successfully deleted!')