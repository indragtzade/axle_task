import uuid


COSMATIC_NAMES = {"first_class": "First Class","second_class":"Second Class"}
FIRST_CLASS_FARE = 400
SECOND_CLASS_FARE = 300

def dummy_data_creator(fc_num_of_cabins,sc_num_of_cabins,fc_available,sc_available,fc_reversed = 0,sc_reserved=0):
    first_class_data = {}
    first_class_data['first_class']={cabin_num:{"available_seats":[str(i) for i in range(fc_reversed+1,fc_available+1)],\
               "reserved_seats": [str(i) for i in range(1,fc_reversed+1)] } for cabin_num in  range(1,fc_num_of_cabins+1) }
    
    second_class_data = {}
    second_class_data['second_class']={cabin_num:{"available_seats":[str(i) for i in range(sc_reserved+1,sc_available+1)],\
               "reserved_seats": [str(i) for i in range(1,sc_reserved+1)] } for cabin_num in  range(1,sc_num_of_cabins+1) }

    return  {**first_class_data, **second_class_data}


# print(dummy_data_creator(fc_num_of_cabins=4,sc_num_of_cabins=3,fc_available=10,sc_available=15,fc_reversed = 6,sc_reserved=5))






def do_reservation(selected_class,data,no_of_family_members,class_fare):
    reservation_details = {}
    for cabin_number,status in data[selected_class].items():
        
        if len(status['available_seats'])>=no_of_family_members:
            status['reserved_seats'] = status['available_seats'][0:no_of_family_members]
            status['available_seats'] =  status['available_seats'][no_of_family_members:]
            reservation_id = str(uuid.uuid1())
            reservation_details['reservation_id']= reservation_id
            reservation_details['details']={
                "selected_class":COSMATIC_NAMES[selected_class],
                "cabin_number":cabin_number,
                "seats_reserved":" ".join(status['reserved_seats']),
                "available_seats": status['available_seats'],
                "reserved_seats": status['reserved_seats'],
                "total_fare": no_of_family_members*class_fare,
                "payment_link":"hello@paylike.io"
            }
       
    return reservation_details

# # do_reservation('first_class',data1,10,400)

# # def do_reservation(selected_class,data,no_of_family_members,class_fare):
# #     reservation_details = {}
# #     for cabin_number,status in data[selected_class].items():
# #         if status['available_seats']>=no_of_family_members:
# #             start = status['reserved_seats']+1
# #             end = status['reserved_seats']+no_of_family_members+1
# #             seats_reserved = [i for i in range(start,end)]
# #             status['available_seats'] -= no_of_family_members
# #             status['reserved_seats'] += no_of_family_members
# #             reservation_id = str(uuid.uuid1())
# #             reservation_details['reservation_id']= reservation_id
# #             reservation_details['details']={
# #                 "selected_class":temporal_data.cosmatic_name[selected_class],
# #                 "cabin_number":cabin_number,
# #                 "seats_reserved": seats_reserved,
# #                 "available_seats": status['available_seats'],
# #                 "reserved_seats": status['reserved_seats'],
# #                 "total_fare": no_of_family_members*class_fare,
# #                 "payment_link":"hello@paylike.io"
# #             }
# #     return reservation_details