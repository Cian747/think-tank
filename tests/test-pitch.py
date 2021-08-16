import unittest
from app.models import Pitch
from . import db


class TestPitch(unittest.TestCase):
    '''
    Testing the pitch model
    '''
    def setUp(self):
        '''
        Creating object and instance of the class        
        '''
        self.pitch_test = Pitch(1,2,'Business',1999-5-12,'Dress good to feel good',1,3)

    def tearDown(self):
        '''
        Array to refresh after every test
        '''
        Pitch.query.delete()

    def test_instance_pitch(self):
        '''
        Testing to see if the data created in setup works
        '''
        self.assertEqual(self.pitch_test.id,1)
        self.assertEqual(self.pitch_test.user_id,2)
        self.assertEqual(self.pitch_test.category_name,'Business')
        self.assertEqual(self.pitch_test.posted,1999-5-12)
        self.assertEqual(self.pitch_test.pitch_content,'Dress good to feel good')
        self.assertEqual(self.pitch_test.upVote,1)
        self.assertEqual(self.pitch_test.downVote,3)

    def test_save_pitch(self):
        '''
        Saving a pitch
        '''
        self.pitch_test.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_review_by_id(self):

        self.new_review.save_review()
        got_pitches = Pitch.get_reviews(1)
        self.assertTrue(len(got_pitches) == 1)
        