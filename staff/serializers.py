from rest_framework.serializers import ModelSerializer
from staff.models import Staff
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'email', 'role']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, staff):
        token = super().get_token(staff)
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom data
        data['id'] = self.user.id
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
