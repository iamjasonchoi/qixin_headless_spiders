# encoding=UTF-8
import xmltodict
from lxml import etree


XSLT = etree.XML(open('rules.xslt').read())
TRANSFORMER = etree.XSLT(XSLT)


def parse_list(html):
    dom = etree.HTML(html)
    xml = TRANSFORMER(dom)
    return xmltodict.parse(xml)['list']['item']
