from google.appengine.ext.ndb import Model, StringProperty, KeyProperty, IntegerProperty


def first_or_default(alist):
        return alist[0] if alist.__len__() > 0 else None


class Role(Model):
    role_id = StringProperty(required=True)
    ordinal = IntegerProperty(required=True)


class LocalUser(Model):
    user_id = StringProperty(required=True)
    email = StringProperty(required=True)
    roles = KeyProperty(kind=Role, repeated=True)

    def get_role(self, role):
        roles = [user_role for user_role in self.roles if user_role.id() == role]
        return first_or_default(roles)

    def get_role_id(self, role):
        roles = [user_role.id() for user_role in self.roles if user_role.id() == role]
        return first_or_default(roles)

    def has_role(self, role):
        return self.get_role(role) is not None

    @classmethod
    def new_user(cls, user_id, email, roles=None):
        """ add new user
        :param roles: list of strings to lookup against Role
        :param email: required
        :param user_id: unique ID as string
        """
        found_roles = [Role.get_by_id(role).key for role in roles]
        return LocalUser(id=user_id, user_id=user_id, email=email, roles=found_roles)


