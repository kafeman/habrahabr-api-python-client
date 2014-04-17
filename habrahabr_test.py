# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Kafeman <kafemanw@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import habrahabr


class TestCase(unittest.TestCase):
    def assert_is_instance(self, obj, cls):
        if not isinstance(obj, cls):
            msg = '%s is not an instance of %r' % (safe_repr(obj), cls)
            self.fail(msg)


class ApiTestCase(TestCase):
    def setUp(self):
        self.api = habrahabr.Api(token='', client='')

    def test_comments(self):
        self.assert_is_instance(self.api.comments, habrahabr.CommentService)

    def test_companies(self):
        self.assert_is_instance(self.api.companies, habrahabr.CompanyService)

    def test_feed(self):
        self.assert_is_instance(self.api.feed, habrahabr.FeedService)

    def test_hubs(self):
        self.assert_is_instance(self.api.hubs, habrahabr.HubService)

    def test_polls(self):
        self.assert_is_instance(self.api.polls, habrahabr.PollService)

    def test_posts(self):
        self.assert_is_instance(self.api.posts, habrahabr.PostService)

    def test_search(self):
        self.assert_is_instance(self.api.search, habrahabr.SearchService)

    def test_settings(self):
        self.assert_is_instance(self.api.settings, habrahabr.SettingsService)

    def test_tracker(self):
        self.assert_is_instance(self.api.tracker, habrahabr.TrackerService)

    def test_users(self):
        self.assert_is_instance(self.api.users, habrahabr.UserService)


if __name__ == '__main__':
    unittest.main()
