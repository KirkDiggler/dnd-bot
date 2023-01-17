from unittest import TestCase
from src.discord import poll

class MockUser:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class TestPoll(TestCase):
    def test_pop(self):
        testPoll = poll.UserPoll(votes_per_user=1)

        firstVote = testPoll.vote(MockUser(name="Test User", id=1), "Test Vote")
        secondVote = testPoll.vote(MockUser(name="Test User", id=1), "Test Vote 2")

        self.assertEqual(firstVote, True)
        self.assertEqual(secondVote, False)

        testPoll.pop_vote(MockUser(name="Test User", id=1))

        thirdVote = testPoll.vote(MockUser(name="Test User", id=1), "Test Vote 2")

        self.assertEqual(thirdVote, True)

    def test_remove(self):
        testPoll = poll.UserPoll(votes_per_user=1)

        firstVote = testPoll.vote(MockUser(name="Test User", id=1), "Test Vote")
        secondVote = testPoll.vote(MockUser(name="Test User", id=1), "Test Vote 2")

        self.assertEqual(firstVote, True)
        self.assertEqual(secondVote, False)

        removeSuccess = testPoll.remove_vote(MockUser(name="Test User", id=1), "Test Vote")
        self.assertEqual(removeSuccess, True)
        
        thirdVote = testPoll.vote(MockUser(name="Test User", id=1), "Test Vote 2")

        self.assertEqual(thirdVote, True)