from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import openai
import os
import json
import logging

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
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=70
        )

        description = response.choices[0].text.strip()

        return Response({'description': description}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Logger exclusivo para los errores del frontend
frontend_logger = logging.getLogger('frontend')

@api_view(['POST'])
def log_frontend_error(request):
    """
    Vista para capturar los errores del frontend y registrarlos en un archivo de logs.
    """
    if request.method == 'POST':
        try:
            # Lee el cuerpo de la solicitud que contiene el error
            data = json.loads(request.body)
            message = data.get('message', 'No message')
            source = data.get('source', 'No source')
            lineno = data.get('lineno', 'No line number')
            colno = data.get('colno', 'No column number')
            error = data.get('error', 'No error detail')

            # Registra el error en el archivo de logs para el frontend
            frontend_logger.error(f"[Frontend Error] {message} at {source}, line {lineno}, column {colno}: {error}")

            # Retorna una respuesta exitosa
            return JsonResponse({'status': 'error logged'}, status=200)
        except Exception as e:
            frontend_logger.error(f"[Frontend Error] Failed to log error: {str(e)}")
            return JsonResponse({'status': 'error processing request'}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)
