class UserNotFoundException(Exception):

    def __init__(self, user_id):
        self.user_id = user_id


class AdAlreadyInFavoritesException(Exception):

    def __init__(self, ad_id):
        self.ad_id = ad_id
