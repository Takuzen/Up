from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    アプリケーション構成クラス
    管理画面での表示名を指定する
    """
    name = 'up.app'
    verbose_name = 'Up'
