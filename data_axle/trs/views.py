from django.shortcuts import render,redirect
from trs.class_config import fc_num_of_cabins,sc_num_of_cabins,fc_available,sc_available,fc_reversed,sc_reserved,FIRST_CLASS_FARE,SECOND_CLASS_FARE
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from trs.helper import do_reservation,dummy_data_creator



def home(request):
    return render(request,'trs/home_trs.html')


@csrf_exempt
def check_availability(request):
    if request.method == 'GET':
        return render(request,'trs/reserve_trs.html')
    if request.method == 'POST':
        available_classes = []
        no_of_family_members = int(request.POST.get('no_of_family_members',0))
        data = dummy_data_creator(fc_num_of_cabins,sc_num_of_cabins,fc_available,sc_available,fc_reversed,sc_reserved)
        for _,status in data['first_class'].items():
            if len(status['available_seats'])>=no_of_family_members:
                available_classes.append('first_class')
                break
        for _,status in data['second_class'].items():
            if len(status['available_seats'])>=no_of_family_members:
                available_classes.append('second_class')
                break
        selected_data = {'no_of_family_members':no_of_family_members,"available_classes":available_classes}
        if len(available_classes) == 0:
            selected_data["Error"] = f"{no_of_family_members} number of seats are not available in any cabin of First Class and Second Class cabins"
            messages.info(request, selected_data["Error"])
        return render(request,'trs/reserve_trs.html', {"selected_data":selected_data})


def reserve_seats(request):
    if request.method == 'POST':
        no_of_family_members = int(request.POST.get('no_of_family_members'))
        data = dummy_data_creator(fc_num_of_cabins,sc_num_of_cabins,fc_available,sc_available,fc_reversed,sc_reserved)
        selected_class = request.POST.get('selected_class')
        reservation_details = {}
        if selected_class == 'first_class':
            reservation_details = do_reservation(selected_class,data,no_of_family_members,FIRST_CLASS_FARE)
        elif selected_class == 'second_class':
            reservation_details = do_reservation(selected_class,data,no_of_family_members,SECOND_CLASS_FARE)
        else:
            reservation_details["Error"] = "Invalid class"
            return JsonResponse(reservation_details,safe=False)
        if 'Error' in reservation_details:
            messages.info(request, reservation_details["Error"])
        return render(request,'trs/reservation_details_trs.html', {"reservation_details":reservation_details}) 
    return redirect("home")
    
        

                


