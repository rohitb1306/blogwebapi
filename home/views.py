from cgi import test
from fileinput import filename
from urllib import response

from django.http import HttpResponse, FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.shortcuts import redirect, render
from blog.models import Blog, Search
from account.models import MyUser
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .task import task_func


# Create your views here.
def index(request):
    p = Paginator(Blog.objects.isapproved(), 5)
    page = request.GET.get('page')
    blog_paginate = p.get_page(page)

    # user_object = MyUser.objects.all()

    return render(request, "home/index.html", {"blog_paginate": blog_paginate})


def admin(request):
    blog_object = Blog.objects.newrequest()
    user_object = MyUser.objects.isnotactive()
    blogsdelete_object = Blog.objects.deleterequest()
    return render(
        request,
        "home/admin.html",
        {"blogs_object": blog_object, "user_object": user_object,
            "blogsdelete_object": blogsdelete_object},
    )


def userapproval(request, uid):

    user_object = MyUser.objects.get(id=uid)
    user_object.is_active = True
    user_object.save()
    messages.success(request, "approved user")
    user_object = MyUser.objects.get(id=uid)
    task_func.delay(message='your sign up request has been approved',
                    title='user approval', receiver=[user_object.user_email])

    return redirect("admin_custom")


def blogapproval(request, slug):

    blog_object = Blog.objects.get(new_slug=slug)
    blog_object.blog_is_approved = True
    blog_object.blog_new_request = False

    blog_object.save()
    messages.success(request, "approved blog")
    blog_object = Blog.objects.get(new_slug=slug)
    task_func.delay(message='your blog has been approved',
                    title='blog approval', receiver=[blog_object.blog_auther.user_email])

    return redirect("admin_custom")


def blog_Delete_approval(request, slug):

    blog_object = Blog.objects.get(new_slug=slug)
    task_func.delay(message='your blog has been deleted',
                    title='blog deletion approved', receiver=[blog_object.blog_auther.user_email])
    blog_object.delete()

    messages.success(request, "blog removed")

    return redirect("admin_custom")


def about(request):
    return render(request, 'home/about.html')


def search(request):
    if request.method == 'POST':
        search_content = request.POST['search']
    search_obj = Search.objects.filter(search_content=search_content)
    if search_obj.exists():
        return redirect('search1', search_content)
    else:
        blog = Blog.objects.isapproved()
        for i in blog:
            if search_content in i.blog_title:
                search_object = Search(
                    object_blog=i, search_content=search_content)
                search_object.save()
        return redirect('search1', search_content)


def search1(request, search):
    search_obj = Search.objects.filter(search_content=search)
    p = Paginator(search_obj, 5)
    page = request.GET.get('page')
    blog_paginate = p.get_page(page)
    if search_obj:
        return render(request, 'home/search.html', {"blog_paginate": blog_paginate})
    else:
        messages.warning(request, 'search result not found')
        return redirect('index')


def blog_csv(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment;Filename=blogs.csv'

    writer = csv.writer(response)

    blog_object = Blog.objects.isapproved()

    writer.writerow(['Blog Title', 'Blog auther',
                    'Blog image', 'Blog content', 'Uploaded on'])

    for blog in blog_object:
        writer.writerow([blog.blog_title, blog.blog_auther,
                        blog.blog_image, (blog.blog_content), blog.blog_uploaded_on])

    return response


def blog_pdf(request):
    # crete a bitestream buffer
    buffer_object = io.BytesIO()
    # create canvas
    canvas_var = canvas.Canvas(
        buffer_object, pagesize=letter, bottomup=0)
    # create text object
    text_object = canvas_var.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont("Helvetica", 14)
    blog_list = []

    blog_object = Blog.objects.isapproved()
    for blog in blog_object:
        blog_list.append(str(f'Title : {blog.blog_title}'))
        blog_list.append(str(f'Auther : {blog.blog_auther.user_name}'))
        blog_list.append(
            str(f'Date Uploaded : {blog.blog_uploaded_on.date()}'))
        blog_list.append("  ")
        blog_list.append(
            str(f'Image : http://127.0.0.1:8000{blog.blog_image.url}'))

        blog_list.append("  ")
        blog_list.append(str(f'Content : {blog.blog_content}'))
        blog_list.append("  ")

        blog_list.append(" ##################################################")
        blog_list.append("  ")

    c = 1
    for blog in blog_list:
        if c % 30 == 0:
            canvas_var.drawText(text_object)
            canvas_var.showPage()
            text_object = canvas_var.beginText()
            text_object.setTextOrigin(inch, inch)
            text_object.setFont("Helvetica", 14)

        text_object.textLines(blog)
        c += 1
    print(text_object)

    canvas_var.save()
    buffer_object.seek(0)
    return FileResponse(buffer_object, as_attachment=True, filename="blog.pdf")
