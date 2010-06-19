import pyjd # dummy in pyjs

from pyjamas.ui.TabBar import TabBar
from pyjamas.ui.TabPanel import TabPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Image import Image
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Composite import Composite
#from pyjamas.ui import DecoratorPanel
from pyjamas.ui import MouseListener
from pyjamas.ui import Event
from pyjamas import Window
from pyjamas.ui.DecoratorPanel import DecoratedTabPanel, DecoratorPanel
from pyjamas.ui.DecoratorPanel import DecoratorTitledPanel
from pyjamas.HTTPRequest import HTTPRequest
from PageLoader import PageListLoader, PageLoader


#class PrettyTab(DecoratorPanel):
class PrettyTab(Composite):

    def __init__(self, text, imageUrl):

        DecoratorPanel.__init__(self, DecoratorPanel.DECORATE_ALL)

        p = HorizontalPanel()
        p.setSpacing(3)
        self.img = Image(imageUrl)
        self.txt = HTML(text)
        p.add(self.img)
        p.add(self.txt)

        self.add(p)

    def addClickListener(self, listener):

        self.img.addClickListener(listener)
        self.txt.addClickListener(listener)

class Tabs:

    def onModuleLoad(self):

        dock = DockPanel()
        self.header = HTML(Width="100%")
        self.footer = HTML(Width="100%")
        self.sidebar = HTML(Width="200px", Height="100%", StyleName="sidebar")
        self.fTabs = DecoratedTabPanel(Size=("100%", "100%"),
                                       StyleName="tabs")

        #dp = DecoratorTitledPanel("Tabs", "bluetitle", "bluetitleicon",
        #              ["bluetop", "bluetop2", "bluemiddle", "bluebottom"])
        #dp.add(self.fTabs)

        dock.add(self.header, DockPanel.NORTH)
        dock.add(self.footer, DockPanel.SOUTH)
        dock.add(self.sidebar, DockPanel.EAST)
        dock.add(self.fTabs, DockPanel.CENTER)
        dock.setCellVerticalAlignment(self.fTabs, HasAlignment.ALIGN_TOP)
        #dock.setCellHorizontalAlignment(self.fTabs, HasAlignment.ALIGN_CENTER)
        dock.setCellWidth(self.header, "100%")
        dock.setCellWidth(self.sidebar, "200px")

        RootPanel().add(dock)

        self.loadPageList()

    def createPage(self, title, text):

        if title == 'header':
            self.header.setHTML(text)
            return
        elif title == 'footer':
            self.footer.setHTML(text)
            return
        elif title == 'sidebar':
            self.sidebar.setHTML(text)
            return

        self.pages[title] = text
        if len(self.pages) != len(self.page_list):
            return
        for l in self.page_list:
            title = l[0]
            text = self.pages[title]
            self.fTabs.add(HTML(text), title, True)
        self.fTabs.selectTab(0)

    def createImage(self, imageUrl):
        image = Image(imageUrl)
        image.setStyleName("ks-images-Image")
        
        p = VerticalPanel()
        p.setHorizontalAlignment(HasAlignment.ALIGN_CENTER)
        p.setVerticalAlignment(HasAlignment.ALIGN_MIDDLE)
        p.add(image)

        return p

    def loadPageList(self):
        HTTPRequest().asyncGet("sidebar.html", PageLoader(self, "sidebar"))
        HTTPRequest().asyncGet("header.html", PageLoader(self, "header"))
        HTTPRequest().asyncGet("footer.html", PageLoader(self, "footer"))
        HTTPRequest().asyncGet("contents.txt", PageListLoader(self))

    def loadPages(self, pages):
        self.pages = {}
        self.page_list = pages
        for l in pages:
            title = l[0]
            desc = l[1]
            HTTPRequest().asyncGet(desc, PageLoader(self, title))


if __name__ == '__main__':
    pyjd.setup("./public/index.html")
    app = Tabs()
    app.onModuleLoad()
    pyjd.run()

