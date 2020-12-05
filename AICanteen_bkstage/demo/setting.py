DEGUG=True

#配置连接数据库信息
#charset=utf-8报错  AttributeError: 'NoneType' object has no attribute 'encoding'
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3306/casher?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3305/casher2?charset=utf8'


SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

#配置DROPZONE信息
DROPZONE_DEFAULT_MESSAGE = '点击上传或者拖拽上传'
DROPZONE_ALLOWED_FILE_TYPE = 'image'
