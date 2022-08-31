[Flow - Backend](0-index.md)
# Flow (Backend)

### Assuming you already have an project created, let's skip the create project and app steps.
#

# Models (Example)
#
````python
class Movie(models.Model):
    name = models.CharField(max_length=250)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=200)
    starring = models.CharField(max_length=350)
    
    def __str__(self):
        return self.name
````


##### Apply models to the DB
#
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```
##### Create Super User
#
```sh
python manage.py createsuperuser
```
# Authentication
[Source](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)

Authentication is the mechanism of associating an incoming request with a set of identifying credentials, such as the user the request came from, or the token that it was signed with. The permission and throttling policies can then use those credentials to determine if the request should be permitted.

#### How authentication is determined
The authentication schemes are always defined as a list of classes. REST framework will attempt to authenticate with each class in the list, and will set request.user and request.auth using the return value of the first class that successfully authenticates.

If no class authenticates, request.user will be set to an instance of django.contrib.auth.models.AnonymousUser, and request.auth will be set to None.

#### Setting the authentication scheme
The default authentication schemes may be set globally, using the DEFAULT_AUTHENTICATION_CLASSES setting. For example.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```
```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
```


# Permissions
[Source](https://www.django-rest-framework.org/api-guide/permissions/)

Together with authentication and throttling, permissions determine whether a request should be granted or denied access.

Permission checks are always run at the very start of the view, before any other code is allowed to proceed. Permission checks will typically use the authentication information in the request.user and request.auth properties to determine if the incoming request should be permitted.

Permissions are used to grant or deny access for different classes of users to different parts of the API.

The simplest style of permission would be to allow access to any authenticated user, and deny access to any unauthenticated user. This corresponds to the IsAuthenticated class in REST framework.
```python
class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
```
A slightly less strict style of permission would be to allow full access to authenticated users, but allow read-only access to unauthenticated users. This corresponds to the IsAuthenticatedOrReadOnly class in REST framework.
```python
class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )
```
#### How permissions are determined
Permissions in REST framework are always defined as a list of permission classes.

Before running the main body of the view each permission in the list is checked. If any permission check fails, an exceptions.PermissionDenied or exceptions.NotAuthenticated exception will be raised, and the main body of the view will not run.

When the permission checks fail, either a "403 Forbidden" or a "401 Unauthorized" response will be returned, according to the following rules:

-  The request was successfully authenticated, but permission was denied. — An HTTP 403 Forbidden response will be returned.
-  The request was not successfully authenticated, and the highest priority authentication class does not use WWW-Authenticate headers. — An HTTP 403 Forbidden response will be returned.
- The request was not successfully authenticated, and the highest priority authentication class does use WWW-Authenticate headers. — An HTTP 401 Unauthorized response, with an appropriate WWW-Authenticate header will be returned.

#### Custom Permissions (Example)
```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```
Then, in the views file:
```python
permission_classes = [IsOwnerOrReadOnly]
```

#### Custom Model Permissions 

To create custom permissions for a given model object, use the permissions model Meta attribute.

This example Task model creates two custom permissions, i.e., actions users can or cannot do with Task instances, specific to your application:

```python
class Task(models.Model):
    ...
    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]
```
The only thing this does is create those extra permissions when you run manage.py migrate (the function that creates permissions is connected to the post_migrate signal). Your code is in charge of checking the value of these permissions when a user is trying to access the functionality provided by the application (changing the status of tasks or closing tasks.) Continuing the above example, the following checks if a user may close tasks:
```python
user.has_perm('app.close_task')
```
# Logging
# [Source](https://docs.djangoproject.com/en/4.1/topics/logging/#logging)
Logging is an important part of every application life cycle. Having a good logging system becomes a key feature that helps developers, sysadmins, and support teams to understand and solve appearing problems.
The Python standard library and Django already comes with an integrated logging module that provides basic as well as advanced logging features. Log messages can give helpful information about various events happening behind the scenes.

A Python logging configuration consists of four parts:
- Loggers
- Handlers
- Filters
- Formatters

##### Loggers
A logger is the entry point into the logging system. Each logger is a named bucket to which messages can be written for processing.
A logger is configured to have a log level. This log level describes the severity of the messages that the logger will handle. Python defines the following log levels:

- DEBUG: Low level system information for debugging purposes
- INFO: General system information
- WARNING: Information describing a minor problem that has occurred.
- ERROR: Information describing a major problem that has occurred.
- CRITICAL: Information describing a critical problem that has occurred.


##### Handlers
The handler is the engine that determines what happens to each message in a logger. It describes a particular logging behavior, such as writing a message to the screen, to a file, or to a network socket.

##### Filters
A filter is used to provide additional control over which log records are passed from logger to handler.
By default, any log message that meets log level requirements will be handled. However, by installing a filter, you can place additional criteria on the logging process. For example, you could install a filter that only allows ERROR messages from a particular source to be emitted.

##### Formatters
Ultimately, a log record needs to be rendered as text. Formatters describe the exact format of that text. A formatter usually consists of a Python formatting string containing LogRecord attributes; however, you can also write custom formatters to implement specific formatting behavior.

##### Default logging definition 
Django’s default logging configuration inherits Python’s defaults. It’s available as django.utils.log.DEFAULT_LOGGING and defined in django/utils/log.py:
```python
{
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
```

##### Basic Custom Logging Configuration [Source](https://docs.djangoproject.com/en/4.1/topics/logging/#topic-logging-parts-loggers)
#
Logging configuration that allows to output warnings in the console:
```python
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
```
You don’t have to log to the console. Here’s a configuration which writes all logging from the django named logger to a local file:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/path/to/django/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```


### Different types of Logging
##### Basic add instance log
#
```python
import logging,traceback
logger = logging.getLogger('django')

def addSomeInstance(request):
    //View logic
    logger.warning('Added instance!')
```
##### Access logs
#
```python
import datetime
import logging
logger = logging.getLogger(__name__)

def home(request):
    logger.warning('Home page was accessed at '+str(datetime.datetime.now())+' hours')
```

## Audit logs
Audit logs is the process of keeping track of the activity within some piece of software. It logs the event, the time which it happened and the responsible.
There are several django libraries that offers this feature, one of those is the django-auditlog.
### django-auditlog [Source](https://django-auditlog.readthedocs.io/en/latest/usage.html)

Auditlog can automatically log changes to objects for you. This functionality is based on Django’s signals, but linking your models to Auditlog is even easier than using signals.
Registering your model for logging can be done with a single line of code, as the following example illustrates:
```python
from django.db import models

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

class MyModel(models.Model):
    sku = models.CharField(max_length=20)
    version = models.CharField(max_length=5)
    product = models.CharField(max_length=50, verbose_name='Product Name')
    history = AuditlogHistoryField()

auditlog.register(MyModel)
```


#
# Serializers
#
````python
from rest_framework import serializers
from backend_api.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
````
#
#### Serializer Validations - [Source](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
By default, all the model fields on the class will be mapped to a corresponding serializer fields.
Any relationships such as foreign keys on the model will be mapped to PrimaryKeyRelatedField. Reverse relationships are not included by default unless explicitly included as specified in the serializer relations documentation.

When deserializing data, you always need to call is_valid() before attempting to access the validated data, or save an object instance. If any validation errors occur, the .errors property will contain a dictionary representing the resulting error messages. For example:
```python
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}
```

##### Inspecting a ModelSerializer
Serializer classes generate helpful verbose representation strings, that allow you to fully inspect the state of their fields. This is particularly useful when working with ModelSerializers where you want to determine what set of fields and validators are being automatically created for you.

Allow blank and null: 
```python
name = CharField(allow_blank=True, max_length=100, required=False)
```

Regex validation:
```python 
class UserSerializer(serializers.ModelSerializer):
     first_name = serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True)
```
##### Field-level validation
Check that the blog post is about Django:
```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
```

Check number limits:
```python
def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Rating has to be between 1 and 10.')
        return value
```

##### Object-level validation
To do any other validation that requires access to multiple fields, add a method called .validate() to your Serializer subclass. This method takes a single argument, which is a dictionary of field values. It should raise a serializers.ValidationError if necessary, or just return the validated values. For example:
```python
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```

##### Custom Validator (Example)
Individual fields on a serializer can include validators, by declaring them on the field instance, for example:
```python
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
```






# Views
As seen in Django Rest Framework docs [(Link)](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset), the ModelViewSet class inherits from GenericAPIView and includes implementations for various actions, by mixing in the behavior of the various mixin classes. The actions provided by the ModelViewSet class are .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().

````python
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
````

### Adding authentication permissions to views (Example)
REST framework includes a number of permission classes that we can use to restrict who can access a given view. In this case the one we're looking for is IsAuthenticatedOrReadOnly, which will ensure that authenticated requests get read-write access, and unauthenticated requests get read-only access. [(Link)](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/)

````python
from rest_framework import permissions
````
````python
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
````

### Different permissions for different actions
You may inspect these attributes to adjust behaviour based on the current action. For example, you could restrict permissions to everything except the list action similar to this:
```python
def get_permissions(self):
    """
    Instantiates and returns the list of permissions that this view requires.
    """
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]
```

### Adding addicional validations to default ModelViewSetFunctions (Example)
This function calls the given model and get object from that if that object or model doesn't exist it raise 404 error.
````python
def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object_or_404(Movie, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
````

### Extra actions with validation (Example)

Getting the Movie director by using an extra action with a different serializer
````python            
class MovieDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'director')
````  

````python            
@action(detail=True, methods=["get"], url_path='movie-director')
    def movie_director(self, request, pk=None):
        movie = self.get_object_or_404(Movie, pk=pk)
        serializer = self.get_serializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
````
Another example using actions:
````python
@action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        user = self.get_object_or_404(User, pk=pk)
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
@action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
````  

#### If a custom endpoint doesn't use Serializer, we must validate each param individually (Example)

```python
def check_positive_numbers(value1, value2):
    if value1 <= 0 || value2 <= 0:
        raise ValidationError(
            _('The values must be greater than 0')
        )
```
```python
def validate_birth_date(self, request):
    birth_date = request.GET.get("birth_date", "")
    if not birth_date:
        return None
    if birth_date >= datetime.date.today():
        raise ValidationError(_('Enter an accurate birthdate.'))
    return date
```