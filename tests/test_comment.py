from datetime import date
import unittest
from app import db
from app.models import Comment,User


class TestComment(unittest.TestCase):
    '''
    Test comment model
    '''

    def setUp(self):
        '''
        Define the set up
        '''
        self.new_user = User(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_comment = Comment(id = 1,user = 2,pitch_id = 2,date = '1660-08-09',com_write='great work')

    def tearDown(self):
        '''
        Refresh
        '''
        Comment.query.delete()

    def test_comment(self):
        '''
        Check instance for the comments table
        '''
        self.assertTrue(isinstance(self.new_comment,Comment))
    

    def test_instance_comment(self):
        '''
        Assert that the details in the class match
        '''
        self.assertEqual(self.new_comment.id, 1)
        self.assertEqual(self.new_comment.user,2)
        self.assertEqual(self.new_comment.pitch_id,2)
        self.assertEqual(self.new_comment.date,'1660-08-09')
        self.assertEqual(self.new_comment.com_write,'great work')

    def test_save_comment(self):
        '''
        Check if a comment is saved
        '''
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

