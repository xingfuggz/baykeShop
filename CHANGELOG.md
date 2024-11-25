# 更新日志

## [1.3.4] - 2024.11.25

### 优化

* 后台用户列表显示字段优化，增加显示头像，隐藏原有姓和名字段，内联扩展用户信息模块。

* 加入对上传图片大小验证，初始限制为2M。

* 加入对用户手机号及收货地址手机号格式验证。

* 优化文章列表显示，对发布文章作者取消必填验证。

* 优化文章详情相关显示字段....

### 新增

* 新增`validate_phone`手机号验证器，路径：`baykeshop.apps.core.validators`

* 新增`validate_image_size`图片大小验证器，路径：`baykeshop.apps.core.validators`

* 集成富文本编辑器quill，新增富文本编辑器字段`RichTextField`，路径：`baykeshop.apps.core.fields`.

* 新增富文本编辑器小部件`QuillWidget`，路径：`baykeshop.apps.core.forms.widgets`.

* 新增访问量获取模版标签`visit_count`，路径：`baykeshop.apps.core.templatetags.bayke`

