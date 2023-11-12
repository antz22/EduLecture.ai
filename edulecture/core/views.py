import os
import shutil

from .models import Subject, Lecture, User
from .serializers import SubjectSerializer, LectureSerializer

from utils.audio import get_audio_length, get_audio_durations, generate_clone, generate_audio, generate_master_sound
from utils.video import generate_video
from utils.upload import upload

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

class SubjectList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class LectureList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        lectures = Lecture.objects.all()
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)


class UserLectureList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        lectures = Lecture.objects.filter(user=request.user)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = User.objects.get(username=request.data["user_name"])
        lectures = Lecture.objects.filter(user=user)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)


class SubjectLectureList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        subject = Subject.objects.get(name=request.data["subject"])
        lectures = Lecture.objects.filter(subject=subject)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)


# function to attach voice file to user
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def upload_voice(request):

    data = request.data
    user = request.user

    file = data["file"]
    name = data["name"]

    print("File uploaded: ")
    print(file)
    print("User's full name: " + name)

    user.voice_file = file
    user.name = name
    user.save()

    # run voice cloning function
    # Ruoming's key
    # API_KEY = "f5ef28538059549f46f9832bf9309ab6"
    # Anthony's key
    # API_KEY = "32e2a6e83130d6f0e6718bf99df3e474"
    API_KEY = "f6d5b3935e642e4f1c548ae7d4be465f"
    voice_id = generate_clone(user.voice_file.path, API_KEY)

    # save voice_id to user object
    user.voice_id = voice_id
    user.save()

    return Response(status=status.HTTP_200_OK)


# function to process uploaded lecture files
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def upload_slides(request):

    data = request.data
    user = request.user

    presentation_link = data["url"]
    title = data["title"]
    subject_name = data["subject"]
    description = data["description"]

    print("URL processed: " + presentation_link)

    # generate video lecture
    video_title = title.replace(" ", "-")
    user_path = f"media/user_{user.id}"
    presentation_id = presentation_link.split("/")[5]
    user_voice_file = user.voice_file.path
    user_voice_id = user.voice_id
    # print("User voice ID: " + user_voice_id)
    video_name = generate_video(presentation_id, user_voice_id, user_path, video_title, user_voice_file, user.name)

    print("Video generated!")

    shutil.rmtree(user_path + "/temp-files")

    subject = Subject.objects.get(name=subject_name)

    # create google drive video link
    video_link = upload(video_name, title)

    print("Video uploaded to Google Drive!")

    # create lecture object
    Lecture.objects.create(user=user, subject=subject, title=title, description=description, presentation_link=presentation_link, video_link=video_link)

    return Response(status=status.HTTP_200_OK)