from django.test import TestCase
from sign.models import Event,Guest
# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id = 1,name = 'tomduck',status =True,limit=1818,address = 'shanghai',start_time = '2019-02-01')
        Guest.objects.create(id = 1,event_id = 1,realname = 'flank',phone = 18000000006,email='123@321.com',sign = False)
    def test_event_models(self):
        result = Event.objects.get(name = 'tomduck')
        self.assertEqual(result.address,'shanghai')
        self.assertTrue(result.status)
    def test_guest_models(self):
        result = Guest.objects.get(phone = 18000000006)
        self.assertEqual(result.realname,'allen')
        self.assertFalse(result.sign)
class IndexPageTest(TestCase):
    def test_index_page_render_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')
        
