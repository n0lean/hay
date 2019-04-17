

class Owner(object):
    def __init__(self, display_name, _id):
        self.display_name = display_name
        self.id = _id

    def to_dict(self):
        return {
            'DisplayName': self.display_name,
            'ID': self.id
        }


class Grantee(object):
    def __init__(self, _type, display_name=None, email_address=None, _id=None, uri=None):
        if _id:
            self.id = _id
        if display_name:
            self.display_name = display_name
        if self.email_address:
            self.email_address = email_address

        self.type = _type

        if uri:
            self.uri = uri

        self.ACC_TYPE = ('CanonicalUser', 'AmazonCustomerByEmail', 'Group')
        assert self.type in self.ACC_TYPE

    def to_dict(self):
        d = {'Type': self.type}
        if 'id' in self.__dict__:
            d['ID'] = self.id
        if 'display_name' in self.__dict__:
            d['DisplayName'] = self.display_name
        if 'email_address' in self.__dict__:
            d['EmailAddress'] = self.email_address
        if 'uri' in self.__dict__:
            d['URI'] = self.uri
        return d


class Grants(object):
    def __init__(self, grantee_list, permission):
        assert isinstance(grantee_list, list)

        self.grantee_list = grantee_list

        self.permission = permission
        self.ACC_PERMISSION = ('FULL_CONTROL', 'WRITE', 'WRITE_ACP', 'READ', 'READ_ACP')

        assert self.permission in self.ACC_PERMISSION

    def set_permission(self, new_permission):
        assert new_permission in self.ACC_PERMISSION
        self.permission = new_permission

    def to_list(self):
        grants = []
        for g in self.grantee_list:
            d = {
                'Permission': self.permission,
                'Grantee': g.to_dict()
            }
            grants.append(d)
        return grants


class AccessControlPolicy(object):
    def __init__(self, grants, owner):
        self.grants = grants
        self.owner = owner

    def to_dict(self):
        return {
            'Grants': self.grants.to_list(),
            'Owner': self.owner.to_dict()
        }
