# Wagtail
Using Wagtail in an existing Django project

## Setup

```bash
poetry add wagtail
```

## Settings
In your `settings.py` file on the project, add the following:

Into the INSTALLED_APPS
```python
'wagtail.contrib.forms',
'wagtail.contrib.redirects',
'wagtail.embeds',
'wagtail.sites',
'wagtail.users',
'wagtail.snippets',
'wagtail.documents',
'wagtail.images',
'wagtail.search',
'wagtail',
'modelcluster',
'taggit',
'<OUR_APP_INTEGRATED_WITH_WAGTAIL>',
'wagtail.admin'  # This one should be the last
```

Into the MIDDLEWARE
```python
'wagtail.contrib.redirects.middleware.RedirectMiddleware'
```

Add a STATIC_ROOT setting, if your project does not have one already:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

Add MEDIA_ROOT and MEDIA_URL, if your project does not have these already:
```python
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

Add a WAGTAIL_SITE_NAME (this will be displayed on the main dashboard of the Wagtail admin backend):
```python
WAGTAIL_SITE_NAME = 'My Example Site'
```

## URL configuration
...