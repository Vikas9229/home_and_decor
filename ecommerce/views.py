from django.shortcuts import render
from store.models import Product
# Create your views here.
def home(request):
    products=Product.objects.filter(is_available=True).order_by('-upload_date')
    context={
        'products':products,
    }
    
    return render(request,'home.html',context)

def decor_idea(request):
    template = 'decor/decor_idea.html'
    return render(request, template, {})

def home_solution(request):
    template = 'decor/home_solution.html'
    return render(request, template, {})

def interior_designers(request):
    template = 'decor/interior_designers.html'
    return render(request, template, {})

def events(request):
    template = 'decor/events.html'
    return render(request, template, {})

def vastu_shastra(request):
    template = 'decor/vastu_shastra.html'
    return render(request, template, {})

# content href

def img8_content(request):
    template = 'decor_content/decor_idea_content/img8_content.html'
    return render(request, template, {})

def img1_content(request):
    template = 'decor_content/decor_idea_content/img1_content.html'
    return render(request, template, {})

def img10_content(request):
    template = 'decor_content/decor_idea_content/img10_content.html'
    return render(request, template, {})

def img3_content(request):
    template = 'decor_content/decor_idea_content/img3_content.html'
    return render(request, template, {})

def imgdecor_content(request):
    template = 'decor_content/decor_idea_content/imgdecor_content.html'
    return render(request, template, {})



def img11_content(request):
    template = 'decor_content/decor_idea_content/img11_content.html'
    return render(request, template, {})

# home_solution content: 

def img12_content(request):
    template = 'decor_content/home_solution_content/img12_content.html'
    return render(request, template, {})

def img13_content(request):
    template = 'decor_content/home_solution_content/img13_content.html'
    return render(request, template, {})

def new1_content(request):
    template = 'decor_content/home_solution_content/new1_content.html'
    return render(request, template, {})

# interior designers fuction:-

def img15_content(request):
    template = 'decor_content/Interior_ designers_content/img15_content.html'
    return render(request, template, {})

def img16_content(request):
    template = 'decor_content/Interior_ designers_content/img16_content.html'
    return render(request, template, {})

def img17_content(request):
    template = 'decor_content/Interior_ designers_content/img17_content.html'
    return render(request, template, {})

def img18_content(request):
    template = 'decor_content/Interior_ designers_content/img18_content.html'
    return render(request, template, {})

def img19_content(request):
    template = 'decor_content/Interior_ designers_content/img19_content.html'
    return render(request, template, {})

def img20_content(request):
    template = 'decor_content/Interior_ designers_content/img20_content.html'
    return render(request, template, {})

def img21_content(request):
    template = 'decor_content/Interior_ designers_content/img21_content.html'
    return render(request, template, {})

def img22_content(request):
    template = 'decor_content/Interior_ designers_content/img22_content.html'
    return render(request, template, {})

def img23_content(request):
    template = 'decor_content/Interior_ designers_content/img23_content.html'
    return render(request, template, {})

def img24_content(request):
    template = 'decor_content/Interior_ designers_content/img24_content.html'
    return render(request, template, {})

# events function:

def img26_content(request):
    template = 'decor_content/events_content/img26_content.html'
    return render(request, template, {})

def img27_content(request):
    template = 'decor_content/events_content/img27_content.html'
    return render(request, template, {})

def img28_content(request):
    template = 'decor_content/events_content/img28_content.html'
    return render(request, template, {})

#vastu shastra:
def img29_content(request):
    template = 'decor_content/vastu_shastra_content/img29_content.html'
    return render(request, template, {})

def img30_content(request):
    template = 'decor_content/vastu_shastra_content/img30_content.html'
    return render(request, template, {})

def img31_content(request):
    template = 'decor_content/vastu_shastra_content/img31_content.html'
    return render(request, template, {})

def img32_content(request):
    template = 'decor_content/vastu_shastra_content/img32_content.html'
    return render(request, template, {})

def img33_content(request):
    template = 'decor_content/vastu_shastra_content/img33_content.html'
    return render(request, template, {})

def img34_content(request):
    template = 'decor_content/vastu_shastra_content/img34_content.html'
    return render(request, template, {})

def img35_content(request):
    template = 'decor_content/vastu_shastra_content/img35_content.html'
    return render(request, template, {})

def img36_content(request):
    template = 'decor_content/vastu_shastra_content/img36_content.html'
    return render(request, template, {})

def img37_content(request):
    template = 'decor_content/vastu_shastra_content/img37_content.html'
    return render(request, template, {})

def img38_content(request):
    template = 'decor_content/vastu_shastra_content/img38_content.html'
    return render(request, template, {})

def img39_content(request):
    template = 'decor_content/vastu_shastra_content/img39_content.html'
    return render(request, template, {})

def img40_content(request):
    template = 'decor_content/vastu_shastra_content/img40_content.html'
    return render(request, template, {})



