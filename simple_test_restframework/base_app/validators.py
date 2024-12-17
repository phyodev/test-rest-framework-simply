from rest_framework import serializers

def is_description_include(description):
    print(f"\n\n\n\n\n{description}\n\n\n\n\n")
    if description == '' or description == None:
        raise serializers.ValidationError('Description cannot be null or empty string.')
    # print(description)

def is_rating(rating):
    if rating < 1 or rating > 10:
        raise serializers.ValidationError('Rating has to be between 1 and 10.')