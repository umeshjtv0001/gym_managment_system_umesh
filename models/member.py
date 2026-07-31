class Member:

    def __init__(self,
                 member_id=None,
                 name="",
                 age=0,
                 gender="",
                 phone="",
                 email="",
                 address="",
                 join_date=None):

        self.member_id = member_id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address
        self.join_date = join_date