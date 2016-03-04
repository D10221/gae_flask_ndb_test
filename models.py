from google.appengine.ext.ndb import Model, StringProperty, KeyProperty, IntegerProperty


def first_or_default(alist):
    """
    1st or None
    :param alist: a list :type list
    :return 1st T in list or None:
    """
    return alist[0] if alist.__len__() > 0 else None


class Role(Model):
    role_id = StringProperty(required=True)
    ordinal = IntegerProperty(required=True)

    @classmethod
    def new(cls, id, ordinal):
        return Role(id=id, role_id=id, ordinal=ordinal)


class LocalUser(Model):
    user_id = StringProperty(required=True)
    email = StringProperty(required=True)
    roles = KeyProperty(kind=Role, repeated=True)

    def get_role(self, role):
        roles = [user_role for user_role in self.roles if user_role.id() == role]
        return first_or_default(roles)

    def get_role_id(self, role):
        return self.get_role(role).id()

    def has_role(self, role):
        return self.get_role(role) is not None

    @classmethod
    def new_user(cls, user_id, email, roles=None):
        """ add new user
        :param roles: list of strings to lookup against Role
        :param email: required
        :param user_id: unique ID as string
        """
        found_roles = [] if roles is None else [Role.get_by_id(role).key for role in roles]
        return LocalUser(id=user_id, user_id=user_id, email=email, roles=found_roles)

    @classmethod
    def from_gae_user(cls, user, roles=None):
        return cls.new_user(user_id=user.user_id(), email=user.email(), roles=roles)
        pass

    def add_role(self, role):
        self.roles.append(Role.get_by_id(role).key)


def set_up_default_roles():
    Role.new('none', 0).put()
    Role.new('user', 1).put()
    Role.new('admin', 2).put()

# set_up_default_roles()
