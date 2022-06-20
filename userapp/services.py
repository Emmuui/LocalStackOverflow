def upload_file(instance, file):
    """ Path to upload avatar file """

    return f'profile_avatar/{instance.username}/{file}'


class UserRating:

    def __init__(self, user):
        self.user = user
        self.mult_by = 10
        self.local_rating = 0

    def rating_for_vote(self, number):
        self.user.rating += int(number)
        self.user.save()
        self.add_rank_to_user()
        return self.user

    def count_user_rating(self):
        self.local_rating = self.mult_by
        self.user.rating += self.local_rating
        self.user.save()
        self.add_rank_to_user()
        return self.user

    def add_rank_to_user(self):
        if self.user.rating <= 100:
            self.user.rank = 'NEW'
        elif 100 < self.user.rating <= 300:
            self.user.rank = 'MIDL'
        elif 300 < self.user.rating <= 500:
            self.user.rank = 'PRO'
        elif self.user.rating > 500:
            self.user.is_staff = True
        self.user.save()
        return self.user