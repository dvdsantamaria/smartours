from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import openai
import os

# CSRF Token endpoint
@api_view(['GET'])
def set_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

# Landmark description endpoint
@api_view(['POST'])
def generate_landmark_description(request):
    place_name = request.data.get('place_name')
    place_address = request.data.get('place_address')
    
    if not place_name or not place_address:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    # Prompt for OpenAI
    prompt = f"Provide a 70-word description about the following place: {place_name}, located at {place_address}"

    try:
        # Call OpenAI API for description generation
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=70
        )

        description = response.choices[0].text.strip()

        return Response({'description': description}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
