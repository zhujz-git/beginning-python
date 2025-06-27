from asyncore import write
from xml.sax.handler import ContentHandler
from xml.sax import parse


class PageMaker(ContentHandler):
    passthrough = False

    def startElement(self, name, attrs):
        if name == 'page':
            self.passthrough = True
            self.out = open(attrs['name'] + '.html', 'w')
            self.out.write('<html><head>\n')
            self.out.write('<title>{}</title>\n'.format(attrs['title']))
            self.out.write('</head><body>\n')
        elif self.passthrough:
            self.out.write('<' + name)
            for key, val in attrs.items():
                self.out.write('{}="{}"'.format(key, val))
            self.out.write('>')
        return super().startElement(name, attrs)

    def endElement(self, name):
        if name == 'page':
            self.passthrough = False
            self.out.write('\n</body></html>\n')
            self.out.close()
        elif self.passthrough:
            self.out.write('</{}>'.format(name))
        return super().endElement(name)

    def characters(self, content):
        if self.passthrough: self.out.write(content)
        return super().characters(content)

parse('website.xml', PageMaker())