from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from api.models import Surtidor


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class TokenObtainSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Usuario o contraseña incorrectos'
    }

    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        token['role'] = user.groups.first().id
        return token


class GroupWithIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = GroupWithIdSerializer(many=False, read_only=True, source='groups.first')
    role_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'role_id', 'first_name', 'last_name']

    def create(self, validated_data):
        try:
            role = validated_data.pop('role_id')
            group = Group.objects.get(pk=role)
            user = User.objects.create_user(
                **validated_data,
                username=validated_data['email'],
            )
            user.groups.add(group)
            return user
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'Este correo ya está en uso'})
        except Group.DoesNotExist:
            raise serializers.ValidationError({'detail': 'El rol no existe'})

    def update(self, instance, validated_data):
        try:
            role = validated_data.pop('role_id')
            group = Group.objects.get(pk=role)
            instance.groups.clear()
            instance.groups.add(group)
            if 'email' in validated_data and User.objects.filter(email=validated_data['email']).exclude(
                    pk=instance.pk).exists():
                raise IntegrityError
            # encrypt the password if it was changed
            if 'password' in validated_data:
                instance.set_password(validated_data['password'])
            validated_data.pop('password')
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'Este correo ya está en uso'})
        except Group.DoesNotExist:
            raise serializers.ValidationError({'detail': 'El rol no existe'})


class SurtidorSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    users_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='users',
        write_only=True,
        many=True
    )

    class Meta:
        model = Surtidor
        fields = ['id', 'nombre', 'latitud', 'longitud', 'users', 'users_ids']

    def validate(self, attrs):
        for user_id in attrs['users']:
            if self.instance:
                if Surtidor.objects.filter(users=user_id).exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError({'detail': 'Uno de los usuarios está asignado a otro surtidor'})
            else:
                if Surtidor.objects.filter(users=user_id).exists():
                    raise serializers.ValidationError({'detail': 'Uno de los usuarios está asignado a otro surtidor'})
            if User.objects.filter(pk=user_id.id).first().groups.first().name not in ['Vendedor',
                                                                                      'Administrador de Surtidor']:
                raise serializers.ValidationError(
                    {'detail': 'Uno de los usuarios no es vendedor o administrador de surtidor'})
        return attrs


class SurtidorWithoutUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surtidor
        fields = ['id', 'nombre', 'latitud', 'longitud']
