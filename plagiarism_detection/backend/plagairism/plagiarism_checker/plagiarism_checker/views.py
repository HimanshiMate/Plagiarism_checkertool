from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .text_detection import detect_text_plagiarism
from .pdf_detection import detect_pdf_plagiarism
# from .image_detection import detect_image_plagiarism

@csrf_exempt
def detect_text(request):
    if request.method == 'POST':
        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')
        if text1 and text2:
            similarity = detect_text_plagiarism(text1, text2)
            return JsonResponse({'similarity': similarity})
        return JsonResponse({'error': 'Invalid input'}, status=400)

@csrf_exempt
def detect_pdf(request):
    if request.method == 'POST':
        pdf1 = request.FILES.get('pdf1')
        pdf2 = request.FILES.get('pdf2')
        if pdf1 and pdf2:
            similarity = detect_pdf_plagiarism(pdf1, pdf2)
            return JsonResponse({'similarity': similarity})
        return JsonResponse({'error': 'Invalid input'}, status=400)

# @csrf_exempt
# def detect_image(request):
#     if request.method == 'POST':
#         image1 = request.FILES.get('image1')
#         image2 = request.FILES.get('image2')
#         if image1 and image2:
#             similarity = detect_image_plagiarism(image1, image2)
#             return JsonResponse({'similarity': similarity})
#         return JsonResponse({'error': 'Invalid input'}, status=400)
