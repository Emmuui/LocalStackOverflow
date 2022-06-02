def upload_file(instance, file):
    """ Path to upload avatar file """

    return f'profile_avatar/{instance.username}/{file}'
