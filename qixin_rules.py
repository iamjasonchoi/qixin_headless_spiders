# encoding=UTF-8
LOGIN_XPATH = {
    'username': '//input[@class="form-control input-lg input-flat input-flat-user"]',
    'password': '//input[@class="form-control input-lg input-flat input-flat-lock"]'
}


LIST_XPATH = {
    'list': "//div[contains(@class, 'company-item')]",
    'title': ".//div[@class='company-title']/a/text()",
    'legal_owner': ".//div[@class='legal-person'][1]/text()",
    'status': ".//div[@class='company-tags']/span[1]/text()",
    'capital': ".//div[contains(@class, 'col-3-1')]/text()",
    'date': ".//div[contains(@class, 'col-3-2')]/text()",
    'url': ".//div[@class='company-title']/a/@href"
}


CATEGORY_XPATH = {
    'info': '//div[@class="grid-item"]',
    'l1': './div/text()',
    'l2': './a/text()'
}
