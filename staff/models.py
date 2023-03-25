from django.db import models
import random, string, hashlib
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import check_password as django_check_password


from django.contrib.auth.models import BaseUserManager

ADMIN_ROLE_ID = 1
EMPLOYEE_ROLE_ID = 2

class Role(models.Model):
    id = models.AutoField(primary_key=True, name='id')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StaffManager(BaseUserManager):
    def get_by_natural_key(self, id):
        user = self.get(id=id)
        return user


class Staff(models.Model):
    id = models.AutoField(primary_key=True, name='id')
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    secret_key = models.TextField()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['password','email', 'role', 'secret_key']

    objects = StaffManager()
    
    @property
    def is_staff(self):
        return self.role.id == ADMIN_ROLE_ID

    @property
    def is_admin(self):
        return self.role == 1 or self.role == 2
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True


    @classmethod
    def generate_secret_key(cls):
        """Generate a random string of length 32."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    
    def check_password(self, raw_password):
        """
        Check the given password against the hashed password in the database.

        Returns True if the passwords match, False otherwise.
        """
        #TODO check accounts with hashed password
        #return Staff.hash_password(raw_password, self.secret_key) == self.password
        return raw_password == self.password

    @classmethod
    def hash_password(cls, password, secret_key):
        """Hash the password using the secret key."""
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), secret_key.encode('utf-8'), 1000)
        return hashed_password.hex()
    
    def __str__(self):
        return f'ID: {self.id} &name: {self.name} &role: {self.role}'
