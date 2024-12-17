from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from rest_framework import serializers
from .models import Movie, Resource
from .validators import is_description_include, is_rating
from .utils import encode_id, decode_id

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff', 'groups']
    
    id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_id(self, obj):
        return encode_id(obj.id)
    
    def get_url(self, obj):
        request = self.context.get('request')
        encrypted_id = encode_id(obj.id)
        return request.build_absolute_uri(reverse('user-detail', args=[encrypted_id]))

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'url', 'name']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
    
    description = serializers.CharField(validators=[is_description_include], allow_null=False, required=False)
    rating = serializers.IntegerField(validators=[is_rating])

    def validate(self, data):
        if data['us_gross'] > data['worldwide_gross']:
            raise serializers.ValidationError('US gross cannot be greater than worldwide gross.')
        return data

    # def validate_rating(self, rating):
    #     if rating < 1 or rating > 10:
    #         raise serializers.ValidationError('Rating has to be between 1 and 10.')
    #     return rating

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.liked_by.count()
        liked_by_users = User.objects.filter(id__in=representation['liked_by'])
        representation['liked_by'] = UserSerializer(liked_by_users, many=True, context={'request': self.context.get('request')}).data
        # User.objects

        return representation