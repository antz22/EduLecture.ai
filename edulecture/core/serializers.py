from rest_framework import serializers

from .models import Subject, Lecture


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'description',
        )

class LectureSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name')
    user_handle = serializers.CharField(source='user.username')
    subject_name = serializers.CharField(source='subject.name')
    time = serializers.DateTimeField(format="%I:%M%p %d %b, %Y")

    class Meta:
        model = Lecture
        fields = (
            'id',
            'user_name',
            'user_handle',
            'subject_name',
            'presentation_link',
            'video_link',
            'title',
            'description',
            'time',
        )