from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.forms import modelformset_factory
from django.shortcuts import render
from django.db.models.query import QuerySet

from .filters import ItemFilterSet
from .forms import ItemForm, PostForm, CommentForm, ImageForm
from .models import Item, Comment, Images, Like
from ..users.models import User, FriendShip
from django.contrib import messages
import re, json

# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin


def regex_format_space(incl_space_string):
    return re.sub(r"\u3000", " ", incl_space_string)


def get_video_extension_tuple():
    return (".MOV", ".mp4")


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
        context_data.update({'imageform': ImageForm})
        context_data["show_profile_icon"] = True
        context_data["images"] = Images.objects.all().order_by('-id')
        all_images = Images.objects.all().order_by('-id')

        image_dict = {}
        for image in all_images:
            # item_idとitem_idに紐づいている画像がまだ辞書に格納されていない場合
            if image.item_id not in image_dict:
                image_dict[image.item_id] = {}
                image_dict[image.item_id]["image"] = [
                    {"photo": image, "is_video": image.image.url.endswith(get_video_extension_tuple())}]
                image_dict[image.item_id]["post"] = Item.objects.get(
                    pk=image.item_id)
                item_obj = Item.objects.get(id=image.item_id)
                number_of_likes = item_obj.like_set.all().count()
                image_dict[image.item_id]["number_of_likes"] = number_of_likes
                try:
                    like_obj = Like.objects.get(user=self.request.user, picture=Item.objects.get(id=image.item_id))
                    already_liked = True
                except:
                    already_liked = False
                image_dict[image.item_id]["already_liked"] = already_liked
                # print("already liked", already_liked)
                # print(image.item_id, ": ", number_of_likes)
            # item_idとitem_idに紐づいている画像が辞書に格納されている場合
            else:
                image_dict[image.item_id]["image"].append(
                    {"photo": image, "is_video": image.image.url.endswith(get_video_extension_tuple())})
        context_data["image_dict"] = image_dict
        context_data["show_left"] = False
        context_data["show_right"] = False
        context_data["show_postbutton"] = True
        context_data["show_plus_button"] = True
        context_data["length"] = len(image_dict)
        return context_data

    def post(self, request, *args, **kwargs):
        postForm = PostForm(request.POST)
        lis = request.FILES.getlist('image')
        for i in lis:
            print(i)
        image_form = ImageForm(request.FILES)
        if postForm.is_valid():
            item = postForm.save(commit=False)
            item.restaurant_memo = regex_format_space(
                request.POST['restaurant_memo'])
            item.restaurant_name = regex_format_space(
                request.POST['restaurant_name'])
            item.created_by = self.request.user
            item.created_at = timezone.now()
            item.updated_by = self.request.user
            item.updated_at = timezone.now()
            item.save()
            if image_form.is_valid:
                for image in lis:
                    image_instance = Images(
                        image=image, item=item
                    )
                    image_instance.save()

            messages.success(request, f'投稿が完了しました！')
            return HttpResponseRedirect(self.success_url)

        return render(request, "/", {'form': postForm})


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
    form_class = PostForm
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data.update({'form_for_post': PostForm})
        context_data.update({'imageform': ImageForm})
        context_data["show_profile_icon"] = True
        return context_data

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

    def post(self, request, *args, **kwargs):
        postForm = PostForm(request.POST)
        lis = request.FILES.getlist('image')
        image_form = ImageForm(request.FILES)
        if postForm.is_valid():
            item = postForm.save(commit=False)
            item.restaurant_memo = regex_format_space(
                request.POST['restaurant_memo'])
            item.restaurant_name = regex_format_space(
                request.POST['restaurant_name'])
            item.created_by = self.request.user
            item.created_at = timezone.now()
            item.updated_by = self.request.user
            item.updated_at = timezone.now()
            item.save()
            if image_form.is_valid:
                for image in lis:
                    if image.name.endswith(get_video_extension_tuple()):
                        print("is video")
                    else:
                        print("is not video")
                    image_instance = Images(
                        image=image, item=item
                    )
                    image_instance.save()
            messages.success(request, f'投稿が完了しました！')
            return HttpResponseRedirect(self.success_url)

        return render(request, "/", {'form': postForm})


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

        images = Images.objects.filter(
            item_id=context["item"].id).order_by('id').reverse().all()

        image_dict = {}
        for image in images:
            if image.image.url.endswith(get_video_extension_tuple()):
                image.is_video = True
            else:
                image.is_video = False
        context["images"] = images
        context["images_cnt"] = len(images)

        if len(images) >= 2:
            context["is_multiple_photos"] = True
        else:
            context["is_multiple_photos"] = False

        context["show_postbutton"] = False
        context["show_profile_icon"] = True
        context["show_left"] = False
        context["show_right"] = False
        context["show_plus_button"] = False
        # context["object"].id is the id of the item
        form = CommentForm(initial={"item": context["object"].id})
        context["comment_form"] = form
        context["comments"] = Comment.objects.filter(
            item_id=context['object'].id).order_by('commented_date').reverse()
        followee_id = Item.objects.get(id=context["object"].id).created_by_id
        try:
            follower_id = User.objects.get(id=self.request.user.id).id
        except:
            follower_id = followee_id

        if follower_id != followee_id:
            context["show_follow_button"] = True
            context["is_own_post"] = False
        else:
            # if follower_id is not same as followee_id
            # AND if user is logged in
            if self.request.user.id is None:
                context["is_own_post"] = False
            else:
                context["is_own_post"] = True

        # if is_follow is above 0, it shows that there is a connection between the two
        is_following = len(FriendShip.objects.filter(
            followee_id=followee_id, follower_id=follower_id)) > 0
        context["is_following"] = is_following
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment_item = form.save(commit=False)
            comment_item.item_id = request.POST['item_id']
            comment_item.comment_text = regex_format_space(
                request.POST['comment_text'])
            comment_item.author = self.request.user
            comment_item.commented_date = timezone.now()
            comment_item.approved_comment = True
            comment_item.save()
            messages.success(request, f'コメントの投稿されました！')
            return HttpResponseRedirect(request.path)

        return render(request, "/", {'form': form})


class CampaignPageView(TemplateView):
    template_name = "app/campaign.html"

class GatePageView(TemplateView):
    template_name = "app/gate.html"


def test_ajax_response(request):
    follower_username = request.user
    followee_username = request.POST["followee-name"]
    is_follow = int(request.POST["is-follow"])
    follower = User.objects.filter(username=follower_username).first()
    followee = User.objects.filter(username=followee_username).first()
    if is_follow:
        friendship = FriendShip(follower=follower, followee=followee)
        friendship.save()
        message = "フォロー中"
    else:
        FriendShip.objects.filter(
            follower=follower, followee=followee).delete()
        message = "フォロー"
    return HttpResponse(message)


def like_ajax_response(request):
    new_like, created = Like.objects.get_or_create(user=request.user, picture=Item.objects.get(id=request.POST["post-id"]))
    if not created:
        # the user already liked this picture before = unlike
        print("DELETE OBJECT")
        Like.objects.filter(user=request.user, picture=Item.objects.get(id=request.POST["post-id"])).delete()
    else:
        print("CREATED")
    item = Item.objects.get(id=request.POST["post-id"])
    number_of_likes = item.like_set.all().count()
    dic_json = {"number_of_likes": number_of_likes, "item_id": request.POST["post-id"]}
    return HttpResponse(json.dumps(dic_json), content_type="application/json")
