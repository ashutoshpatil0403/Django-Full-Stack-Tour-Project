from django.shortcuts import render,HttpResponse,redirect
from .models import packages,user_booking,Places
from django.db.models import Q
from django.contrib import messages
# Create your views here.
from django.views.generic import CreateView
from django.urls import reverse_lazy
def home(request):
    package_obj = None
    if 'package_obj' in request.session:
        package_obj_serialized = request.session['package_obj']
        package_obj = list(serializers.deserialize('json', package_obj_serialized))
    return render(request, 'home.html', {'package_obj': package_obj})

class imgadd(CreateView):
    template_name='nav.html'
    model=user_booking
    fields=['user_img']
    context_object_name = 'object'
    success_url=reverse_lazy('/')


def package(request):
    data=packages.objects.all()
    
    return render(request,'package.html',{"object_list":data})

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,'contact.html')

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import SignupForm
from django.contrib.auth import authenticate,login,logout
from django.core import serializers

def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registered Successfully ! Login to Continue')
            return redirect('login')
    else:
        form = SignupForm()
    # messages.success(request,'Registered failed')
    return render(request, 'signup.html', {'form': form})
import json
def user_login(request):
    if request.method == 'POST':
        ul = AuthenticationForm(request=request, data=request.POST)
        
        if ul.is_valid():
            uname = ul.cleaned_data['username']
            upass = ul.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful!')
                package_obj=packages.objects.all()
                package_obj_serialized = serializers.serialize('json', package_obj)
                # Store the serialized data in the session
                request.session['package_obj'] = package_obj_serialized
                return redirect('/')  # Redirect to packages page after successful login
            else:
                messages.error(request, 'Invalid Username or Password!')
        else:
            messages.error(request, 'Invalid Form Submission!')
    else:
        ul = AuthenticationForm()  # Create an empty form for GET requests
    return render(request, 'login.html', {'form': ul})

def search_package_view(request):
    try:
        if request.method == 'POST':
            searching_date = request.POST.get("searching_date")
            searching_pickup = request.POST.get("searching_pickup")
            pak = request.POST.get("pak")

            available_package = packages.objects.filter(pk=pak).first()

            matching_place = Places.objects.filter(place_name=searching_pickup).first()

            booked_packages = user_booking.objects.filter(package_id__pk=pak, travel_date=searching_date)
            booked_packages_place=booked_packages.filter(from_place=matching_place)

            print(booked_packages_place.count())

            if available_package:
                if int(available_package.seats) > booked_packages.count():
                    if matching_place and int(available_package.seats) > booked_packages_place.count():
                        return render(request, 'package.html', {"object_list": [available_package]})
                    else:
                        messages.error(request, 'Package unavailable on Entered Pickup!.')
                        return redirect('/')
                else:
                    messages.error(request, 'Package unavailable on selected date!.')
                    return redirect('/')
            else:
                messages.error(request, 'Package not found')
                return redirect('/')
        else:
            package_obj = packages.objects.all()
            return render(request, 'package_search.html', {'package_obj': package_obj})
    except Exception as e:
        print(e)
        return HttpResponse(e)



def user_logout(request):
    if  request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logout Successfully ! ')
    return redirect('login')

from django.views.generic import View ,ListView
from django.db.models import Q

class search(ListView):
    model=packages
    template_name='package.html'
    context_object_name='POST'
    def get_queryset(self):
        ser = self.request.GET.get('search')
        object=packages.objects.filter(Q(p1_name__icontains=ser) | Q(p1_price__icontains=ser)) 
        return object
    
# class select_package(View):
#     def get(self, request, id):
#         try:
#             pkg = packages.objects.get(package_id=id)
#             if pkg.seats:
#                 num = int(pkg.seats)
#             else: 
#                 num=0
#             # Generate the total seat list
#             total_seat = [x for x in range(1, num + 1)]
#             # Get booked seats
#             seat = user_booking.objects.filter(Q(package_id=id) | Q(confirm=True))

#             seat_num = [int(x.seat_no) for x in seat if x.seat_no]

#             package_obj=packages.objects.filter(package_id=id).first()
#             if len(seat_num) == int(package_obj.seats):
#                 package_obj.is_pack_available=False
#                 package_obj.save()

#             # Calculate the midpoint for splitting the seats into two columns
#             midpoint = len(total_seat) // 2

#             # Get from places
#             from_places = pkg.from_place.all()

#             # Render the template with the context
#             return render(request, 'booking.html', {
#                 'seat_num': seat_num,
#                 'total_seat': total_seat,
#                 'midpoint': midpoint,
#                 'pkg': pkg,
#                 'from_places': from_places
#             })
#         except Exception as e:
#             print(e)
#             return HttpResponse(e)

        
#     def post(self,request,id):
#         try:
#             booking=packages.objects.filter(package_id=id)
#             pkg=packages.objects.get(package_id=id)
#             child=(pkg.p1_price)-(pkg.p1_price)*25//100
#             if request.method=="POST":
#                 name=request.POST.get("fname")
#                 type=request.POST.get("type")
#                 phone=request.POST.get("phone")
#                 from_place=request.POST.get("from_place")
#                 travel_date=request.POST.get("travel_date")
#                 ad_proice=0
#                 cd_price=0
#                 if type == "Adults":
#                    ad_proice=pkg.p1_price
#                 else:
#                     cd_price=child
#                 seat=request.POST.get('seat')
#                 from_obj=Places.objects.filter(pk=int(from_place)).first()
#                 user_booking_obj=user_booking.objects.create(user=request.user,package_id=packages.objects.get(package_id=id),name=name,type=type,Adult_price=ad_proice,child_price=cd_price,seat_no=seat)
#                 user_booking_obj.phone_number=phone
#                 user_booking_obj.from_place=from_obj
#                 user_booking_obj.travel_date=travel_date
#                 user_booking_obj.save()
#             return redirect("/user_book")
#         except Exception as e:
#             return HttpResponse(e)
        

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db.models import Q
from .models import packages, user_booking, Places

class select_package(View):
    def get(self, request, id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX requests for filtering seats
            travel_date = request.GET.get('travel_date', None)
            try:
                pkg = packages.objects.get(package_id=id)
                if pkg.seats:
                    num = int(pkg.seats)
                else:
                    num = 0

                total_seat = [x for x in range(1, num + 1)]
                
                if travel_date:
                    seat = user_booking.objects.filter(package_id=id, travel_date=travel_date)
                else:
                    seat = user_booking.objects.filter(package_id=id, confirm=True)

                seat_num = [int(x.seat_no) for x in seat if x.seat_no]
                print("kkkkk",seat_num)

                if len(seat_num) == int(pkg.seats):
                    pkg.is_pack_available = False
                    pkg.save()

                response_data = {
                    'seat_num': seat_num,
                    'total_seat': total_seat,
                    'midpoint': len(total_seat) // 2,
                }
                return JsonResponse(response_data)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        else:
            # Handle normal GET requests
            try:
                pkg = packages.objects.get(package_id=id)
                if pkg.seats:
                    num = int(pkg.seats)
                else:
                    num = 0
                
                total_seat = [x for x in range(1, num + 1)]
                
                # Get booked seats based on current or selected travel date
                travel_date = request.GET.get('travel_date', None)
                if travel_date:
                    seat = user_booking.objects.filter(package_id=id, travel_date=travel_date, confirm=True)
                else:
                    seat = user_booking.objects.filter(package_id=id, confirm=True)

                seat_num = [int(x.seat_no) for x in seat if x.seat_no]

                if len(seat_num) == int(pkg.seats):
                    pkg.is_pack_available = False
                    pkg.save()

                midpoint = len(total_seat) // 2
                from_places = pkg.from_place.all()

                return render(request, 'booking.html', {
                    'seat_num': seat_num,
                    'total_seat': total_seat,
                    'midpoint': midpoint,
                    'pkg': pkg,
                    'from_places': from_places,
                    'selected_date': travel_date
                })
            except Exception as e:
                print(e)
                return HttpResponse(e)
        
    def post(self, request, id):
        try:
            pkg = packages.objects.get(package_id=id)
            child_price = pkg.p1_price - (pkg.p1_price * 25 // 100)
            if request.method == "POST":
                name = request.POST.get("fname")
                booking_type = request.POST.get("type")
                phone = request.POST.get("phone")
                from_place = request.POST.get("from_place")
                travel_date = request.POST.get("travel_date")
                seat = request.POST.get('seat')
                
                adult_price = pkg.p1_price if booking_type == "Adults" else 0
                child_price = child_price if booking_type == "child" else 0
                
                from_obj = Places.objects.filter(pk=int(from_place)).first()
                user_booking_obj = user_booking.objects.create(
                    user=request.user,
                    package_id=pkg,
                    name=name,
                    type=booking_type,
                    Adult_price=adult_price,
                    child_price=child_price,
                    seat_no=seat,
                    phone_number=phone,
                    from_place=from_obj,
                    travel_date=travel_date
                )
                user_booking_obj.save()
            return redirect("/user_book")
        except Exception as e:
            return HttpResponse(e)
    

def user_book(request):
    if request.user.is_authenticated:
        user_bookings = user_booking.objects.filter(Q(user=request.user) & Q(confirm=False))
        
        total_adult_price = sum(i.Adult_price for i in user_bookings)
        total_child_price = sum(i.child_price for i in user_bookings)
        total_price = total_adult_price + total_child_price
        
        package_ids = [i.package_id for i in user_bookings]
        if not package_ids:
            package_ids.append(1)

        if request.method == "POST":
            con = request.POST.get("confirm")
            coni = request.POST.get("con")
            if con == "on":
                try:
                    booking_to_confirm = user_booking.objects.get(id=coni, user=request.user)
                    booking_to_confirm.confirm = True
                    booking_to_confirm.save()
                except user_booking.DoesNotExist:
                    messages.error(request, "Booking not found or you are not authorized to confirm it.")

        return render(request, 'mybooking.html', {
            "user_bok": user_bookings,
            'total_ap': total_adult_price,
            'total_cp': total_child_price,
            'total_price': total_price,
            'k': package_ids[-1]
        })
    messages.error(request, "You are not logged in.")
    return redirect('/packages')

def delete_booking(request,uid):
    try:
       id_field=user_booking.objects.get(booking_id=uid)
       id=id_field.package_id
       print(uid)
       user_booking.objects.get(booking_id=uid).delete()
       if user_booking:
            return redirect("/user_book")
       else:
           messages.warning(request,"no packages in your login") 
           return redirect("/packages")
           
    except Exception as e:
        return HttpResponse(e)
import razorpay 
from django.conf import settings
def confirm(request):
    if request.user.is_authenticated:
        con_tic= user_booking.objects.filter(user=request.user,confirm=True,payment=False)
        return render(request,'confirm.html',{"con_tic":con_tic})

def success(request):
    if request.method=="GET":
        data=request.GET
        p_id=data.get('payment_id')
        id=data.get('package_id')
        model=user_booking.objects.get(id=id)
        model.payment_id=p_id
        model.payment=True
        model.save()
        con_tic= user_booking.objects.filter(user=request.user,payment=True)
    return render(request,'success.html',{'con_tic':con_tic,'download_tic':model})

def del_conf(request,id):
    user_booking.objects.get(booking_id=id).delete()
    if user_booking:
        return redirect("/confirm")
    else:
        return redirect("/packages")

def view_tickets(request):
    con_tic= user_booking.objects.filter(user=request.user,payment=True)
    return render(request,'view_tickets.html',{'con_tic':con_tic})

def processed(request,id):
    processed=user_booking.objects.get(id=id)
    return render(request,'processed.html',{'download_tic':processed})




