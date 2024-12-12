from rest_framework import serializers

class TranscriptAudioSerializer(serializers.Serializer):
    url = serializers.URLField()
    start_time = serializers.FloatField()

class IntroSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()
    with_audio = serializers.BooleanField()

class ContentSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()
    with_audio = serializers.BooleanField()

class PostRequestSerializer(serializers.Serializer):
    transcript_audio = TranscriptAudioSerializer(many=True)
    intro = IntroSerializer(many=True)
    content = ContentSerializer(many=True)
