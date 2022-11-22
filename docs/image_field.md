# Image Field

For the ImageField to work it's necessary to have the Pillow library installed.

## Django Models

The setup of the model containing the image field can be done in the following way.

````python
class BookInformation(models.Model):
    #...
    cover_image = models.ImageField(upload_to="covers/", null=True)
    #...
````
Note that the `upload_to` option corresponds to the path in which the images are stored/saved in the media folder.
In this case the path will be `.../library_project/media/covers/`.

## Factory Boy mock data

The easiest way to generate mock images data with factory boy is with the `factory.django.ImageField()` method just like the example below.

```` python 
class BookInformationFactory(factory.django.DjangoModelFactory):
    #...
    cover_image = factory.django.ImageField(color=factory.Faker("color"))
    #...
````

Note that the `color` option can Hardcoded with something like `color="blue"` and that will result in the 
generation of images with the color blue. In this case, `factory.Faker("color")` will generate random color names
which will result in the generation of images with diferent colors for each `cover_image`.

## ImageField Views Tests

To test the views that involve the `cover_image` attribute you can simply generate an image based on the
implemented factory for the cover image just like the example below.

````python
from PIL import Image
import shutil
from ..fixtures import REMOVE_MEDIA_FILES_PATH

class BookCreateViewTestCase(APITestCase):
    def setUp(self):
        #...
        self.data = {
            "cover_image": #...
            #...
        }

    def tearDown(self):
        shutil.rmtree(REMOVE_MEDIA_FILES_PATH)

    def test_create_with_image(self):
        cover = BookInformationFactory.create().cover_image

        self.data["cover_image"] = cover
        res = self.client.post(self.url, self.data, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            BookInformation.objects.first().cover_image.read(), BookInformation.objects.last().cover_image.read()
        )

    def test_create_with_image_failure(self):
        self.data["cover_image"] = Image.new(mode="RGB", size=(20, 20))

        res = self.client.post(self.url, self.data, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

```` 

It is crucial that the `format` option in set to `"multipart"` for the test to work. 
It is also important to have the `tearDown` method implemented in order to delete the images
saved on the folder refered previously (`.../library_project/media/covers/`).

## ImageField Views Tests using temp files

Other way of implementing a view test that includes an ImageField is with the `SimpleUploadedFile()` method.

````python
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
import shutil

class BookCreateViewTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "cover_image": #...
            #...
        }

    def tearDown(self):
        shutil.rmtree(REMOVE_MEDIA_FILES_PATH)

    def test_create_with_image(self):
        image = Image.new(mode="RGB", size=(20, 20))

        tempFile = BytesIO()
        image.save(tempFile, format="JPEG")
        tempFile.seek(0)

        with tempFile as temp:
            image = SimpleUploadedFile("sample.jpg", temp.read(), content_type="image/jpeg")
            self.data["cover_image"] = image

            res = self.client.post(self.url, self.data, format="multipart")
            image.seek(0)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookInformation.objects.first().cover_image.read(), image.read())


````
The code above will generate an Image with the PIL Library, save it in a temporary file,
process it with `SimpleUploadedFile()` method and then make the POST request.

In this case the tearDown method still needs to be implemented, since the POST
request will save the image in the media folder.
