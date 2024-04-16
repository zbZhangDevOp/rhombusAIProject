from django.shortcuts import render
from django.http import JsonResponse
from .models import UploadedFile
from .data_processor import infer_and_convert_data_types
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_and_process_file(request):
    if request.method == 'POST':
        uploaded_file = UploadedFile(file=request.FILES['file'])
        uploaded_file.save()

        # Process the file
        file_path = uploaded_file.file.path
        processed_df = infer_and_convert_data_types(file_path)

        # Get data types of the processed DataFrame
        data_types = processed_df.dtypes.apply(lambda x: x.name).to_dict()

        # Convert DataFrame to JSON
        processed_data = processed_df.to_json(orient='records')


        return JsonResponse({'data': processed_data, 'dataTypes': data_types}, status=200)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)