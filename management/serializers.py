from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers, status

from OneToOne.serializers import CustomerCodeSerializer ,CustomerSerializer
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('productcode' , 'producttype')


class MainPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPack
        fields = ('packagecode', 'isbytime', 'isbyusage', 'price', 'exfiltermonth', 'exfiltervolume', 'packagedetail')
        extra_kwargs = {
            'packagecode': {
                'validators': [], 'required': True
            },
            'price': {
                'required': False
            }
        }


class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = ('staffcode', 'staffshort', 'staffname', 'staffcontact', 'email')
        extra_kwargs = {
            'staffcode': {
                'validators': [], 'required': True
            },
            'staffname': {
                'validators': [], 'required': False
            },
            'staffcontact': {
                'validators': [], 'required': False
            },
            'email': {
                'validators': [], 'required': False
            },

        }


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ('filtercode', 'filtername', 'filterdetail', 'price')
        extra_kwargs = {
            'filtercode': {
                'validators': [], 'required': True
            },
            'filtername': {
                'required': False
            },
            'filterdetail': {
                'required': False
            },
            'price': {
                'required': False
            },

        }

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('productcode', 'producttype', 'price')

class LiteMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ('machineid',)
        extra_kwargs = {
            'machineid': {
                'validators': [], 'required': True
            },
        }

class LiteFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = ('filtercode',)
        extra_kwargs = {
            'filtercode': {
                'validators': [], 'required': True
            },
        }


class LiteTechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = ('staffcode','staffname')
        extra_kwargs = {
            'staffcode': {
                'validators': [], 'required': True
            },


        }


class MachineSerializer(serializers.ModelSerializer):
    """
    A MachineSerializer serializer to return the Water Purifier details
    """

    customer = CustomerCodeSerializer(required=True)
    machinetype =  ProductSerializer(required=True)
    # main_pack = MainPackSerializer(required=True)

    class Meta:
        model = Machine
        fields = ('customer','machineid', 'installaddress1', 'installaddress2',
                  'mac', 'installdate','nextservicedate', 'machinetype','id')
        extra_kwargs = {

            'machineid': {
                'validators': [], 'required': False
            },
            'user': {
                'required': False
            },
            'machinetype': {
                'required': False
            },
            'main_pack': {
                'required': False
            },

            'installaddress1': {
                'required': False
            },

        }

    def create(self, validated_data):
        try:

            machineid = validated_data["machineid"]
            machinetype = validated_data.pop("machinetype")
            customer = validated_data.pop("customer")
            ##main_pack = validated_data["main_pack"]
            installaddress1 = validated_data["installaddress1"]
            installaddress2 = validated_data["installaddress2"]
            mac = validated_data["mac"]
            installdate = validated_data["installdate"]
            nextservicedate = validated_data["nextservicedate"]

        except KeyError as e:
            print('I got a KeyError - reason "%s"' % str(e))
            raise serializers.ValidationError({'error': "please make sure JSON format"})

        if machineid == "" or customer =="":
            raise serializers.ValidationError({'error': "please make sure to fill all informations"})

        if Machine.objects.filter(machineid=validated_data["machineid"]).exists():
            raise serializers.ValidationError({'error': 'there is a water purifier with the same id'})

        if User.objects.filter(username=customer["customercode"]["username"]).exists():
            user_data = User.objects.get(username=customer["customercode"]["username"])
        else:
            raise serializers.ValidationError({"error": {"customercode": "the customercode did not exist"}})
        if Customer.objects.filter(customercode=user_data).exists():
            customer_data = Customer.objects.get(customercode=user_data)
        else:
            raise serializers.ValidationError({"error": {"customer": "the customer did not exist"}})
        if Product.objects.filter(productcode=machinetype["productcode"]).exists():
            machinetype_data = Product.objects.get(productcode=machinetype["productcode"])
        else:
            raise serializers.ValidationError({"error": {"productcode": "the productcode did not exist"}})


        machine, created = Machine.objects.update_or_create(customer=customer_data,
                                                  machinetype=machinetype_data,
                                                  machineid=machineid,
                                                  mac=mac,
                                                  installaddress1=installaddress1,
                                                  installaddress2=installaddress2,
                                                  installdate=installdate,
                                                  nextservicedate=nextservicedate)
        machine.save()
        return machine




class CaseSerializer(serializers.ModelSerializer):

    machines = LiteMachineSerializer(required=True , many=True )
    filters =  LiteFilterSerializer(required=True , many = True)
    handledby = LiteTechnicianSerializer(required=True)

    class Meta:
        model = Case
        fields = ('case_id','machines', 'casetype', 'scheduledate', 'time', 'action',
                  'suggest', 'comment','iscompleted','filters', 'handledby')

    def create(self, validated_data):

        # user_data = validated_data.pop('user')
        machines_data = validated_data.pop('machines')
        filters_data = validated_data.pop('filters')
        handledby_data = validated_data.pop('handledby')
        casetype = validated_data["casetype"]
        scheduledate = validated_data["scheduledate"]
        time = validated_data["time"]
        action = validated_data["action"]
        suggest = validated_data["suggest"]
        comment = validated_data["comment"]
        iscompleted = validated_data["iscompleted"]

        for machine_data in machines_data:
            if not Machine.objects.filter(machineid=machine_data["machineid"]).exists():
                raise serializers.ValidationError({'error': "the water purifer with the {} id is not exist".format(
                    machine_data["machineid"])})

        for filter_data in filters_data:
            if not Filter.objects.filter(filtercode=filter_data["filtercode"]).exists():
                raise serializers.ValidationError(
                    {'error': 'there is no filter with this id {}'.format(filter_data["filtercode"])})

        if not Technician.objects.filter(
                staffcode=handledby_data["staffcode"]).exists():
            raise serializers.ValidationError({'error': "there user not exist or the technician not exist"})

        userTemp = Machine.objects.get(machineid=machines_data[0]["machineid"]).customer


        for machine_data3 in machines_data:
            user = Machine.objects.get(machineid=machine_data3["machineid"]).customer
            if user != userTemp:
                raise serializers.ValidationError({'error': "all the machines in the same case must have the same "
                                                            "client"})
            else:
                userTemp = user
        technician = Technician.objects.get(staffcode=handledby_data["staffcode"])

        case, created = Case.objects.update_or_create(handledby=technician,
                                                        casetype=casetype,
                                                        scheduledate=scheduledate,
                                                        time=time,
                                                        action=action,
                                                        suggest=suggest,
                                                        comment=comment,
                                                        iscompleted=iscompleted,
                                                        customer=userTemp)
        case.save()

        if(created):
            for machine_data2 in machines_data:
                m = Machine.objects.get(machineid=machine_data2["machineid"])
                case.machines.add(m)
            for filter_data2 in filters_data:
                case.filters.add(Filter.objects.get(filtercode=filter_data2["filtercode"]))






        return case
