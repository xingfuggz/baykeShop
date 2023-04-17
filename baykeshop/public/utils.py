'''
@file            :utils.py
@Description     :小工具方法
@Date            :2022/03/21 18:03:29
@Author          :幸福关中 && 轻编程
@version         :v1.0
@EMAIL           :1158920674@qq.com
@WX              :baywanyun
'''

import os
import uuid
from django.conf import settings
from baykeshop.conf import bayke_settings

def generate_tree(source, parent):
    """分类递归算法

    Args:
        source (_list_): [{id: 1, name: 'nav', parent: None }, {id: 2, name: 'nav', parent: 1 }]
        parent (_None_): 根据此字段进行分类递归
    Returns:
        _type_: _description_. 递归嵌套
    """
    tree = []
    for item in source:
        if item["parent"] == parent:
            item["sub_cates"] = generate_tree(source, item["id"])
            tree.append(item)
    return tree


def _file_path(file_path=settings.MEDIA_ROOT / bayke_settings.FILE_PATH):
    """判断该路径是否存在不存在则创建
    """
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path


def _file_type(file, size=5120, file_type=['.jpg', '.png', '.gif', '.bmp', '.jpeg']):
    """判断上传文件类型并修改名称
    file：用request.FILES获取到的文件类型
    file_type: 允许上传的文件类型
    """
    if not (file.size / 1024) < size:
        print("图片大小超过额定大小5M")
        return False
    names = list(os.path.splitext(file.name))
    if names[1].lower() in file_type:
        names[0] = ''.join(str(uuid.uuid4()).split('-'))
        return names
    else:
        print('图片类型不允许')
        return False


def add_upload_file(file):
    """上传文件
    file：用request.FILES获取到的文件类型
    """
    names = _file_type(file)
    if names:
        file.name = ''.join(names)
        new_path = os.path.join(_file_path(), file.name) 
        # 开始上传
        with open(new_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return file.name
    else:
        print('上传失败')
        return False