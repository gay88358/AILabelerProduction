


from webserver.util.query_util import fix_ids


class JsonPrepare:
    def prepare_user_json(self, user):
        user_json = fix_ids(user)
        del user_json['password']
        return user_json