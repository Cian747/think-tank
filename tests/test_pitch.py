import unittest
from app.models import Pitch,User
from app import db


class TestPitch(unittest.TestCase):
    '''
    Testing the pitch model
    '''
    def setUp(self):
        '''
        Creating object and instance of the class        
        '''
        self.user_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.pitch_test = Pitch(id = 15,user_id = 2,category_name='Business',posted='1999-5-12',pitch_content='Dress good to feel good',upVote=1,downVote=3)


    def tearDown(self):
        '''
        Clear the table
        '''
        Pitch.query.delete()

    
    def test_instance(self):
        '''
        test instance for pitch class
        '''

        self.assertTrue(isinstance(self.pitch_test,Pitch))

    def test_instance_pitch(self):
        '''
        Testing to see if the data created in setup works
        '''
        self.assertEqual(self.pitch_test.id,15)
        self.assertEqual(self.pitch_test.user_id,2)
        self.assertEqual(self.pitch_test.category_name,'Business')
        self.assertEqual(self.pitch_test.posted,'1999-5-12')
        self.assertEqual(self.pitch_test.pitch_content,'Dress good to feel good')
        self.assertEqual(self.pitch_test.upVote,1)
        self.assertEqual(self.pitch_test.downVote,3)

    def test_save_pitch(self):
        '''
        Saving a pitch
        '''
        self.pitch_test.save_pitch()
        self.assertTrue(len(Pitch.query.all())> 0)

    

        