from rest_framework.views import APIView
from .serializers import PostRequestSerializer
from rest_framework.response import Response
from .Main import create_video

class CreateVideoView(APIView):
    def post(self, request):
        serializer = PostRequestSerializer(data=request.data)
        if serializer.is_valid():
            transcript_audio = serializer.validated_data['transcript_audio']
            intro = serializer.validated_data['intro']
            content = serializer.validated_data['content']
            path = create_video( intro, transcript_audio, content)
            url = f"https://.s3.amazonaws.com/{path}"
        return Response({'url': f"{path}"})