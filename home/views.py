from django.views.generic import ListView, TemplateView,DeleteView
from django.views import View

from django.http import HttpResponse
import csv
import io

from django.template.loader import get_template
from xhtml2pdf import pisa

from django.shortcuts import redirect, render
from blog.models import Blog, Search
from account.models import MyUser
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from .task import task_func
from datetime import datetime


# Create your views here.
class Index(ListView):
    model = Blog
    template_name = "home/index.html"
    paginate_by = 5
    paginate_orphans = 1

    def get_queryset(self):
        return Blog.objects.isapproved()


class Admin(TemplateView):
    template_name = "home/admin.html"

    def get_context_data(self):
        blog_object = Blog.objects.newrequest()
        user_object = MyUser.objects.isnotactive()
        blogsdelete_object = Blog.objects.deleterequest()
        context = {
            "user_object": user_object,
            "blogs_object": blog_object,
            "blogsdelete_object": blogsdelete_object,
        }
        return context


class Userapproval(View):
    def get(self, request, uid):
        user_object = MyUser.objects.get(id=uid)
        user_object.is_active = True
        user_object.save()
        messages.success(request, "approved user")
        user_object = MyUser.objects.get(id=uid)
        task_func.delay(
            message="your sign up request has been approved",
            title="user approval",
            receiver=[user_object.user_email],
        )
        return redirect("admin_custom")


class Blogapproval(View):
    def get(self, request, slug):
        blog_object = Blog.objects.get(slug=slug)
        blog_object.blog_is_approved = True
        blog_object.blog_new_request = False

        blog_object.save()
        messages.success(request, "approved blog")
        blog_object = Blog.objects.get(slug=slug)
        task_func.delay(
            message="your blog has been approved",
            title="blog approval",
            receiver=[blog_object.blog_auther.user_email],
        )

        return redirect("admin_custom")

class Blog_delete_approval(View):
    def get(self, request, slug):
        blog_object = Blog.objects.get(slug=slug)
        task_func.delay(
            message="your blog has been deleted",
            title="blog deletion approved",
            receiver=[blog_object.blog_auther.user_email],
        )
        blog_object.delete()

        messages.success(request, "blog removed")

        return redirect("admin_custom")


class Searching(View):
    def post(self, request):
        search_content = request.POST["search"]
        search_obj = Search.objects.filter(search_content=search_content)
        if search_obj.exists():
            return redirect("search1", search_content)
        else:
            blog = Blog.objects.isapproved()
            for i in blog:
                if search_content in i.blog_title:
                    search_object = Search(
                        object_blog=i, search_content=search_content
                    )
                    search_object.save()
            return redirect("search1", search_content)


class Search1(View):
    def get(self, request, search):
        search_obj = Search.objects.filter(search_content=search)
        p = Paginator(search_obj, 5)
        page = request.GET.get("page")
        blog_paginate = p.get_page(page)
        if search_obj:
            return render(
                request,
                "home/search.html",
                {"blog_paginate": blog_paginate},
            )
        else:
            messages.warning(request, "search result not found")
            return redirect("index")


class Blog_download(View):
    def post(self, request):
        fromtime = request.POST["from"]
        totime = request.POST["to"]
        downloads = request.POST["downloads"]
        mail = request.POST["mail"]
        if downloads == "csv" and fromtime != "" and totime != "":
            return redirect("blog-csv", fromtime, totime, mail)
        elif downloads == "pdf" and fromtime != "" and totime != "":
            return redirect("blog-pdf", fromtime, totime, mail)
        else:
            return redirect("/admin/blog/blog/")


class Blog_csv(View):
    def get(self, request, fromtime, totime, mail):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment;Filename=blogs.csv"

        writer = csv.writer(response)

        blog_object = Blog.objects.all()
        lst = []
        for i in blog_object:
            fromtime1 = datetime.strptime(fromtime, "%Y-%m-%d").date()
            totime1 = datetime.strptime(totime, "%Y-%m-%d").date()

            if (
                i.blog_uploaded_on.date() >= fromtime1
                and i.blog_uploaded_on.date() <= totime1
            ):
                lst.append(i)

        writer.writerow(
            [
                "Blog Title",
                "Blog auther",
                "Blog image",
                "Blog content",
                "Uploaded on",
            ]
        )
        filename = "blogs.csv"

        for blog in lst:
            writer.writerow(
                [
                    blog.blog_title,
                    blog.blog_auther,
                    blog.blog_image,
                    (blog.blog_content),
                    blog.blog_uploaded_on,
                ]
            )
        if mail == "sendmail":
            receiver = [
                user.user_email for user in MyUser.objects.isstaff()
            ]
            email = EmailMessage(
                "blog download",
                "message",
                "bhatttest852@gmail.com",
                receiver,
            )
            email.attach(filename, response.getvalue(), "text/csv")
            email.send(fail_silently=False)
            return redirect("/admin/blog/blog")
        return response


class Blog_pdf(View):
    def get(self, request, fromtime, totime, mail):
        blog_object = Blog.objects.all()
        lst = []
        for i in blog_object:
            fromtime1 = datetime.strptime(fromtime, "%Y-%m-%d").date()
            totime1 = datetime.strptime(totime, "%Y-%m-%d").date()
            if (
                i.blog_uploaded_on.date() >= fromtime1
                and i.blog_uploaded_on.date() <= totime1
            ):
                lst.append(i)

        # getting html to pdf

        context = {"blog_objects": lst}
        template = get_template("home/admin12.html")
        html = template.render(context)
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html.encode()), result)
        pdf = result.getvalue()
        filename = "blog.pdf"

        # sending mail

        if mail == "sendmail":
            receiver = [
                user.user_email for user in MyUser.objects.isstaff()
            ]
            email = EmailMessage(
                "blog download",
                "message",
                "bhatttest852@gmail.com",
                receiver,
            )
            email.attach(filename, pdf, "text/pdf")
            email.send(fail_silently=False)
            return redirect("/admin/blog/blog")

        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "blog.pdf"
            content = "inline; filename='%s'" % (filename)
            content = "attachment; filename=%s" % (filename)
            response["Content-Disposition"] = content
            return response

        return response
