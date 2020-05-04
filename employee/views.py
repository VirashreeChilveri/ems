from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from employee.forms import UserForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from ems.decorators import admin_hr_required,admin_only
from django.views.generic import DetailView,ListView
from django.views.generic.edit import UpdateView,CreateView

# Create your views here.

@login_required(login_url="/login/")
def employee_list(request):
    print(request.role)
    context={}
    context['users']=User.objects.all()
    context['title']='Employees'
    return render(request,'employees/index.html',context)

@login_required(login_url="/login/")
def employee_details(request,id=None):
    context={}   
    context['title']='Employee details' 
    context['user']=get_object_or_404(User,id=id)
    return render(request,'employees/details.html',context)

@login_required(login_url="/login/")
# @role_required(allowed_roles=['Admin','HR'])
@admin_only
def employee_add(request):
    context={}

    # if request.role=='Admin':
    if request.method=="POST":
        user_form=UserForm(request.POST)
        context['user_form']=user_form

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request,'employees/add.html/',context)  
    else:
        user_form=UserForm()          
        context['user_form']=user_form
        return render(request,'employees/add.html/',context) 
    # else:
    #     return HttpResponseRedirect(reverse('employee_list'))

@login_required(login_url="/login/")
def employee_edit(request,id=None):
    user=get_object_or_404(User,id=id)

    if request.method=="POST":
        user_form=UserForm(request.POST,instance=user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))       
        else:        
            return render(request,'employees/edit.html',{'user_form':user_form})

    else:
        user_form=UserForm(instance=user)        
        return render(request,'employees/edit.html',{'user_form':user_form})

@login_required(login_url="/login/")
def employee_delete(request,id=None):
    user=get_object_or_404(User,id=id)

    if request.method=="POST":
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))

    else:
        context={}    
        context['user']=user
        return render(request,'employees/delete.html',context)

def user_login(request):
    context={}

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        
        if user:
            login(request,user)

            if request.GET.get('next',None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context['error']='Provide valid credentials!!'
            return render(request,'auth/login.html',context)

    else:
        return render(request,'auth/login.html',context)   

def user_success(request):
    context={}         
    context['user']=request.user
    return render(request,'auth/success.html',context)

def user_logout(request):
    # if request.method=="POST":
    logout(request) 
    return HttpResponseRedirect(reverse('user_login'))

class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.profile



class MyProfile(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        return self.request.user.profile      
                     


