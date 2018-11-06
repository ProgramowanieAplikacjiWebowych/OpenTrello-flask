from Database.Entities.Security.User import User
from UsersAccountManager.UsersRepository import UsersRepository


class UsersAccountManager:

    def tryLogin(self, name, password):
        usersRepository = UsersRepository()
        return(usersRepository.checkLoginData(name, password) == True)

    def getUserData(self, name, password):
        usersRepository = UsersRepository()
        if(usersRepository.checkLoginData(name, password) == True):
            return User("Login", "Password", "Email")
        else:
            return None

