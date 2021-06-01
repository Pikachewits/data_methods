import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class ProductparserPipeline:
    def process_item(self, item, spider):
        print()
        return item


class ImagesLoader(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item