import base64
import requests,io
from alibabacloud_imagesearch20200212.client import Client
from alibabacloud_imagesearch20200212.models import AddImageAdvanceRequest,DeleteImageRequest 
from alibabacloud_imagesearch20200212.models import SearchImageByPicAdvanceRequest,SearchImageByNameRequest
from alibabacloud_tea_rpc.models import Config
from alibabacloud_oss_util.models import RuntimeOptions
# from urllib.request import urlopen

REGION = 'cn-shanghai'
ACCESS_KEY = 'LTAI4Fz2nxCeTFxKVUcJtWDr'
ACCESS_SECRET = 'Aqre80rlxahMsyMnULkXPFnVK8nfz1'
INSTANCE_NAME = 'test1111'
END_POINT = 'imagesearch.%s.aliyuncs.com'%REGION

class ImageInfo(object):
    def __init__(self, item_id, cat_id, url, item_name, price, str_attr=None):
        self.item_id = int(item_id)
        self.item_name = item_name 
        self.pic_content = self.get_img_base64(url)
        self.cat_id = cat_id
        # print(self.cat_id)
        self.str_attr = str(cat_id)
        self.int_attr = int(price)
        self.crop = True

    def get_img_base64(self, url):
        # urlopen(url).read()
        # return base64.b64encode(requests.get(url).content)
        return io.BytesIO(requests.get(url).content)

class ImageOption(object):
    def __init__(self):
        config = Config()
        config.access_key_id = ACCESS_KEY
        config.access_key_secret = ACCESS_SECRET
        config.endpoint = END_POINT
        config.region_id = REGION
        config.type = 'access_key'
        self.client = Client(config)

    # 添加图片
    def add_image(self, image: ImageInfo):

        request = AddImageAdvanceRequest()
        request.instance_name = INSTANCE_NAME
        request.product_id = image.item_id
        request.pic_name = image.item_name
        request.category_id = image.cat_id
        request.crop = image.crop
        request.int_attr = image.int_attr
        request.str_attr = image.str_attr
        # f = open('<filePath>', 'rb')
        request.pic_content_object = image.pic_content
        runtime_option = RuntimeOptions()
        response = self.client.add_image_advance(request, runtime_option)
        print(response.to_map())
        return response

    # 按照商品库里的图片搜索
    def search_by_name(self, image: ImageInfo, start, num, my_filter=None):
        
        request = SearchImageByNameRequest()
        request.instance_name = INSTANCE_NAME
        request.product_id = image.item_id
        request.pic_name = image.item_name
        request.start = start
        request.num = num
        request.filter = my_filter
        runtime_option = RuntimeOptions()
        response = self.client.search_image_by_name(request, runtime_option)
        print(response.to_map())
        return response.to_map()

    # 过滤条件。int_attr支持的操作符有>、>=、<、<=、=。str_attr支持的操作符有=和!=，
    # 多个条件之支持AND和OR进行连接。例如：int_attr>=100、str_attr!=”value1”、int_attr=1000 AND str_attr=”value1”。
    # 新上传图片搜索
    def search_by_Pic(self, image:ImageInfo, start, num, my_filter=None):
        request = SearchImageByPicAdvanceRequest()
        request.instance_name = INSTANCE_NAME
        request.pic_content_object = image.pic_content
        request.num = num
        request.start = start
        request.filter = my_filter
        runtime_option = RuntimeOptions(read_timeout=50000, connect_timeout=50000)
        response = self.client.search_image_by_pic_advance(request, runtime_option)
        # print(response.to_map())
        return response.to_map()
       
    def delete(self, item_id, item_name):
        # 删除图片

        request = DeleteImageRequest()
        request.instance_name = INSTANCE_NAME
        request.product_id = item_id
        request.pic_name = item_name
    
        runtime_option = RuntimeOptions()
        response = self.client.delete_image(request, runtime_option)
        print(response.to_map())

    
