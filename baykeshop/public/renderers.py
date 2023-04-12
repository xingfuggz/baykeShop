from rest_framework import renderers


class TemplateHTMLRenderer(renderers.TemplateHTMLRenderer):
    """ 修复为list时渲染html错误 """
    def get_template_context(self, data, renderer_context):
        context = super().get_template_context(data, renderer_context)
        if isinstance(context, list):
            context = {'datas': context}
        return context