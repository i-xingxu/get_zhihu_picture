# coding=utf-8

import requests
import os
import re
import time

# path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/zhihu'
path = './' + 'zhihu/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
cookies = '''d_c0="ALDldXJO6g2PTkoUSO-jby8V_CPFxw1QTSo=|1531842337"; _zap=efb1d97e-d5d5-4f1f-bc57-dc82682af428; __gads=ID=3f93efa8af05a528:T=1543149809:S=ALNI_MYzkolb9-rpnLS8nZh4Trr_Dg3TNg; _xsrf=66aOP9ytDxy6zw8toPuOqJfTMYLjsGhn; __utmv=51854390.100-1|2=registration_date=20131024=1^3=entry_date=20131024=1; capsion_ticket="2|1:0|10:1572709781|14:capsion_ticket|44:MDQ5ZGE3YTRjYTdkNDljNThmMWFhYmY3ZjU5Y2E3MjU=|a84348a79cccd15f13225f224545a49aeaceb29a7e296dbe7cfed16f509d64dc"; z_c0="2|1:0|10:1572709784|4:z_c0|92:Mi4xM29ZZEFBQUFBQUFBc09WMWNrN3FEU1lBQUFCZ0FsVk5tUE9xWGdCY09CZkxzYnI0MldsYzRVOXNwZ1ZqY3hpSy13|252cc8de540f4cd549a5e00ecff410c942499a7ec3b816cb3f829467dd4f91dd"; tst=r; q_c1=736c2ddcd3e44a04befa51b0c23aca3b|1572710299000|1531842338000; __utma=51854390.42059747.1563464090.1563464090.1574949014.2; __utmc=51854390; __utmz=51854390.1574949014.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/324766011/answer/852075615; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1574814106,1574950212,1575127213,1575177890; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1575186759; tgw_l7_route=4860b599c6644634a0abcd4d10d37251'''


# url='https://www.zhihu.com/api/v4/questions/26037846/answers'

# res=requests.get(url,headers=headers)
#
# print(res.json())
# jpgList = []


def get_url_res(url, parm):
    res = requests.get(url, headers=headers, params=parm)

    return res


def get_picture_url(res):
    jpgList = []
    if res.status_code == 200:
        text = str(res.json())
        pattern = re.compile('src="(.*?)".*?class="origin_image', re.S)
        items = re.findall(pattern, text)
        # print(res.json())
        for item in items:
            if re.match(r'^https?:/{2}\w.+$', item):
                jpgList.append(item)
        save_jpg(jpgList)
        return jpgList
    else:
        return False


def save_jpg(jpgList):

    for url in jpgList:
        time.sleep(0.8)
        print(url)
        try:
            html = requests.get(url, headers=headers)
            with open(path + url.split('/')[-1], 'wb') as file:
                file.write(html.content)
                file.flush()
            file.close()
        except:
            print(url + '失败')


def main(url):
    res = get_url_res(url, parm)
    get_picture_url(res)


if __name__ == '__main__':
    # jpgLists = []

    if os.path.exists('./zhihu'):
        pass
    else:
        os.mkdir('./zhihu')

    url = 'https://www.zhihu.com/api/v4/questions/319371540/answers'
    for i in range(5, 200, 5):
        parm = {
            'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
            'limit': 5,
            'offset': i,
            'platform': 'desktop',
            'sort_by': 'default'
        }
        main(url)

    # print(jpgList)
