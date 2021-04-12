from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs.order_by('-id').filter(post_published=True)
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comments__comment_published=True, then=1)
                )
            )
        )

        return qs


class PostSearch(PostIndex):
    template_name = 'posts/post_search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.egt('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(title__icontains=termo) |
            Q(author__first_name__iexact=termo) |
            Q(post_content__icontains=termo) |
            Q(post_excert__icontains=termo) |
            Q(post_category__name_cat__iexact=termo)
        )

        return qs


class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.kwargs.get('category', None)

        if not category:
            return qs

        qs = qs.filter(post_category__nome_cat__iexact=category)

        return qs


class PostDetails(UpdateView):
    pass
