
from ast import Add
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Blog, Comment
from account.models import MyUser
from django.core.paginator import Paginator
from .tasks import task_func
from django.views.generic import View, TemplateView,ListView,UpdateView,CreateView
from .forms import blogform


# Create your views here.

class Add_blog(CreateView):
    form_class = blogform
    template_name = "blog/newblog.html"
    success_url='my-blog'
    def form_valid(self, form):
        form.instance.blog_auther=self.request.user
        messages.success(self.request,'blog added send for admin approval')
        
        task_func.delay(
                message="An auther wants to add new blog",
                title="Blog addition Request",
                receiver=[user.user_email for user in MyUser.objects.isstaff()],
            )
        return super().form_valid(form)
    
class My_blog(ListView):
    model = Blog
    template_name = "blog/myblog.html"
    paginate_by = 5
    paginate_orphans = 1

    def get_queryset(self):
        return Blog.objects.isapproved().filter(blog_auther=self.request.user.id)

class Blogupdate(UpdateView):
    template_name = "blog/updateblog.html"
    form_class=blogform
    success_url='/blog/my-blog'
    model=Blog
    def form_valid(self,form):
        form.instance.blog_is_approved=False
        form.instance.blog_new_request=True
        messages.success(self.request,'blog updated sent for admin approval')
        task_func.delay(
            message="An auther wants to update blog",
                title="Blog updation Request",
                receiver=[user.user_email for user in MyUser.objects.isstaff()],
        )
        return super().form_valid(form)


class Blogdelete(View):
    def get(self, request, slug):
        blog_object = Blog.objects.get(slug=slug)
        blog_object.blog_del_request = True
        blog_object.save()
        messages.success(
            request, "send for admin approval to delete the blog"
        )
        user_object = MyUser.objects.isstaff()

        task_func.delay(
            message="An auther wants to delete their blog",
            title="Blog Deletion Request",
            receiver=[user.user_email for user in user_object],
        )
        return redirect("add-blog")

class Open_blog(TemplateView):

    template_name = "blog/singleblog.html"

    def get(self, request, slug):
        blog_object = Blog.objects.filter(slug=slug)

        p = Paginator(
            Comment.objects.filter(blog_key__slug=slug).order_by(
                "-comment_added_on"
            ),
            7,
        )
        page = request.GET.get("page")
        comment_paginate = p.get_page(page)
        return render(
            request,
            "blog/singleblog.html",
            {"blogs": blog_object, "page_obj": comment_paginate},
        )


class Addcomment(View):
    def post(self, request, slug):
        comment_blog = request.POST["com"]
        if request.user.is_authenticated:
            blog_object = Blog.objects.get(slug=slug)
            comment_object = Comment(
                user=get_object_or_404(MyUser, id=request.user.id),
                blog_key=get_object_or_404(Blog, id=blog_object.id),
                blog_comment=comment_blog,
            )
            comment_object.save()
            blog_object = Blog.objects.get(slug=slug)

            return redirect("open-blog", slug)
        else:
            messages.warning(request, "please login")
            return redirect("sign-in")
