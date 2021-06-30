
from accounts.models import Student
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
import uuid
from base_rest.utils import *



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()
    
    

class ResetPasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'
        


class RegisterStudentSerializer(serializers.Serializer):
    uid = serializers.CharField(required =False)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required = True)
    student_name = serializers.CharField(required= True)
    phone_number = serializers.CharField(required= True)
    whatsapp_number = serializers.CharField(required= True)
    course = serializers.CharField(required= True)
    date_of_birth = serializers.CharField(required= True)
    gender = serializers.CharField(required= True)
    state = serializers.CharField(required= True)
    district = serializers.CharField(required= True)
    #accepted_terms = serializers.BooleanField(default=True)
    pincode = serializers.CharField(required= True)

    class Meta:
        model = Student
        fields = [ 'student_name',  'phone_number',  'whatsapp_number',  'course',  'date_of_birth',  'gender',  'state',  'district',  'pincode', ]
        
    def create(self , validated_data):
        student_obj = Student.objects.create(
            email= validated_data['email'],
            username = validated_data['email'],
            student_name = validated_data['student_name'],
            phone_number = validated_data['phone_number'],
            whatsapp_number = validated_data['whatsapp_number'],
            course = validated_data['course'],
            date_of_birth= validated_data['date_of_birth'],
            gender =validated_data['gender'],
            state = validated_data['state'],
            otp = get_random_otp(),
            district = validated_data['district'],
          
            pincode = validated_data['pincode'])
        student_obj.set_password(validated_data['password'])

        student_obj.save()
        
        return student_obj
    
    
    def forget_password(self , instance , validated_data):
        
        email = validated_data['email']
        
        print(email)
    
    
class StudentSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'country']

    
    def get_country(self, obj):
        print(obj)
        return "Nigeria"


        
    
    
        


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['email' , 'password']
  
        
    
           
        

# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(required=True)
#     token = serializers.CharField(required=True)
#     class Meta:
#         model = ForgetPassword
#         fields = ['token' , 'password']
        
#     def change_password(self):
#         validated_data = self.validated_data
#         forget_password_obj =  None
#         print(validated_data['token'])
#         try:
#             forget_password_obj = ForgetPassword.objects.get(forget_password_token=validated_data['token'])
#         except Exception as e:
#             raise serializers.ValidationError("invalid token")
        
#         user_obj = User.objects.get(id = forget_password_obj.user.id)
#         user_obj.set_password(validated_data['password'])
#         user_obj.save()
        
#         return True
        

class ForgetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['email']    
        
    def forget_password(self):
        email = self.validated_data['email']
        user_obj = None
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("invalid email user not found")
        
        token = str(uuid.uuid4())
        #ForgetPassword.objects.create(user = user_obj ,forget_password_token = token )
        return True
        
        