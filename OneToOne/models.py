from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Customer(models.Model):
    """
    A class based model for storing the records of a university student
    Note: A OneToOne relation is established for each student with User model.
    """
    SOURCE_CHOICES = (
        ('Online', 'Online'), ('Referral', ' Referral'), ('Old', 'Old Customer'), ('Phone', ' Phone Call'))
    customercode= models.OneToOneField(User, on_delete=models.CASCADE, )
    contactname = models.CharField(max_length=100)
    companyname = models.CharField(max_length=200, blank=True)
    billingaddress = models.TextField(max_length=100)
    installaddress = models.TextField(max_length=100, blank=True, null=True)
    contactno = models.CharField(max_length=20 , null=True)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    invitationcode = models.CharField(max_length=20, blank=False)
    joindate = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    comment = models.TextField(max_length=300, blank=True, null=True)
    isconfirm = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s" % (self.customercode, self.contactname)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class EmailVerification(models.Model):
    code_of_verification = models.CharField(max_length=254, unique=True)
    username = models.CharField(max_length=100, primary_key=True)
    date = models.DateTimeField(auto_now=True)

