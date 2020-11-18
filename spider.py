from pyquery import PyQuery as pq
import requests
from jieba import lcut
from wordcloud import WordCloud
from imageio import imread

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/86.0.4240.183 Safari/537.36'}


def main():
    start = 'https://movie.douban.com/subject/26303622/comments?start='
    end = '&limit=20'

    comment = ''
    for i in range(0, 20, 1):
        url = start + str(i * 20) + end
        comment = comment + get_movie(url)
    with open('all_comment.txt', 'w', encoding='utf-8') as f:
        f.write(comment)
        f.close()

    cut_comment = lcut(comment)
    cut_comment = ' '.join(cut_comment)
    mk = imread('belle.png')
    stopwords= {'电影', '一个', '几个', '这么', '这种', '一些', '觉得', '什么', '最后', '虽然', '这些', '以为', '各种', '一种',
                '还是', '就是', '一部', '这样', '这部', '我们', '真是', '知道', '自己', '可能', '也是', '这个', '那么', '没有',
                '一起', '甚至', '片中', '只有', '但是', '以及', '他们', '因为', '已经', '不是', '可以', '东西', '今年', '那个',
                '那些', '怎么', '作为', '很多', '本身', '不过', '居然', '非常', '只是', '那些', '看到', '实在'}

    wc = WordCloud(background_color='white', font_path='SIMLI.TTF', scale=10, mask=mk, stopwords=stopwords)

    wc.generate(cut_comment)
    wc.to_file('comment.png')


def get_movie(url):
    resp = requests.get(url, headers=headers)
    doc = pq(resp.text)
    items = doc('#comments > div.comment-item').items()
    all_comment = ''
    for item in items:
        comment = item.find('div.comment > p > span').text()
        all_comment = all_comment + comment
    return all_comment


if __name__ == '__main__':
    main()
