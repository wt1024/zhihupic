import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import shutil
import os,errno
from scrapy.utils.project import get_project_settings
class MyImagesPipeline(ImagesPipeline):

    img_store = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        print(item['image_paths'])
        real_path="%s/%s" % (self.img_store, item['question_answer_id'])
        if os.path.exists(real_path) == False:
            #os.mkdirs(real_path)
            os.makedirs(real_path)
        
        print(self.img_store +"---"+ real_path[0])
        print(real_path + "/----" + item["question_answer_id"] + '.jpg')
        urls_unique = list(set(item["image_paths"]))
        for image_path in urls_unique:
            print(image_path)
            shutil.move(self.img_store + image_path, real_path + "/" + image_path[5:][:-4] + '.jpg')
        print("***********debug")
        return item
    def file_path(self, request, response=None, info=None):
        open("image_urls.txt","a").write(request.url + "\n")
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

