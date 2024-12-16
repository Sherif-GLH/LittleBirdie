from rest_framework.views import APIView
from .serializers import PostRequestSerializer
from rest_framework.response import Response
from.tasks import create_video_task

class CreateVideoView(APIView):
    def post(self, request):
        serializer = PostRequestSerializer(data=request.data)
        if serializer.is_valid():
            transcript_audio = serializer.validated_data['transcript_audio']
            intro = serializer.validated_data['intro']
            content = serializer.validated_data['content']
            create_video_task.delay(intro, transcript_audio, content)
        return Response({'respose': "success"})