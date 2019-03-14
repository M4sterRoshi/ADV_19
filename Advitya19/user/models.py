from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework import exceptions
from django.conf import settings
from datetime import datetime, timedelta
import jwt



class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, name, password, institution, need_accomodation, gender, contact_number):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            institution=institution,
            need_accomodation=need_accomodation,
            gender=gender,
            contact_number=contact_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password, institution, need_accomodation, gender, contact_number):
        user = self.create_user(
            email,
            password=password,
            name=name,
            institution=institution,
            need_accomodation=need_accomodation,
            gender=gender,
            contact_number=contact_number
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, institution="AdminHouse", need_accomodation=False, gender="M", contact_number="0000000"):
        user = self.create_user(
            email,
            password=password,
            name= name,
            institution=institution,
            need_accomodation=need_accomodation,
            gender=gender,
            contact_number=contact_number
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other/Choose to not specify')
    )
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER, default = 'M')
    institution = models.CharField(max_length=100)
    need_accomodation = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        if self.is_staff:
            if self.is_superuser:
                return('ADMIN'+str(10000+self.pk))
            else:
                return('STAFF'+str(10000+self.pk))
        else:
            return('PARTP'+str(10000+self.pk))

    def token(self):
        return self.__generate__jwt_token()

    def __generate__jwt_token(self):

        dt = datetime.now() + timedelta(hours=12)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

