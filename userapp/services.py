def upload_file(instance, file):
    """ Path to upload avatar file """

    return f'profile_avatar/{instance.username}/{file}'


class UserRating:

    def __init__(self, user):
        self.user = user
        self.one_time_add = 5
        self.mult_by_mapping = {
            'NEW': 5,
            'MIDL': 10,
            'PRO': 15,
            'STAFF': 20
        }
        self.mult_by = self.mult_by_mapping[self.user.rank]

    def rating_for_creation_record(self):
        self.user.rating += self.one_time_add
        self.user.save()
        return self.user.rating

    def count_user_rating(self, vote):
        if int(vote) == 1:
            self.user.rating += self.mult_by
        elif int(vote) == -1:
            self.user.rating -= self.mult_by
        self.user.save()
        return self.user.rating

    def add_rank_to_user(self):
        if self.user.rating <= 100:
            self.user.rank = 'NEW'
        elif 100 < self.user.rating <= 300:
            self.user.rank = 'MIDL'
        elif 300 < self.user.rating <= 500:
            self.user.rank = 'PRO'
        elif self.user.rating > 500:
            self.user.rank = 'STAFF'
            self.user.is_staff = True
        self.user.save()
        return self.user.rank

    def run_system(self, vote):
        self.count_user_rating(vote)
        self.add_rank_to_user()
        return self.user.rank
