# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Kafeman <kafemanw@gmail.com>
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

import json
import urllib


ENDPOINT = 'https://api.habrahabr.ru/v1'
OAUTH_URL = 'https://habrahabr.ru/auth/o/login/'


def _fetch_url(url, method, data, headers):
    if data is not None:
        data = urllib.urlencode(data)
    request = urllib.request.Request(url, data, headers)
    request.get_method = lambda: method
    response = urllib.request.urlopen(request)
    return response.read()


class Service:
    """Абстрактный сервис для наследования."""
    def __init__(self, **settings):
        """Инициализировать сервис."""
        if 'client' not in settings or 'token' not in settings:
            raise ValueError('Нужно указать ID клиента и токен')
        self.settings = settings

    def request(self, resource, method='GET', data=None):
        """Послать запрос на сервер Хабрахабра и распарсить ответ."""
        url = self.settings.get('endpoint') + resource
        headers = { 'client': self.settings.get('client'),
                    'token': self.settings.get('token') }
        resp = _fetch_url(url, method, data, headers)
        return json.loads(resp)


class CommentService(Service):
    """Сервис для работы с комментариями."""
    def get(self, post_id):
        """Получить комментарии к посту."""
        return self.request('/comments/%d' % post_id)

    def add(self, post_id, text, parent_id=0):
        """Добавить комментарий к посту."""
        data = {'text': text, 'parent_id': parent_id}
        return self.request('/comments/%d' % post_id, method='PUT', data=data)

    def vote(self, comment_id, vote):
        """Проголосовать за комментарий."""
        if vote not in [-1, 1]:
            raise ValueError('Неверный формат голоса')
        data = {'vote': vote}
        return self.request('/comments/%d/vote' % comment_id, method='PUT', data=data)

    def vote_plus(self, comment_id):
        """Проголосовать за комментарий положительно."""
        return self.vote(comment_id, 1)

    def vote_minus(self, comment_id):
        """Проголосовать за комментарий отрицательно."""
        return self.vote(comment_id, -1)


class CompanyService(Service):
    """Сервис для работы с компаниями."""
    def get_posts(self, alias, page=1):
        """Получить посты из корпоративного блога компании."""
        return self.request('/company/%s?page=%d' % (alias, page))

    def get_info(self, alias):
        """Получить информацию о компании."""
        return self.request('/company/%s/info' % alias)


class FeedService(Service):
    """Сервис для работы с лентой пользователя."""
    def get_habred(self, page=1):
        """Получить захабренные посты."""
        return self.request('/feed/habred?page=%d' % page)

    def get_unhabred(self, page=1):
        """Получить отхабренные посты."""
        return self.request('/feed/unhabred?page=%d' % page)

    def get_new(self, page=1):
        """Получить новые посты."""
        return self.request('/feed/new?page=%d' % page)


class HubService(Service):
    """Сервис для работы с хабами."""
    def get_info(self, alias):
        """Получить информацию о хабе."""
        return self.request('/hub/%s/info' % alias)

    def get_habred(self, alias, page=1):
        """Получить захабренные посты."""
        return self.request('/hub/%s/habred?page=%d' % (alias, page))

    def get_unhabred(self, alias, page=1):
        """Получить отхабренные посты."""
        return self.request('/hub/%s/unhabred?page=%d' % (alias, page))

    def get_new(self, alias, page=1):
        """Получить новые посты."""
        return self.request('/hub/%s/new?page=%d' % (alias, page))

    def get_all(self, page=1):
        """Получить все хабы."""
        return self.request('/hubs?page=%d' % page)

    def get_categories(self):
        """Получить категории хабов."""
        return self.request('/hubs/categories')

    def get_by_category(self, category, page=1):
        """Получить хабы, относящиеся к указанной категории."""
        return self.request('/hubs/categories/%s?page=%d' % (category, page))

    def subscribe(self, alias):
        """Подписать пользователя на хаб."""
        return self.request('/hub/%s' % alias, method='PUT')

    def unsubscribe(self, alias):
        """Отписать пользователя от хаба."""
        return self.request('/hub/%s' % alias, method='DELETE')


class PollService(Service):
    """Сервис для работы с опросами."""
    def get(self, poll_id):
        """Получить опрос."""
        return self.request('/polls/%d' % poll_id)

    def vote(self, poll_id, answer_id):
        """Проголосовать за один или несколько ответов."""
        pass


class PostService(Service):
    """Сервис для работы с постами."""
    def get(self, post_id):
        """Получить информацию о посте по его ID."""
        return self.request('/post/%d' % post_id)

    def vote(self, post_id, vote):
        """Проголосовать за пост.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        if vote not in [-1, 0, 1]:
            raise ValueError('Неверный формат голоса')
        data = {'vote': vote}
        return self.request('/post/%d/vote' % post_id, method='PUT', data=data)

    def vote_plus(self, post_id):
        """Проголосовать за пост положительно.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        return self.vote(post_id, 1)

    def vote_minus(self, post_id):
        """Проголосовать за пост отрицательно.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        return self.vote(post_id, -1)

    def vote_neutral(self, post_id):
        """Проголосовать за пост нейтрально.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        return self.vote(post_id, 0)

    def add_to_favorite(self, post_id):
        """Добавить пост в избранное."""
        return self.request('/post/%d/favorite' % post_id, method='PUT')

    def remove_from_favorite(self, post_id):
        """Удалить пост из избранного."""
        return self.request('/post/%d/favorite' % post_id, method='DELETE')

    def increment_view_counter(self, post_id):
        """Увеличить счетчик просмотров."""
        return self.request('/post/%d/viewcount' % post_id, method='PUT')

    def get_meta(self, post_ids):
        """Получить мета-информацию постов.

        В настоящий момент можно запрашивать не более 30 постов за раз.
        """
        ids = ','.join(post_ids)
        return self.request('/posts/meta?ids=%s' % ids)


class SearchService(Service):
    """Сервис для поиска."""
    def search_posts(self, query, page=1):
        """Искать в постах."""
        return self.request('/search/posts/%s?page=%d' % (query, page))

    def search_users(self, query, page=1):
        """Искать в пользователях."""
        return self.request('/search/users/%s?page=%d' % (query, page))

    def search_hubs(self, query):
        """Искать в хабах."""
        return self.request('/hubs/search/%s' % query)


class SettingsService(Service):
    """Сервис для настроек."""
    def accept_agreement(self, query, page=1):
        """Принять соглашение."""
        return self.request('/settings/agreement', method='PUT')


class TrackerService(Service):
    """Сервис для работы с трекером пользователя."""
    def push(self, title, text):
        """Отправить уведомление в раздел "Приложения"."""
        data = {'title': title, 'text': text}
        return self.request('/tracker', method='PUT', data=data)

    def get_counters(self):
        """Получить количество новых уведомлений.

        Уведомления не отмечаются как просмотренные.
        """
        return self.request('/tracker/counters')

    def get_posts(self):
        """Получить уведомления из раздела "Посты".

        Уведомления не отмечаются как просмотренные."""
        return self.request('/tracker/posts')

    def get_subscribers(self):
        """Получить уведомления из раздела "Подписчики".

        Уведомления не отмечаются как просмотренные."""
        return self.request('/tracker/subscribers')

    def get_mentions(self):
        """Получить уведомления из раздела "Упоминания".

        Уведомления не отмечаются как просмотренные."""
        return self.request('/tracker/mentions')

    def get_apps(self):
        """Получить уведомления из раздела "Приложения".

        Уведомления не отмечаются как просмотренные."""
        return self.request('/tracker/apps')


class UserService(Service):
    """Сервис для работы с пользователями."""
    def get(self, username=None):
        """Получить информацию о пользователе или список из 100 пользователей с
        самым высоким рейтингом."""
        if username:
            return self.request('/users/%s' % username)
        return self.request('/users')

    def get_current_user(self):
        """Получить информацию о текущем пользователе."""
        return self.get('me')

    def get_comments(self, username, page=1):
        """Получить комментарии пользователя."""
        return self.request('/users/%s/comments?page=%d' % (username, page))

    def get_posts(self, username):
        """Получить посты пользователя."""
        return self.request('/users/%s/posts?page=%d' % (username, page))

    def get_hubs(self, username):
        """Получить хабы на которые подписан пользователь."""
        return self.request('/users/%s/hubs' % username)

    def get_companies(self, username, page=1):
        """Получить компании, в которых работает пользователь."""
        return self.request('/users/%s/companies' % username)

    def get_followers(self, username, page=1):
        """Получить подписчиков пользователя."""
        return self.request('/users/%s/followers?page=%d' % (username, page))

    def get_followed(self, username, page=1):
        """Получить пользователей, которые подписаны на данного пользователя."""
        return self.request('/users/%s/followed?page=%d' % (username, page))

    def vote_plus(self, username):
        """Проголосовать за карму положительно.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        return self.request('/users/%s/vote' % username, method='PUT')

    def vote_minus(self, username):
        """Проголосовать за карму отрицательно.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        return self.request('/users/%s/vote' % username, method='DELETE')

    def get_favorite_comments(self, username, page=1):
        """Получить избранные комментарии пользователя."""
        return self.request('/users/%s/favorites/comments?page=%d' % (username, page))

    def get_favorite_posts(self, username, page=1):
        """Получить избранные посты пользователя."""
        return self.request('/users/%s/favorites/posts?page=%d' % (username, page))


class Api:
    """Базовый класс для работы с API Хабрахабра."""
    def __init__(self, **settings):
        """Инициализирует клиента API."""
        self._settings = settings
        if 'endpoint' not in self._settings:
            self._settings['endpoint'] = ENDPOINT
        # TODO(kafeman): Сделать "ленивую" инициализацию, чтобы сервисы
        # создавались только при необходимости и кешировались
        self.comments = CommentService(**self._settings)
        self.companies = CompanyService(**self._settings)
        self.feed = FeedService(**self._settings)
        self.hubs = HubService(**self._settings)
        self.polls = PollService(**self._settings)
        self.posts = PostService(**self._settings)
        self.search = SearchService(**self._settings)
        self.settings = SettingsService(**self._settings)
        self.tracker = TrackerService(**self._settings)
        self.users = UserService(**self._settings)

    def get_authorization_url(self, redirect_uri, response_type='code'):
        """Составить URL для запроса доступа."""
        data = { 'redirect_uri': redirect_uri,
                 'response_type': response_type,
                 'client_id': self._settings.get('client') }
        return OAUTH_URL + '?' + urllib.urlencode(data)
