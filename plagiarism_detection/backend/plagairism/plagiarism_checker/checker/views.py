

import requests
from django.shortcuts import render
from .utils import extract_text_from_pdf, extract_text_from_image, preprocess_text, calculate_similarity
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
import urllib.parse
from django.shortcuts import render
from django.http import HttpResponse
from checker.forms import RegistrationForm,LoginForm
from checker.models import RegiModel



def google_search(query):
    """Fetch search results from Google for a given query."""
    query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={query}&num=10"  # Fetch top 10 results
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract snippets from search results
    snippets = []
    for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
        snippets.append(g.get_text())
    
    return snippets

def calculate_plagiarism_percentage(original_text, snippets):
    """Calculate plagiarism percentage based on snippets found in search results."""
    if not snippets:
        return 0  # No snippets means no plagiarism
    
    total_similarity = 0
    snippet_count = len(snippets)
    
    for snippet in snippets:
        similarity = fuzz.ratio(original_text, snippet)
        total_similarity += similarity
    
    # Average similarity percentage
    average_similarity = total_similarity / snippet_count
    
    return min(average_similarity, 100)  # Ensure it doesn't exceed 100%

def read_text_from_file(file):
    """Read text from uploaded file."""
    return file.read().decode('utf-8')

def fetch_text_from_url(url):
    """Fetch content from a provided URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException:
        return None


def detect_ai_content(text):
    """Detect AI-generated content using RapidAPI AI content detector."""
    url = "https://ai-content-detector-ai-gpt.p.rapidapi.com/api/detectText/"
    
    payload = { "text": text }
    headers = {
        "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",  # Replace with your actual key
        "x-rapidapi-host": "ai-content-detector-ai-gpt.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
        
        # Debugging print to verify the response structure
        print("API Response:", data)  # You can remove this once verified

        # Assuming 'isAIContent' is the correct key; update if different
        return data.get("isAIContent", False)  
    
    except requests.exceptions.RequestException as e:
        print("Error in API request:", e)  # Log any API errors
        return None  # Return None on error for clarity



def check_plagiarism(request):
    context = {
        'plagiarism_percentage': None,
        'error_message': None,
        'original_content_message': None,
        'ai_content_message': None
    }

    if request.method == 'POST':
        input_method = request.POST.get('input_method')
        content_to_check = None  # Initialize content_to_check to avoid uninitialized errors

        # Determine input method and extract content
        if input_method == 'text':
            content_to_check = request.POST.get('input_text')
        elif input_method == 'url':
            url = request.POST.get('url')
            content_to_check = fetch_text_from_url(url)
            if not content_to_check:
                context['error_message'] = 'Unable to fetch content from the provided URL.'
        elif input_method == 'file':
            file = request.FILES.get('document')
            if file:
                if file.name.endswith('.pdf'):
                    content_to_check = extract_text_from_pdf(file)
                elif file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    content_to_check = extract_text_from_image(file)
                else:
                    context['error_message'] = "Unsupported file format."

        # Proceed if content is available
        if content_to_check:
            # Detect AI-generated content
            is_ai_content = detect_ai_content(content_to_check)
            if is_ai_content is True:
                context['ai_content_message'] = "Content appears to be AI-generated."
            elif is_ai_content is False:
                context['ai_content_message'] = "Content does not appear to be AI-generated."

            # Check plagiarism with Google snippets
            snippets = google_search(content_to_check)
            if snippets:
                plagiarism_percentage = calculate_plagiarism_percentage(content_to_check, snippets)
                context['plagiarism_percentage'] = plagiarism_percentage

                # Provide messages based on plagiarism threshold
                if plagiarism_percentage > 20:  # Example threshold
                    context['error_message'] = f"Plagiarism detected: {plagiarism_percentage:.2f}% copied from other sources."
                else:
                    context['original_content_message'] = "Content appears to be original."
            else:
                context['error_message'] = "No similar content found in search results."
        else:
            # If no valid content was provided or extraction failed
            if 'error_message' not in context or context['error_message'] is None:
                context['error_message'] = 'Please provide valid input.'

    return render(request, 'check.html', context)


# def check_plagiarism(request):
#     context = {
#         'plagiarism_percentage': None,
#         'error_message': None,
#         'original_content_message': None,
#         'ai_content_message': None
#     }

    # if request.method == 'POST':
    #     input_method = request.POST.get('input_method')

    #     if input_method == 'text':
    #         content_to_check = request.POST.get('input_text')
    #     elif input_method == 'url':
    #         url = request.POST.get('url')
    #         content_to_check = fetch_text_from_url(url)
    #         if not content_to_check:
    #             context['error_message'] = 'Unable to fetch content from the provided URL.'
    #     elif input_method == 'file':
    #         file = request.FILES.get('document')
    #         if file:
    #             if file.name.endswith('.pdf'):
    #                 content_to_check = extract_text_from_pdf(file)
    #             elif file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
    #                 content_to_check = extract_text_from_image(file)
    #             else:
    #                 context['error_message'] = "Unsupported file format."

    #     # if content_to_check:
    # # # Detect AI-generated content
    # #         is_ai_content = detect_ai_content(content_to_check)
    # #         if is_ai_content is True:
    # #             context['ai_content_message'] = "Content appears to be AI-generated."
    # #         elif is_ai_content is False:
    # #             context['ai_content_message'] = "Content does not appear to be AI-generated."
    # #     else:
    # #         context['error_message'] = "Error in AI detection."


    #     if content_to_check:
    #         # Check for AI-generated content
    #         is_ai_content = detect_ai_content(content_to_check)
    #         if is_ai_content:
    #             context['ai_content_message'] = "Content appears to be AI-generated."

    #         # Check plagiarism with Google snippets
    #         snippets = google_search(content_to_check)
    #         if snippets:
    #             plagiarism_percentage = calculate_plagiarism_percentage(content_to_check, snippets)
    #             context['plagiarism_percentage'] = plagiarism_percentage

    #             # Provide messages based on plagiarism threshold
    #             if plagiarism_percentage > 20:  # Example threshold
    #                 context['error_message'] = f"Plagiarism detected: {plagiarism_percentage:.2f}% copied from other sources."
    #             else:
    #                 context['original_content_message'] = "Content appears to be original."
    #         else:
    #             context['error_message'] = "No similar content found in search results."
    #     else:
    #         context['error_message'] = 'Please provide valid input.'

    # return render(request, 'check.html', context)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    form = LoginForm()
    if request.method=="POST":
        data = LoginForm(request.POST)
        if data.is_valid():
            Email = data.cleaned_data['email']
            Pass = data.cleaned_data['password']
            # print(email,password)
            user = RegiModel.objects.filter(email=Email)
            
            # if user:
            #     user = RegiModel.objects.get(email=Email)
                # print(user.stu_password)
                # if user.stu_password==password:
                #     name = user.stu_name
                #     email = user.stu_email
                #     contact = user.stu_mobile
                #     city = user.stu_city
                #     password = user.stu_password
                #     data = {
                #         'name':name,
                #         'email':email,
                #         'contact':contact,
                #         'city':city,
                #         'password':password
                #     }
                #     initial_data = {
                #                     'stu_name': name,
                #                     'stu_email': email
                #                 } 
                #     form1=QueryForm(initial=initial_data)
                #     data1 = StudentQuery.objects.filter(stu_email=email)
                #    return render(request,'dashboard.html',{'data':data,'query':form1,'query_detail':data1})
                # else:
                #     msg = "Email & Password not matched"
                #     return render(request,'login.html',{'form':form,'msg':msg})
        else:
            msg = "Email not register so please register first"
            return render(request,'login.html',{'form':form,'msg':msg})
    else:
        return render(request,'login.html',{'form':form})
    

def registration(request):

    form = RegistrationForm()
    if request.method=='POST':
        data = RegistrationForm(request.POST)
        if data.is_valid():
            Name=data.cleaned_data['username']
            Email=data.cleaned_data['email']
            Role=data.cleaned_data['role']
            Contact=data.cleaned_data['contact']
            Pass = data.cleaned_data['password']
            # print(name,email,city,contact,password)
            # data.save()
            user=RegiModel.objects.filter(email=Email)
            if user:
                msg="Email already exist"
                form=RegistrationForm()
                return render (request,'regi.html',{'form':form, 'msg':msg})
            else:
                data.save()
                msg="registration successfully"
                # form=RegistrationForm()
                return render(request,'regi.html',{'form':form,'msg':msg})
    else:
        return render(request,'regi.html',{'form':form})