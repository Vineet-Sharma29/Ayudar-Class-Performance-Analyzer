from rest_framework import serializers
from dashboard.models import course_dashboard
from .models import User
class userlogserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


class equationlogserializer(serializers.ModelSerializer):
    professor = userlogserializer()
    class Meta:
        model = course_dashboard
        fields = (
            'professor',
            'course_difficulty',
            'course_average',
            
        )
        read_only_fields=('force',)

    def create(self, validated_data):
        userlogid_data = validated_data.pop('userlogid')
        userlogid = UserLog.objects.create(**userlogid_data)
        mass = validated_data['mass']
        accelaration = validated_data['accelaration']
        force = float(mass)*float(accelaration)
        p=equation.objects.create(mass=mass,accelaration=accelaration,force=force,userlogid=userlogid)
        return p