from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required=True,style={'input_type':'password'})
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name','password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            password = validated_data['password'],)
        
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =("id","email","username","first_name","last_name","is_active","date_joined")
        read_only_fields = ('id', 'is_active', 'date_joined')
