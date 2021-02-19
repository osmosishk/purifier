from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from OneToOne.models import Customer

class Product(models.Model):
    PRODUCT_CHOICES = (('WPU','Water Purifier'),('U','Under Sink'),('F','Filter'))
    productcode = models.CharField(max_length=30)
    producttype =models.CharField(max_length=3 , choices =PRODUCT_CHOICES)
    price = models.FloatField()

    def __str__(self):
        return self.productcode

class MainPack(models.Model):
    packagecode = models.CharField(max_length=30, unique=True)
    isbytime = models.BooleanField(default=True)
    isbyusage = models.BooleanField(default=False)
    price = models.FloatField()
    exfiltermonth = models.IntegerField(default=6)
    exfiltervolume = models.IntegerField(default=2500)
    packagedetail = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.packagecode


class Machine(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default='')
    machineid = models.CharField(max_length=100, unique=True)
    installaddress1 = models.TextField(max_length=100)
    installaddress2 = models.TextField(max_length=300, blank=True)
    photoncode = models.CharField(max_length=100)
    mac = models.CharField(max_length=100, blank=True)

    installdate = models.DateField(null=True, blank=True)
    nextservicedate = models.DateField(null=True, blank=True)
    machinetype = models.ForeignKey(Product , on_delete=models.CASCADE ,null=True)
    maintenance = models.ForeignKey(MainPack, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return "%s %s " % (self.machineid, self.customer.customercode)

    def get_period(self):
        return "%s " % self.maintenance.exfiltermonth

class Filter(models.Model):
    filtercode = models.CharField(max_length=30, unique=True)
    filtername = models.CharField(max_length=30)
    filterdetail = models.CharField(max_length=300)
    price = models.FloatField()

    def __str__(self):
        return self.filtername


class Technician(models.Model):
    staffcode = models.CharField(max_length=30, unique=True)
    staffshort = models.CharField(max_length=5, default='')
    staffname = models.CharField(max_length=30)
    staffcontact = models.CharField(max_length=300)
    email = models.EmailField(max_length=30)

    def __str__(self):
        return self.staffshort


class Case(models.Model):
    case_id = models.AutoField(primary_key=True)
    CASE_TYPE = [('Filter replacement', 'Filter replacement'), ('Urgent Repair', 'Urgent Repair'),
                 ('Installation', 'Installation'), ('Checking', 'Checking')]
    machines = models.ManyToManyField(Machine)
    casetype = models.CharField(max_length=100, choices=CASE_TYPE)
    scheduledate = models.DateField(null=True, blank=False)
    time = models.TimeField(null=True, blank=False)
    action = models.TextField(max_length=100, blank=True)
    suggest = models.TextField(max_length=100, blank=True)
    comment = models.TextField(max_length=100, blank=True)
    iscompleted = models.BooleanField(default=False, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default='')
    filters = models.ManyToManyField(Filter, blank=True)
    handledby = models.ForeignKey(Technician, on_delete=models.CASCADE)



    # def get_absolute_url(self):
    #    return reverse("crm:caselist")

    # def get_machine(self):
    #     return ",".join([str(p) for p in self.machine.all()])

    # def get_filter(self):
    #     return " / ".join([str(f) for f in self.filter.all()])


class MainPeriod(models.Model):
    machine = models.ForeignKey('Machine',on_delete=models.CASCADE)
    startdate = models.DateField(null=True, blank=False)
    enddate = models.DateField(null=True, blank=False)
    Price = models.CharField(max_length=30, blank=False)
    isrenewed = models.BooleanField(default=False, blank=False)

