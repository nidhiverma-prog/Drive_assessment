from rest_framework import serializers
from django.contrib.auth  import authenticate
from rest_framework import exceptions
from myapp.models import Movies

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):
        username=data.get("username" ,"")
        password=data.get("password","")

        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data['user']=user
                else:
                    msg="user is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg="Unable to login with given credentials"
                raise exceptions.ValidationError(msg)    
        
        else:
            msg="must provie username and password"
            raise exceptions.ValidationError(msg)
        return data    

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movies
        fields=(
            'id',
            'title',
            'reviews'
        )        