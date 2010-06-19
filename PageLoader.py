
class PageListLoader:
    def __init__(self, panel):
        self.panel = panel

    def onCompletion(self, text):
        """ pages.txt is in the format:
               title:filename.html
               title2:filename2.html
        """
        res = []
        for l in text.split('\n'):
            if not l:
                continue
            l = l.split(':')
            if len(l) != 2:
                continue
            res.append([l[0].strip(), l[1].strip()])
        self.panel.loadPages(res)

    def onError(self, text, code):
        self.panel.onError(text, code)

    def onTimeout(self, text):
        self.panel.onTimeout(text)


class PageLoader:
    def __init__(self, panel, title):
        self.panel = panel
        self.title = title

    def onCompletion(self, text):
        self.panel.createPage(self.title, text)

    def onError(self, text, code):
        self.panel.onError(text, code)

    def onTimeout(self, text):
        self.panel.onTimeout(text)


