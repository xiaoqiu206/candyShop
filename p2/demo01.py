# coding=utf-8
'''
Created on 2015年8月4日

@author: Administrator
'''
from bs4 import BeautifulSoup

html = """
<cite class="CitationContent" id="CR1">
          Anderson, C. (2008). The end of theory: The data deluge makes the scientific method obsolete. 
          <em class="EmphasisTypeItalic">Wired,</em>
          <em class="EmphasisTypeItalic">16</em>, 07.
   </cite>
"""

soup = BeautifulSoup(html)
print soup.find('cite').get_text()
