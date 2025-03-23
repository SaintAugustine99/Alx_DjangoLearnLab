from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, PostForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

def post_list(request):
    posts = Post.objects.order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # Get all comments for this post
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': None
    })

@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', pk=post_id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/comment_form.html', {
        'form': form,
        'post': post
    })

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check if the logged-in user is the author of the comment
    if request.user != comment.author:
        messages.error(request, "You can't edit someone else's comment.")
        return redirect('post_detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated!')
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/comment_edit.html', {'form': form, 'comment': comment})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check if the logged-in user is the author of the comment
    if request.user != comment.author:
        messages.error(request, "You can't delete someone else's comment.")
        return redirect('post_detail', pk=comment.post.pk)
    
    post_pk = comment.post.pk
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
        return redirect('post_detail', pk=post_pk)
    
    return render(request, 'blog/comment_delete.html', {'comment': comment})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    return render(request, 'blog/profile.html', context)

# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update an existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Class-based comment views (alternative to function-based views)
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_id']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
    
# Adding search functionality

def search_posts(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tags__name__icontains=query)
        ).distinct()
    
    return render(request, 'blog/search_results.html', {
        'query': query,
        'results': results
    })

def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.all()
    
    return render(request, 'blog/tag_posts.html', {
        'tag': tag,
        'posts': posts
    })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Save tags (handled in the form's save method)
            form.save_m2m()
            messages.success(request, 'Your post has been created!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user is the author
    if request.user != post.author:
        messages.error(request, "You can't edit someone else's post.")
        return redirect('post_detail', pk=post.pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form})