from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer


class CollectionJsonLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import pmr2.json
        self.loadZCML(package=pmr2.json)
        self.loadZCML('testing.zcml', package=pmr2.json.testing)

COLLECTION_JSON_FIXTURE = CollectionJsonLayer()

COLLECTION_JSON_LAYER = IntegrationTesting(
    bases=(COLLECTION_JSON_FIXTURE,), name="pmr2.json.collection:integration",)
