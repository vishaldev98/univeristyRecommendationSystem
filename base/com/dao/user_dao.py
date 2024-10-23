from base import db
from base.com.vo.user_vo import UserVO


class UserDAO:
    def insert_user(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()

    def get_all_users(self):
        """Fetch all users from the database."""
        try:
            return UserVO.query.all()  # Fetch all users from the user_table
        except Exception as ex:
            print("Error fetching users: ", ex)  # Ensure this prints any exceptions
            return []
