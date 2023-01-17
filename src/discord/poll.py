class UserPoll:
    def __init__(self, votes_per_user):
        __slots__ = '_votes_per_user', '_votes', '_user_votes'

        self.votes_per_user = votes_per_user
        self._user_votes = {}
        self._votes = {}

    def vote(self, user, vote):
        print(f"UserPoll: User {user.id} voted for {vote} userVotes: {self._user_votes}.")
        if user.id not in self._user_votes:
            self._user_votes[user.id] = [vote]
        else:
            if len(self._user_votes[user.id]) < self.votes_per_user:
                self._user_votes[user.id].append(vote)
            else:
                return False

        if vote not in self._votes:
            self._votes[vote] = 1
        else:
            self._votes[vote] += 1

        return True

    def pop_vote(self, user):
        if user.id not in self._user_votes:
            return None

        vote = self._user_votes[user.id].pop(0)
        self._decrement_vote(vote)
        
        return vote

    def remove_vote(self, user, vote):
        if user.id not in self._user_votes:
            return False

        if vote in self._user_votes[user.id]:
            self._user_votes[user.id].remove(vote)
        else:
            return False

        self._decrement_vote(vote)

        return True

    def _decrement_vote(self, vote):
        if vote not in self._votes:
            return False

        self._votes[vote] -= 1
        return True

    def get_winners(self):
        votes = []
        for _ in range(self.votes_per_user):
            for key, vote in self._votes.items():
                if vote == max(self._votes.values()):
                    votes.append(key)
                    self._votes[key] = -1
                    break
        return votes
