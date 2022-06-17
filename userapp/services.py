def upload_file(instance, file):
    """ Path to upload avatar file """

    return f'profile_avatar/{instance.username}/{file}'


class DeleteUsersVote:
    def __init__(self, user):
        self.user = user

    def all_votes_by_user(self):
        pass