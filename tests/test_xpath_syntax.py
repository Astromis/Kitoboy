from app.spider.scrapper_config import * 
import pytest
from lxml.etree import XPath, XPathSyntaxError

class TestXpathSyntax:

    def test_vk_headless(self):
        try:
            for key, xpath in vk_xpath_headless.items():
                XPath(xpath)
        except XPathSyntaxError:
            pytest.fail(f"Unexpected XPath syntax for {key}")
    
    def test_twitter_headless(self):
        try:
            for key, xpath in twitter_xpath_headless.items():
                XPath(xpath)
        except XPathSyntaxError:
            pytest.fail(f"Unexpected XPath syntax for {key}")
            
    
    def test_twitter_head(self):
        try:
            for key, xpath in twitter_xpath_head.items():
                XPath(xpath)
        except XPathSyntaxError:
            pytest.fail(f"Unexpected XPath syntax for {key}")    
