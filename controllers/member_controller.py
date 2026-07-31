from dao.member_dao import MemberDAO

class MemberController:

    def __init__(self):
        self.dao = MemberDAO()

    def save_member(self, member):
        self.dao.add_member(member)

    def show_members(self):
        return self.dao.get_all_members()

    def remove_member(self, member_id):
        self.dao.delete_member(member_id)