from django.db.models import Count,Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render , get_object_or_404,redirect,reverse
from .forms import CommentForm,PostForm
from .models import Post, Author ,PostView
from marketings.models import SignupNewsLetter 


def get_author(user) : 
    qs = Author.objects.filter(user=user)
    if qs.exists() : 
        return qs[0]
    else : 
        return None
def search(request) : 
    queryset = Post.objects.all() 
    query = request.GET.get('q') 
    if query : 
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset':queryset , 
    }
    return render(request,'search_results.html',context)
def get_category_counter() : 
    queryset= Post.objects.values('categories__title').annotate(Count("categories__title"))
    return queryset
def index(request) : 
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    if request.method == "POST" : 
        email = request.POST['email']
        email_object = SignupNewsLetter()
        email_object.email=email
        email_object.save()
        

    context =  {
        'objects_list' : featured , 
        'latest' : latest , 
    }

    return render(request,'index.html',context)



def blog(request) : 
    
    recent_posts = Post.objects.order_by("-timestamp")[0:3]
    post_list = Post.objects.all() 
    paginator = Paginator(post_list,5)
    page = request.GET.get('page')
    try : 
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger :
        paginated_queryset = paginator.page(1)
    except EmptyPage : 
        paginated_queryset = paginator.page(paginator.num_pages)
        
    context = {
        "queryset" : paginated_queryset ,
        "recent_posts": recent_posts,
        'category' : get_category_counter() ,

    }

    return render(request,'blog.html',context)
def post_create(request) : 
    title = "Create"
    form = PostForm(request.POST or None, request.FILES or None) 
    author = get_author(request.user)
    if request.method == "POST" : 
        if form.is_valid() : 
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail",kwargs = {
                'id' :form.instance.id
            }))
    context = {
        'title':title,
        'form' : form, 
    }
    return render(request,'create_post.html',context)

    
def post(request,id) :
    recent_posts = Post.objects.order_by("-timestamp")[0:3]
    post = get_object_or_404(Post,id=id)
    PostView.objects.get_or_create(user=request.user,post=post)
    comment_form = CommentForm(request.POST or None) 
    if request.method == 'POST'  : 
        if comment_form.is_valid() : 
            comment_form.instance.user = request.user
            comment_form.instance.post = post 
            comment_form.save()
    context = {
        'form':comment_form,
        'post':post , 
        "recent_posts": recent_posts,
        'category' : get_category_counter() ,

    } 

    return render(request,'post.html',context)

def post_update(request , id) : 
    title = "Update"
    post = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance = post) 
    author = get_author(request.user)
    if request.method == "POST" : 
        if form.is_valid() : 
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail",kwargs = {
                'id' :form.instance.id
            }))
    context = {
        'title':title,
        'form' : form, 
    }
    return render(request,'create_post.html',context)



def post_delete(request,id) : 
    post = get_object_or_404(Post,id=id)
    post.delete() 
    return redirect('all_blogs')