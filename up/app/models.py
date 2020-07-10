from django import forms
from django.db import models

from ..users.models import User


class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # レストラン名 文字列
    restaurant_name = models.CharField(
        verbose_name='',
        max_length=20,
        blank=True,
        null=True,
        help_text='タイトルはズバリ...！',
    )

    # レストランのメモ 大きめのテキストエリア
    restaurant_memo = models.TextField(
        verbose_name='',
        blank=True,
        null=True,
        help_text='もっと詳しく聞かせて...（写真も忘れずにね）',
    )

    # 23区の選択
    ward_choice = (
        ('千代田区', '千代田区'),
        ('中央区', '中央区'),
        ('港区', '港区'),
        ('新宿区', '新宿区'),
        ('文京区', '文京区'),
        ('台東区', '台東区'),
        ('墨田区', '墨田区'),
        ('江東区', '江東区'),
        ('品川区', '品川区'),
        ('目黒区', '目黒区'),
        ('大田区', '大田区'),
        ('世田谷区', '世田谷区'),
        ('渋谷区', '渋谷区'),
        ('中野区', '中野区'),
        ('杉並区', '杉並区'),
        ('豊島区', '豊島区'),
        ('北区', '北区'),
        ('荒川区', '荒川区'),
        ('板橋区', '板橋区'),
        ('練馬区', '練馬区'),
        ('足立区', '足立区'),
        ('葛飾区', '葛飾区'),
        ('江戸川区', '江戸川区'),
    )

    # 23区のプルダウン
    ward_address = models.CharField(
        verbose_name='住所（区）',
        choices=ward_choice,
        max_length=20,
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to='images/restaurant_posts', blank=True, null=True)

    # 価格帯 選択肢
    price_range_choice = (
        (1, '~500'),
        (2, '~1000'),
        (3, '~2000'),
    )

    # 価格帯 プルダウン
    price_range = models.IntegerField(
        verbose_name='予算',
        choices=price_range_choice,
        blank=True,
        null=True,
    )

    # サンプル項目9 選択肢（マスタ連動）
    sample_10 = models.ForeignKey(
        User,
        verbose_name='サンプル項目10_選択肢（マスタ連動）',
        blank=True,
        null=True,
        related_name='sample_10',
        on_delete=models.SET_NULL,
    )

    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.restaurant_name

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サンプル'
        verbose_name_plural = 'サンプル'
