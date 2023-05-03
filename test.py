import requests
from bs4 import BeautifulSoup

# Define the URL of your game's Steam page
url = 'https://store.steampowered.com/app/1948280/Reviews/'

# Send a GET request to the URL and retrieve the HTML content
response = requests.get(url)
content = response.content

# Create a BeautifulSoup object from the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Find all the review containers on the page
reviews = soup.find_all('div', {'class': 'apphub_UserReviewCardContent'})

# Loop through each review container and extract the review text
for review in reviews:
    text = review.find('div', {'class': 'apphub_CardTextContent'}).text.strip()
    print(text)


    def post_process():
        # with Python中的上下文管理器，会帮我们释放资源，比如 关闭文件句柄
        # open 函数为Python内建的文件读取函数，r代表只读
        with open(AppID + '-summary.json', 'r', encoding='utf8') as f:
            # 解析一个有效的JSON字符串并将其转换为Python字典
            data = json.loads(f.read())
        # 使用 ，连接列表中的值
        # data[0]是一个字典类型，一个星号代表展开键，两个星号（**）代表展开字典的值
        output = ','.join([*data[0]])
        # 遍历 字典列表data
        for obj in data:
            # 将结果转化为字符串，累加到output中
            # f 为f-string格式化，将大括号中的表达式替代
            output += f'\n{obj["num_reviews"]},{obj["review_score"]},{obj["review_score_desc"]},{obj["total_positive"]},{obj["total_negative"]},{obj["total_reviews"]}'
        # 将结果写到到output.csv中
        with open(AppID + '-summary_post.csv', 'w', encoding='utf8') as f:
            f.write(output)

        for tag in page.find_all('div', class_='list_left'):
            sub_tag = tag.find('ul', class_="disease_basic")
            my_span = sub_tag.findAll('span')
            # my_span is a list
            is_yibao = my_span[1].text  # 是否医保
            othername = my_span[3].text  # 别名
            fbbw = my_span[5].text  # 发病部位
            is_infect = my_span[7].text  # 传染性
            dfrq = my_span[9].text  # 多发人群
            my_a = sub_tag.findAll('a')
            xgzz = my_a[2].text + ' ' + my_a[3].text + ' ' + my_a[4].text  # 相关症状
            # ps: .contents[0] or .get_text() is also accepted











            # 登录时需要POST的数据

            data = {'Login.Token1': '账号',

                    'Login.Token2': '密码',

                    'goto:http': '//x/loginSuccess.portal',

                    'gotoOnFail:http': '//x/loginFailure.portal'}

            # 设置请求头

            headers = {
                'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

            # 登录时表单提交到的地址（用开发者工具可以看到）

            login_url = 'http://x/userPasswordValidate.portal'

            # 构造Session

            session = requests.Session()

            # 在session中发送登录请求，此后这个session里就存储了cookie

            # 可以用print(session.cookies.get_dict())查看

            resp = session.post(login_url, data)

            # 登录后才能访问的网页

            url = '/cmstar/index.portal'

            # 发送访问请求

            resp = session.get(url)

            print(resp.content.decode('utf-8'))
