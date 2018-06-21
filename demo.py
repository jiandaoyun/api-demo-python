import requests
import json
import time

class APIUtils:

    WEBSITE = "https://www.jiandaoyun.com"
    RETRY_IF_LIMITED = True

    # 构造函数
    def __init__(self, appId, entryId, api_key):
        self.url_get_widgets = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/widgets'
        self.url_get_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data'
        self.url_retrieve_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_retrieve'
        self.url_update_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_update'
        self.url_create_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_create'
        self.url_delete_data = APIUtils.WEBSITE + '/api/v1/app/' + appId + '/entry/' + entryId + '/data_delete'
        self.api_key = api_key

    # 带有认证信息的请求头
    def get_req_header(self):
        return {
            'Authorization': 'Bearer ' + self.api_key,
            'Content-Type': 'application/json;charset=utf-8'
        }

    # 发送http请求
    def send_request(self, method, request_url, data):
        headers = self.get_req_header()
        if method == 'GET':
            res = requests.get(request_url, params=data, headers=headers, verify=False)
        if method == 'POST':
            res = requests.post(request_url, data=json.dumps(data), headers=headers, verify=False)
        result = res.json()
        if res.status_code >= 400:
            if result['code'] == 8303 and APIUtils.RETRY_IF_LIMITED:
                # 5s后重试
                time.sleep(5)
                return self.send_request(method, request_url, data)
            else:
                raise Exception('请求错误！', result)
        else:
            return result

    # 获取表单字段
    def get_form_widgets(self):
        result = self.send_request('POST', self.url_get_widgets, {})
        return result['widgets']

    # 根据条件获取表单中的数据
    def get_form_data(self, dataId, limit, fields, data_filter):
        result = self.send_request('POST', self.url_get_data, {
            'data_id': dataId,
            'limit': limit,
            'fields': fields,
            'filter': data_filter
        })
        return result['data']

    # 获取表单中满足条件的所有数据
    def get_all_data(self, fields, data_filter):
        form_data = []

        # 递归取下一页数据
        def get_next_page(dataId):
            data = self.get_form_data(dataId, 100, fields, data_filter)
            if data:
                for v in data:
                    form_data.append(v)
                dataId = data[len(data) - 1]['_id']
                get_next_page(dataId)
        get_next_page('')
        return form_data

    # 检索一条数据
    def retrieve_data(self, dataId):
        result = self.send_request('POST', self.url_retrieve_data, {
            'data_id': dataId
        })
        return result['data']

    # 创建一条数据
    def create_data(self, data):
        result = self.send_request('POST', self.url_create_data, data)
        return result['data']

    # 更新数据
    def update_data(self, dataId, data):
        result = self.send_request('POST', self.url_update_data, {
            'data_id': dataId,
            'data': data
        })
        return result['data']

    # 删除数据
    def delete_data(self, dataId):
        result = self.send_request('POST', self.url_delete_data, {
            'data_id': dataId
        })
        return result


if __name__ == '__main__':
    appId = '5b1747e93b708d0a80667400'
    entryId = '5b1749ae3b708d0a80667408'
    api_key = 'CTRP5jibfk7qnnsGLCCcmgnBG6axdHiX'
    api = APIUtils(appId, entryId, api_key)
    # 获取表单字段
    widgets = api.get_form_widgets()
    print('获取表单字段：')
    print(widgets)

    # 按条件获取表单数据
    data = api.get_form_data('', 100, ['_widget_1528252846720', '_widget_1528252846801'], {
        'rel': 'and',
        'cond': [{
            'field': '_widget_1528252846720',
            'type': 'text',
            'method': 'empty'
        }]
    })
    print('按条件获取表单数据：')
    for v in data:
        print(v)

    # 获取所有表单数据
    form_data = api.get_all_data([], {})
    print('所有表单数据：')
    for v in form_data:
        print(v)

    # 创建单条数据
    data = {
        # 单行文本
        '_widget_1528252846720': {
            'value': '123'
        },
        # 子表单
        '_widget_1528252846801': {
            'value': [{
                '_widget_1528252846952': {
                    'value': '123'
                }
            }]
        },
        # 数字
        '_widget_1528252847027': {
            'value': 123
        },
        # 地址
        '_widget_1528252846785': {
            'value': {
                'province': '江苏省',
                'city': '无锡市',
                'district': '南长区',
                'detail': '清名桥街道'
            }
        },
        # 多行文本
        '_widget_1528252846748': {
            'value': '123123'
        }
    }
    create_data = api.create_data(data)
    print('创建单条数据：')
    print(create_data)

    # 更新单条数据
    update = {
        # 单行文本
        '_widget_1528252846720': {
            'value': '12345'
        },
        # 子表单
        '_widget_1528252846801': {
            'value': [{
                '_widget_1528252846952': {
                    'value': '12345'
                }
            }]
        },
        # 数字
        '_widget_1528252847027': {
            'value': 12345
        },
        # 地址
        '_widget_1528252846785': {
            'value': {
                'province': '江苏省',
                'city': '无锡市',
                'district': '南长区',
                'detail': '清名桥街道'
            }
        },
        # 多行文本
        '_widget_1528252846748': {
            'value': '123123'
        }
    }
    result = api.update_data(create_data['_id'], update)
    print('更新单条数据：')
    print(result)

    # 查询单条数据
    retrieve_data = api.retrieve_data(create_data['_id'])
    print('查询单条数据：')
    print(retrieve_data)

    # 删除单条数据
    result = api.delete_data(create_data['_id'])
    print('删除单条数据：')
    print(result)
