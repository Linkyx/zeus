# zeus
### 基于Django的项目管理系统
#### 用于xiyoulinux兴趣小组内部使用（调用了内部的auth授权，如果个人使用的话， 需要自己维护user）

* 请自行配制settings

```python
INSTALLED_APPS = (
    ''''''
    'djcelery',
    'kombu.transport.django',
    'zeus',
    ''''''
)
```
```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zeus',
        'USER': 'root',
        'PASSWORD': '****',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
* 运行项目之前请在项目统计目录下创建log文件夹，并创建all.log, info.log,error.log, script.log文件
 