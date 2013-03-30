"""
Tests for suite results view.

"""
from django.core.urlresolvers import reverse

from tests import case

from ...lists.runs import RunsListTests



class SuiteResultsViewTest(case.view.ListViewTestCase,
                         RunsListTests,
                         case.view.ListFinderTests,
                         ):
    """Tests for suite results view."""
    @property
    def factory(self):
        """The Suite factory."""
        return self.F.SuiteFactory


    @property
    def url(self):
        """Shortcut for run results url."""
        return reverse("results_suites")


    def test_sort_by_start(self):
        """Suites don't have starts"""
        pass

    def test_sort_by_productversion(self):
        """Suites don't have productversions"""
        pass

    def test_sort_by_end(self):
        """Suites don't have ends"""
        pass

    def test_filter_by_suite(self):
        """Redundant"""
        pass



class SuiteDetailTest(case.view.AuthenticatedViewTestCase):
    """Test for suite-detail ajax view."""
    def setUp(self):
        """Setup for suite details tests; create a run."""
        super(SuiteDetailTest, self).setUp()
        self.testsuite = self.F.SuiteFactory.create()


    @property
    def url(self):
        """Shortcut for run detail url."""
        return reverse(
            "results_suite_details",
            kwargs=dict(suite_id=self.suite.id)
            )


    def test_details_description(self):
        """Details lists description."""
        self.testsuite.description = "foodesc"
        self.testsuite.save()

        res = self.get(headers={"X-Requested-With": "XMLHttpRequest"})

        res.mustcontain("foodesc")


    def test_details_envs(self):
        """Details lists envs."""
        self.testsuite.environments.add(
            *self.F.EnvironmentFactory.create_full_set({"OS": ["Windows"]}))

        res = self.get(headers={"X-Requested-With": "XMLHttpRequest"})

        res.mustcontain("Windows")


    def test_details_team(self):
        """Details lists team."""
        u = self.F.UserFactory.create(username="somebody")
        self.testsuite.add_to_team(u)

        res = self.get(headers={"X-Requested-With": "XMLHttpRequest"})

        res.mustcontain("somebody")


    def test_details_drilldown(self):
        """Details contains link to drilldown to suites."""
        res = self.get(headers={"X-Requested-With": "XMLHttpRequest"})

        res.mustcontain(
            "{0}?filter-suite={1}".format(
                reverse("results_suitess"), self.testsuite.id)
            )
