import json
def message():
    message = '''[
  {
    "comment": "消息",
    "name": "下拉可刷新，课表可滑动和修改",
    "title": "下拉可刷新，课表可滑动和修改"
  },
  {
    "comment": "通知",
    "name": "感谢你的支持",
    "title": "感谢你的支持"
  },
  {
    "comment": "通知",
    "name": "有问题请寻找我们",
    "title": "有问题请寻找我们"
  },
  {
    "comment": "通知",
    "name": "欢迎来到WE广油",
    "title": "欢迎来到WE广油"
  }
]'''

    temp = json.loads(message)
    message = json.dumps(temp)
    return message
