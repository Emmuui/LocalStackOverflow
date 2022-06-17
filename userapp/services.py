from vote.services import CountSystem


def upload_file(instance, file):
    """ Path to upload avatar file """

    return f'profile_avatar/{instance.username}/{file}'


class UserRating:

    def __init__(self, user, one_record):
        self.user = user
        self.one_record = one_record
        self.mult_by = 10
        self.local_rating = 0
        self.rating_for_registration = 20

    def count_user_rating(self):

        self.local_rating = self.mult_by * self.one_record
        self.user.rating = self.local_rating + self.rating_for_registration

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

