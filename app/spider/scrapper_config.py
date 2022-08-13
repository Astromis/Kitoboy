vk_xpath_headless = {
    "wall": "//div[@id='page_wall_posts']",
    "text": '.', # data-testid
    "is_reposted": ".",
    "nickname" : ".",
    "user_tag": ".",
    "is_exists": ".",
    "username_input" : "//input[@class='VkIdForm__input']",
    "password_input" : "//input[@class='vkc__TextField__input'][@type='password']",
    "otp_input": "//input[@class='vkc__TextField__input'][@name='otp']",
    "login_next_button" : '.',
    "user_tag_on_rel_pages" : '.'
}

twitter_xpath_head = {
    "head": "css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l",
    "tweets": "css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg",
    "text": "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0",
    "is_reposted":"css-901oao css-16my406 css-cens5h r-1bwzh9t r-poiln3 r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0",
    "nickname" : "css-901oao r-1awozwy r-1nao33i r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0",
    "user_tag": "css-901oao css-1hf3ou5 r-1bwzh9t r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0",
    "is_exists": "css-901oao r-1fmj7o5 r-37j5jr r-1yjpyg1 r-1vr29t4 r-ueyrd6 r-5oul0u r-bcqeeo r-fdjqy7 r-qvutc0",
    "username_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "password_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "login_next_button" : '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]',
    "user_tag_on_rel_pages" : '//div[@class="css-901oao css-cens5h r-1bwzh9t r-37j5jr r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0"]/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]'
}


twitter_xpath_headless = {
    "header": "//div[@class='css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l']",
    "wall": "//article[@class='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg']",
    "text": ".//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']", # data-testid
    "is_reposted": ".//span[@class='css-901oao css-16my406 css-cens5h r-1bwzh9t r-poiln3 r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0']",
    "nickname" : ".//div[@class='css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0']",
    "user_tag": ".//div[@class='css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']",
    "is_exists": "//div[@class='css-901oao r-18jsvk2 r-37j5jr r-1yjpyg1 r-1vr29t4 r-ueyrd6 r-5oul0u r-bcqeeo r-fdjqy7 r-qvutc0']",
    "username_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "password_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "login_next_button" : '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]',
    "user_tag_on_rel_pages" : '//div[@class="css-901oao css-cens5h r-1bwzh9t r-37j5jr r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0"]/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]'
}