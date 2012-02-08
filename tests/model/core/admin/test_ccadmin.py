# Case Conductor is a Test Case Management system.
# Copyright (C) 2011-2012 Mozilla
#
# This file is part of Case Conductor.
#
# Case Conductor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Case Conductor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.
"""
Tests for CC base admin forms.

"""
from django.contrib.admin.sites import AdminSite

from tests import case



class CCModelFormTest(case.DBTestCase):
    """Tests of CCModelForm."""
    @property
    def form(self):
        """The form class under test."""
        from cc.model.ccadmin import CCModelForm
        return CCModelForm


    def test_commit(self):
        """CCModelForm passes in user when saving model with commit=True."""
        u = self.F.UserFactory.create()
        p = self.F.ProductFactory.create(name="Firefox")
        f = self.form(instance=p, data={"name": "Fennec"})

        p = f.save(commit=True, user=u)

        self.assertEqual(p.modified_by, u)


    def test_no_commit(self):
        """CCModelForm patches save() so user is tracked w/ commit=False."""
        u = self.F.UserFactory.create()
        p = self.F.ProductFactory.create(name="Firefox")
        f = self.form(instance=p, data={"name": "Fennec"})

        p = f.save(commit=False, user=u)
        p.save()

        self.assertEqual(p.modified_by, u)



class TeamModelAdminTest(case.DBTestCase):
    """Tests of TeamModelAdmin."""
    @property
    def admin(self):
        """The model admin class under test."""
        from cc.model.ccadmin import TeamModelAdmin
        return TeamModelAdmin


    def test_fieldsets(self):
        """Sans declared fieldsets, puts team fields into Team fieldset."""
        ma = self.admin(self.model.ProductVersion, AdminSite())

        fs = ma.get_fieldsets(None, None)

        self.assertEqual(len(fs), 4)

        default, team, deletion, meta = fs

        self.assertNotIn("has_team", default[1]["fields"])
        self.assertNotIn("own_team", default[1]["fields"])
        self.assertEqual(team[0], "Team")
        self.assertEqual(team[1]["fields"], [("has_team", "own_team")])
