from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    # NOTE: This field is doing something quite interesting. The source argument controls which attribute is used to populate a field, and can point at any attribute on the serialized instance. It can also take the dotted notation shown above, in which case it will traverse the given attributes, in a similar way as it is used with Django's template language.

    # NOTE: The field we've added is the untyped ReadOnlyField class, in contrast to the other typed fields, such as CharField, BooleanField etc... The untyped ReadOnlyField is always read-only, and will be used for serialized representations, but will not be used for updating model instances when they are deserialized. We could have also used CharField(read_only=True) here.

    class Meta: # Defines the behavior of the class
        model = Snippet # Copies the structure from the Snippet model
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner',)

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    # Because 'snippets' is a reverse relationship on the User model, it will not be included by default when using the ModelSerializer class, so we needed to add an explicit field for it.

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
