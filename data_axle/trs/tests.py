from django.test import TestCase,RequestFactory
from django.test import Client
from django.contrib.messages import get_messages
from trs.helper import dummy_data_creator
from trs.class_config import fc_num_of_cabins,sc_num_of_cabins,fc_available,sc_available,fc_reversed,sc_reserved,FIRST_CLASS_FARE,SECOND_CLASS_FARE
from django.core.cache import cache


class ReservationTests(TestCase):
    

    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        self.fc_num_of_cabins=fc_num_of_cabins
        self.sc_num_of_cabins=sc_num_of_cabins
        self.fc_available=fc_available
        self.sc_available=sc_available
        self.fc_reversed = fc_reversed
        self.sc_reserved=sc_reserved
        self.fc_fare = FIRST_CLASS_FARE
        self.sc_fare = SECOND_CLASS_FARE


        with open('trs/class_config.py','w') as myfile:
            myfile.write('fc_num_of_cabins = {}\n'.format(2))
            myfile.write('sc_num_of_cabins = {}\n'.format(3))
            myfile.write('fc_available = {}\n'.format(10))
            myfile.write('sc_available = {}\n'.format(15))
            myfile.write('fc_reversed = {}\n'.format(4))
            myfile.write('sc_reserved = {}\n'.format(5))
            myfile.write('FIRST_CLASS_FARE = {}\n'.format(self.fc_fare))
            myfile.write('SECOND_CLASS_FARE = {}\n'.format(self.sc_fare))
        

    def tearDown(self):
    
        with open('trs/class_config.py','w') as myfile:
            myfile.write('fc_num_of_cabins = {}\n'.format(self.fc_num_of_cabins))
            myfile.write('sc_num_of_cabins = {}\n'.format(self.sc_num_of_cabins))
            myfile.write('fc_available = {}\n'.format(self.fc_available))
            myfile.write('sc_available = {}\n'.format(self.sc_available))
            myfile.write('fc_reversed = {}\n'.format(self.fc_reversed))
            myfile.write('sc_reserved = {}\n'.format(self.sc_reserved))
            myfile.write('FIRST_CLASS_FARE = {}\n'.format(self.fc_fare))
            myfile.write('SECOND_CLASS_FARE = {}\n'.format(self.sc_fare))
        
   

    def test_check_availability(self):
        """
         Test if no_of_family_members is more than seats available in first class and second class
        """
        self.client = Client()
        post_data = {
            'no_of_family_members':100
        }
        response = self.client.post("/trs/check_availability/",post_data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        # print(messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"{post_data['no_of_family_members']} number of seats are not available in any cabin of First Class and Second Class cabins")
        self.assertEqual(response.status_code, 200)


    def test_class_availability(self):
        """
         Test if first class appears in case of availability for no_of_family_members
        """
        self.client = Client()
        post_data = {
            'no_of_family_members':6
        }
        response = self.client.post("/trs/check_availability/",post_data)

        self.assertIn('first_class', response.context['selected_data']['available_classes'], "First Class option will appear")
        self.assertEqual(response.status_code, 200)


    def test_class_non_availability(self):
        """
         Test if first class not appear in case of non availability for no_of_family_members 
        """
        self.client = Client()
        post_data = {
            'no_of_family_members':7
        }
        response = self.client.post("/trs/check_availability/",post_data)

        self.assertNotIn('first_class', response.context['selected_data']['available_classes'], "First Class option will appear")
        self.assertEqual(response.status_code, 200)

    
    def test_reserve_seats(self):
        """ 
        Test if first class cabin seats are being reserved in case of availability
        """
        self.client = Client()
        post_data = {
            'no_of_family_members':6,
            'selected_class':'first_class'
        }
        response = self.client.post("/trs/reserve_seats/",post_data)
        # print(response.context['reservation_details'])
        test_res = ['5', '6', '7', '8', '9', '10']
        self.assertTrue(all(x == y for x, y in zip(response.context['reservation_details']['details']['reserved_seats'], test_res)))
        self.assertEqual(response.status_code, 200)



