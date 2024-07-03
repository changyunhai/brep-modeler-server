'''

manager 用于处理documentId， userID， socketID之间的对应关系以及
user可以处理那些document

详细可以见
readme.md 文件

todo
'''

from cache import Cache, gCache


class Manager:
    """
    manager for the application, include context and helps
    """

    def __init__(self):
        self.contexts: Cache = gCache
        """stores the documentid-context"""
        self.helps: dict = {}
        """stores the help info and details. key=cmd str, value=[description_str,[details_str1,detail_str2...]]"""

    def help(self, description: str, detail):
        '''
        an annotation to give helps to user for this command
        :param description: a description string
        :param detail: str[] or lambda expression (mgr:Manager)->str[]
        :return:
        '''
        if (callable(detail)):
            detail = detail(self)

        def _saveHelp(func):
            self.helps[func.__name__] = [description, detail]
            return func

        return _saveHelp
