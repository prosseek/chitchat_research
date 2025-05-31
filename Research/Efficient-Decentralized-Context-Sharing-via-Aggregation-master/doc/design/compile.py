# -*- coding: utf-8 -*-
from glob import glob
from os import path, makedirs
from codecs import open
from shutil import copytree, rmtree

import markdown
from jinja2 import Template

MENU = [
    {'file': 'groupContext', 'icon': 'icon-shopping-cart', 'name': u'GroupContext'},
    {'file': 'things_to_know', 'icon': 'icon-shopping-cart', 'name': u'Things to know'},
]

template = Template(open('template.html', encoding='utf-8').read())
# md = markdown.Markdown()

def compile_page(source, dest):
    s = open(source, encoding='utf-8') 
    d = open(dest, 'w', encoding='utf-8')
    compiled = markdown.markdown(s.read(), ['footnotes', 'tables'])
    d.write(template.render(MENU=MENU, content=compiled))
    print 'generated', dest

def main():

    if path.exists('output'): 
        rmtree('output')
    makedirs('output')

    for source in glob('pages/*.md'): 
        page_name = '.'.join(path.basename(source).split('.')[:-1])
        dest = path.join('output', page_name + '.html')
        compile_page(source, dest)

    copytree('static', 'output/static')

if __name__ == '__main__':
    main()
