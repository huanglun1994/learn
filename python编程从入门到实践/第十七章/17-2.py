# -*- coding: utf-8 -*-
"""xxxxx"""
__author__ = 'Huang Lun'
import requests
import pygal
from operator import itemgetter
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# 执行API调用并存储响应
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)

# 处理有关每篇文章的信息
submission_ids = r.json()
submission_dicts, names = [], []
for submission_id in submission_ids[:30]:
    # 对于每篇文章，都执行一个API调用
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_id) + '.json')
    submission_r = requests.get(url)
    response_dict = submission_r.json()

    names.append(response_dict['title'])
    submission_dict = {
        'value': response_dict.get('descendants', 0),
        'label': response_dict['title'],
        'xlink': 'http://news.ycombinator.com/item?id=' + str(submission_id)
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('value'), reverse=True)

# 可视化
my_style = LS('#333366', base_style=LCS)

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 16
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Active Discussion on Hacker News'
chart.x_labels = names

chart.add('', submission_dicts)
chart.render_to_file('active_discussion.svg')
