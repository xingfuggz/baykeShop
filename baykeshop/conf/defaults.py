from django.conf import settings


bayke_defaults = {
    
    "SITE_HEADER": "BaykeShop",
    "SITE_TITLE": "BaykeShop",
    "PC_LOGO": "BaykeShop",
    
    # 后台自定义菜单开关
    "ADMIN_MENUS": False,
    
    # 商品列表页分页数量
    "PAGE_SIZE": 16,
    "MAX_PAGE_SIZE": 1000,
    
    # 是否开启按分类搜索功能
    "HAS_SEARCH_CATEGORY": True,
    
    # 手机号验证规则
    "PHONE_REGX": r"^1[35678]\d{9}$",
    
    # PC端登录后跳转配置
    "LOGIN_NEXT_PAGE": "baykeshop:home",
    
    # 支付宝相关配置
    "ALIPAY_PRIVATE_KEY":"baykeshop/module/payment/alipay/keys/app_private_key.pem",
    "ALIPAY_PUBLIC_KEY": "baykeshop/module/payment/alipay/keys/app_public_key.pem",
    "ALIPAY_APPID": "2021000116697536",
    "ALIPAY_NOTIFY_URL": "baykeshop:alipay_notify",
    "ALIPAY_RETURN_URL": "baykeshop:alipay_notify",
    "ALIPAY_SIGN_TYPE": "RSA2",  # RSA 或者 RSA2
    "ALIPAY_DEBUG": settings.DEBUG,
    "ALIPAY_TIMOUT": 15,
    # 支付宝回调页模版，一个模版路径字符串
    "ALIPAYNOTIFY_TEMPLATE_NAME": None,
    
    
    # tinymce富文本编辑器默认配置
    "TINYMCE_CDN": False,
    "TINYMCE_API_KEY": "no-api-key",   # 当TINYMCE_CDN未True时，必须设置该项为你的api-key,否则不能正确加载
    "TINYMCE_DEFAULTS": {
        # 向用户展开展示的工具栏
        'toolbar': 'undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons',
        # 选择要在加载时包含的插件
        'plugins': [
            'advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'preview', 'anchor', 'pagebreak',
            'searchreplace', 'wordcount', 'visualblocks', 'visualchars', 'code', 'fullscreen', 'insertdatetime',
            'media', 'table', 'emoticons', 'template', 'help'
        ],
        "browser_spellcheck": True,
        "contextmenu": False,
        'image_title': False,
        'automatic_uploads': True,
        'images_file_types': 'jpg,svg,webp,png,gif',
        'file_picker_types': 'file image media',
        'images_upload_url': '/upload/tinymce/',
        'images_reuse_filename': True,   # 是否开启每次为文件生成唯一名称
    },
    
    
    # 是否开启邮件通知
    'HAS_MESSAGE_EAMIL': True
}