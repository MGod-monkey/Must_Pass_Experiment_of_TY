# # from django.shortcuts import render

# # # Create your views here.
# # from django.http import HttpResponse

# # def home(request):
# #     return HttpResponse('Hello, world!')

# from django.http import HttpResponse
# from django.shortcuts import render
# import pysolr
# import openpyxl

# # 数据集名称
# collection_name = 'tiku'
# tixing_str = ["单选题", "多选题", "判断题"]
# tiku_num = 270
# solr = pysolr.Solr(f'http://localhost:8983/solr/{collection_name}', always_commit=True)

# def search(request):
#     # 获取用户提交的搜索关键词
#     keyword = request.GET.get('inputs', '')
#     # 搜索并返回结果
#     results = []
#     # 定义查询语句，进行题目模糊搜索
#     query = f'(Question:"*{keyword}*" OR OptionA:"*{keyword}*" OR OptionB:"*{keyword}*" OR OptionC:"*{keyword}*" OR OptionD:"*{keyword}*")'
#     # 查询solr
#     try:
#         response = solr.search(query, fl=['QNumber', 'AnswerType', 'Question', 'Answer', 'OptionA', 'OptionB', 'OptionC', 'OptionD'], rows=10)
#         for hit in response:
#                     if len(hit) > 6:
#                         result = {
#                             'QNumber': hit['QNumber'][0],
#                             'AnswerType': tixing_str[int(hit['AnswerType'][0])],
#                             'Question': hit['Question'][0],
#                             'Answer': hit['Answer'][0],
#                             'OptionA': hit['OptionA'][0],
#                             'OptionB': hit['OptionB'][0],
#                             'OptionC': hit['OptionC'][0],
#                             'OptionD': hit['OptionD'][0],
#                         }
#                     else:
#                         result = {
#                         'QNumber': hit['QNumber'][0],
#                         'AnswerType': tixing_str[int(hit['AnswerType'][0])],
#                         'Question': hit['Question'][0],
#                         'Answer': hit['Answer'][0],
#                         'OptionA': hit['OptionA'][0],
#                         'OptionB': hit['OptionB'][0],
#                         }
#                     if result not in results:
#                         results.append(result)
#             # 渲染模板并返回结果
#         return render(request, 'search.html', {'keyword': keyword, 'results': results})
#     except Exception as e:
#         return render(request, 'search.html', {'keyword': keyword, 'results': ""})
    

# def handler404(request, exception):
#     return render(request, '404.html', status=404)
from django.http import HttpResponse
from django.shortcuts import render
import pysolr
import openpyxl

# 数据集名称
collection_name = 'tiku'
tixing_str = ["单选题", "多选题", "判断题"]
tiku_num = 270
solr = pysolr.Solr(f'http://localhost:8983/solr/{collection_name}', always_commit=True)

def search(request):
    # 获取用户提交的搜索关键词
    keyword = request.GET.get('inputs', '')
    
    # 如果关键词是实验报告，返回图片
    if "实验" in keyword and "报告" in keyword:
        images = [
            'https://mybog.s3.bitiful.net/imgs/reward_alipay.png',  # 示例图片文件名，可以替换为你的实际图片文件名
            'https://mybog.s3.bitiful.net/imgs/reward_wechat.png',
            'https://mybog.s3.bitiful.net/imgs/JaEtOo8VKfpsh5M.jpg',
        ]
        return render(request, 'search.html', {'keyword': keyword, 'images': images})

    # 搜索并返回结果
    results = []
    # 定义查询语句，进行题目模糊搜索
    query = f'(Question:"*{keyword}*" OR OptionA:"*{keyword}*" OR OptionB:"*{keyword}*" OR OptionC:"*{keyword}*" OR OptionD:"*{keyword}*")'
    # 查询solr
    try:
        response = solr.search(query, fl=['QNumber', 'AnswerType', 'Question', 'Answer', 'OptionA', 'OptionB', 'OptionC', 'OptionD'], rows=10)
        for hit in response:
                    if len(hit) > 6:
                        result = {
                            'QNumber': hit['QNumber'][0],
                            'AnswerType': tixing_str[int(hit['AnswerType'][0])],
                            'Question': hit['Question'][0],
                            'Answer': hit['Answer'][0],
                            'OptionA': hit['OptionA'][0],
                            'OptionB': hit['OptionB'][0],
                            'OptionC': hit['OptionC'][0],
                            'OptionD': hit['OptionD'][0],
                        }
                    else:
                        result = {
                        'QNumber': hit['QNumber'][0],
                        'AnswerType': tixing_str[int(hit['AnswerType'][0])],
                        'Question': hit['Question'][0],
                        'Answer': hit['Answer'][0],
                        'OptionA': hit['OptionA'][0],
                        'OptionB': hit['OptionB'][0],
                        }
                    if result not in results:
                        results.append(result)
        # 渲染模板并返回结果
        return render(request, 'search.html', {'keyword': keyword, 'results': results})
    except Exception as e:
        return render(request, 'search.html', {'keyword': keyword, 'error': str(e)})

def handler404(request, exception):
    return render(request, '404.html', status=404)
