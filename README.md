# zeus
### 基于Django的项目管理系统


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