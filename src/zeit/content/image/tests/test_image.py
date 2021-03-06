from zeit.content.image.testing import create_image_group
import zeit.cms.checkout.interfaces
import zeit.cms.interfaces
import zeit.cms.testing
import zeit.content.image.testing
import zope.component


class TestImageMetadataAcquisition(zeit.cms.testing.FunctionalTestCase):

    layer = zeit.content.image.testing.ZCML_LAYER

    def setUp(self):
        super(TestImageMetadataAcquisition, self).setUp()
        self.group_id = create_image_group().uniqueId
        with zeit.cms.checkout.helper.checked_out(self.group) as co:
            metadata = zeit.content.image.interfaces.IImageMetadata(co)
            metadata.title = u'Title'

    @property
    def group(self):
        return zeit.cms.interfaces.ICMSContent(self.group_id)

    @property
    def img(self):
        return self.group['new-hampshire-450x200.jpg']

    def test_acquired_in_repository(self):
        metadata = zeit.content.image.interfaces.IImageMetadata(self.img)
        self.assertEqual(u'Title', metadata.title)

    def test_acquired_in_workingcopy(self):
        with zeit.cms.checkout.helper.checked_out(self.img) as co:
            metadata = zeit.content.image.interfaces.IImageMetadata(co)
            self.assertEqual(u'Title', metadata.title)
            metadata.title = u'Image title'
        metadata = zeit.content.image.interfaces.IImageMetadata(self.img)
        self.assertEqual(u'Image title', metadata.title)

    def test_in_workingcopy_when_removed_in_repository(self):
        co = zeit.cms.checkout.interfaces.ICheckoutManager(self.img).checkout()
        del self.group[self.img.__name__]
        metadata = zeit.content.image.interfaces.IImageMetadata(co)
        self.assertEqual(None, metadata.title)


class TestImageXMLReference(zeit.cms.testing.FunctionalTestCase):

    layer = zeit.content.image.testing.ZCML_LAYER

    def test_master_image_without_filename_extension_sets_mime_as_type(self):
        fh = self.repository['2006']['DSC00109_2.JPG'].open()
        image = zeit.content.image.image.LocalImage()
        image.mimeType = 'image/jpeg'
        image.open('w').write(fh.read())
        self.repository['example-image'] = image
        ref = zope.component.getAdapter(
            self.repository['example-image'],
            zeit.cms.content.interfaces.IXMLReference, name='image')
        self.assertEqual('jpeg', ref.get('type'))
