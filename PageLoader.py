def process_question(qtxt):
    question = ''
    skip = False
    for letter in qtxt:
        if letter == '<':
            skip = True
        if letter == '>':
            skip = False
        if skip:
            continue
        if letter.isalnum() or letter == ' ':
            if letter == ' ':
                letter = '_'
            question += letter.lower()
    return question

class PageListLoader:
    def __init__(self, panel, purpose):
        self.panel = panel
        self.purpose = purpose

    def onCompletion(self, text):
        """ pages.txt is in the format:
               title:filename.html
               title2:filename2.html
        """
        res = []
        for l in text.split('\n'):
            if not l:
                continue
            if self.purpose == 'contents':
                l = l.split(':')
                if len(l) != 2:
                    continue
                res.append([l[0].strip(), l[1].strip()])
            elif self.purpose == 'faq':
                fname = process_question(l)
                #print fname, l
                res.append([l, "faq/answers/%s.html" % fname])
        self.panel.loadPages(res, self.purpose)

    def onError(self, text, code):
        self.panel.onError(text, code)

    def onTimeout(self, text):
        self.panel.onTimeout(text)


class PageLoader:
    def __init__(self, panel, title, purpose):
        self.panel = panel
        self.title = title
        self.purpose = purpose

    def onCompletion(self, text):
        self.panel.createPage(self.title, self.purpose, text)

    def onError(self, text, code):
        self.panel.onError(text, code)

    def onTimeout(self, text):
        self.panel.onTimeout(text)


