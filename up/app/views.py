from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .filters import ItemFilterSet
from .forms import ItemForm, PostForm, CommentForm
from .models import Item, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re

# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin


def regex_format_space(incl_space_string):
    return re.sub(r"\u3000", " ", incl_space_string)


class ItemFilterView(FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Item
    form_class = PostForm

    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10
    success_url = reverse_lazy('index')

    API_KEY = "7fcef725a068a78b7270e0cad04c289b"
    url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session:
                if isinstance(request.session['query'], dict):
                    if 'page' in request.session['query'].keys():
                        request.session['query'] = request.session['query'].pop(
                            'page')
        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return Item.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data.update({'form': PostForm})
        context_data["show_profile_icon"] = True
        context_data["show_left"] = False
        context_data["show_right"] = False
        context_data["show_postbutton"] = True
        context_data["show_plus_button"] = True
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            item = form.save(commit=False)
            item.image = request.FILES['image']
            item.restaurant_memo = regex_format_space(
                request.POST['restaurant_memo'])
            item.restaurant_name = regex_format_space(
                request.POST['restaurant_name'])
            item.created_by = self.request.user
            item.created_at = timezone.now()
            item.updated_by = self.request.user
            item.updated_at = timezone.now()
            item.save()
            messages.success(request, f'投稿ありがとうございます!')
            return HttpResponseRedirect(self.success_url)

        return render(request, "/", {'form': form})


class ItemDetailView(DetailView):
    """
    ビュー：詳細画面
    """
    model = Item

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        return super().get_context_data(**kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """
        item = form.save(commit=False)
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        更新処理
        """
        item = form.save(commit=False)
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Item
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(self.success_url)


class CardDetailPageView(DetailView):
    model = Item
    template_name = "app/card_detail.html"
    form_class = CommentForm
    success_url = reverse_lazy('index')

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)


    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'

        context = super().get_context_data(**kwargs)
        context["show_postbutton"] = False
        context["show_profile_icon"] = False
        context["show_left"] = False
        context["show_right"] = False
        context["show_plus_button"] = False
        form = CommentForm(initial={"item": context["object"].id})
        context["comment_form"] = form
        context["comments"] = Comment.objects.filter(item_id=context['object'].id).order_by('commented_date').reverse()
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment_item = form.save(commit=False)
            comment_item.item_id = request.POST['item_id']
            comment_item.comment_text = regex_format_space(request.POST['comment_text'])
            comment_item.author = self.request.user
            comment_item.commented_date = timezone.now()
            comment_item.approved_comment = True
            comment_item.save()
            messages.success(request, f'コメント投稿ありがとうございます!')
            return HttpResponseRedirect(request.path)

        return render(request, "/", {'form': form})


class CampaignPageView(TemplateView):
    template_name = "app/campaign.html"


def test_ajax_response(request):
    input_text = request.POST.getlist("name_input_text")
    hoge = "Ajax Response: " + input_text[0]
    print(input_text)

    return HttpResponse(hoge)
