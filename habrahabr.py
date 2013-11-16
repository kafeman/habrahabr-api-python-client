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
import urllib2


ENDPOINT = 'https://api.habrahabr.ru/v1'


def _fetch_url(url, method, data, headers):
    if data is not None:
        data = urllib.urlencode(data)
    request = urllib2.Request(url, data, headers)
    request.get_method = lambda: method
    response = urllib2.urlopen(request)
    return response.read()


class ClientError(Exception):
    """ Ошибка клиента.
    """
    @property
    def message(self):
        return self.args[0]


class Service:
    """ Абстрактный сервис для наследования.
    """
    def __init__(self, **settings):
        """ Инициализирует сервис.
        """
        # Все ресурсы API Хабрахабра требуют авторизации
        # TODO Возможно, это можно записать красивее?
        if 'client' not in settings or 'token' not in settings:
            raise ClientError('Нужно указать ID клиента и токен')
        self.settings = settings

    def request(self, resource, method='GET', data=None):
        """ Посылает запросы на сервера Хабрахабра и парсит ответ.
        """
        url = self.settings.get('endpoint') + resource
        headers = { 'client': self.settings.get('client'),
                    'token': self.settings.get('token') }
        resp = _fetch_url(url, method, data, headers)
        return json.loads(resp)


class CommentService(Service):
    """ Сервис для работы с комментариями.
    """
    def get(self, post_id):
        """ Получает комментарии к посту.
        """
        return self.request('/comments/%d' % post_id)

    def add(self, post_id, text, parent_id=0):
        """ Добавляет комментарий к посту.
        """
        data = {'text': text, 'parent_id': parent_id}
        return self.request('/comments/%d' % post_id, method='PUT', data=data)


class CompanyService(Service):
    """ Сервис для работы с компаниями.
    """
    def get_posts(self, alias, page=1):
        """ Получает посты из корпоративного блога компании.
        """
        return self.request('/company/%s?page=%d' % (alias, page))

    def get_info(self, alias):
        """ Получает информацию о компании.
        """
        return self.request('/company/%s/info' % alias)


class FeedResource(Service):
    """ Сервис для работы с лентой пользователя.
    """
    def get_habred(self, page=1):
        """ Получает захабренные посты.
        """
        return self.request('/feed/habred?page=%d' % page)

    def get_unhabred(self, page=1):
        """ Получает отхабренные посты.
        """
        return self.request('/feed/unhabred?page=%d' % page)

    def get_new(self, page=1):
        """ Получает новые посты.
        """
        return self.request('/feed/new?page=%d' % page)


class HubService(Service):
    """ Сервис для работы с хабами.
    """
    def get_info(self, alias):
        """ Получает информацию о хабе.
        """
        return self.request('/hub/%s/info' % alias)

    def get_habred(self, alias, page=1):
        """ Получает захабренные посты.
        """
        return self.request('/hub/%s/habred?page=%d' % (alias, page))

    def get_unhabred(self, alias, page=1):
        """ Получает отхабренные посты.
        """
        return self.request('/hub/%s/unhabred?page=%d' % (alias, page))

    def get_new(self, alias, page=1):
        """ Получает новые посты.
        """
        return self.request('/hub/%s/new?page=%d' % (alias, page))


class PostService(Service):
    """ Сервис для работы с постами.
    """
    def get(self, post_id):
        """ Получает пост по id.
        """
        return self.request('/post/%d' % post_id)

    def vote(self, post_id, vote):
        """ Голосует за пост.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        if vote not in [-1, 0, 1]:
            raise ClientError('Неверный формат голоса')
        data = {'vote': vote}
        return self.request('/post/%d/vote' % post_id, method='PUT', data=data)

    def add_to_favorite(self, post_id):
        """ Добавляет пост в избранное.
        """
        return self.request('/post/%d/favorite' % post_id, method='PUT')

    def remove_from_favorite(self, post_id):
        """ Удаляет пост из избранного.
        """
        return self.request('/post/%d/favorite' % post_id, method='DELETE')


class SearchService(Service):
    """ Сервис для поиска.
    """
    def search_posts(self, query, page=1):
        """ Получает результаты поиска для постов.
        """
        return self.request('/search/posts/%s?page=%d' % (query, page))

    def search_users(self, query, page=1):
        """ Получает результаты поиска для пользователей.
        """
        return self.request('/search/users/%s?page=%d' % (query, page))


class TrackerService(Service):
    """ Сервис для работы с трекером пользователя.
    """
    def push(self, title, text):
        """ Отправляет сообщение в раздел "Приложения".
        """
        data = {'title': title, 'text': text}
        return self.request('/tracker', method='PUT', data=data)

    def get_counters(self):
        """ Получает счетчик новых сообщений.
        """
        return self.request('/tracker/counters')

    def get_posts(self):
        """ Получает сообщения из раздела "Посты".
        """
        return self.request('/tracker/posts')

    def get_subscribers(self):
        """ Получает сообщения из раздела "Подписчики".
        """
        return self.request('/tracker/subscribers')

    def get_mentions(self):
        """ Получает сообщения из раздела "Упоминания".
        """
        return self.request('/tracker/mentions')

    def get_apps(self):
        """ Получает сообщения из раздела "Приложения".
        """
        return self.request('/tracker/apps')


class UserService(Service):
    """ Сервис для работы с пользователями.
    """
    def get(self, username=None):
        """ Получает информацию о пользователе по логину или список из 100
        пользователей с самым высоким рейтингом.
        """
        if username:
            return self.request('/users/%s' % username)
        return self.request('/users')

    def get_comments(self, username, page=1):
        """ Получает комментарии пользователя.
        """
        return self.request('/users/%s/comments?page=%d' % (username, page))

    def get_posts(self, username):
        """ Получает посты пользователя.
        """
        return self.request('/users/%s/posts?page=%d' % (username, page))

    def get_hubs(self, username):
        """ Получает хабы на которые подписан пользователь.
        """
        return self.request('/users/%s/hubs' % username)

    def get_companies(self, username, page=1):
        """ Получает компании в которых работает пользователь.
        """
        return self.request('/users/%s/companies' % username)

    def get_followers(self, username, page=1):
        """ Получает подписчиков пользователя.
        """
        return self.request('/users/%s/followers?page=%d' % (username, page))

    def get_followed(self, username, page=1):
        """ Кто подписан на пользователя, c пагинацией.
        """
        return self.request('/users/%s/followed?page=%d' % (username, page))

    def vote_plus(self, username):
        """ Голосует положительно за карму пользователя.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        return self.request('/users/%s/vote' % username, method='PUT')

    def vote_minus(self, username):
        """ Голосует отрицательно за карму пользователя.

        Этот метод отключен по-умолчанию. Для включения обратитесь в службу
        технической поддержки Хабрахабра.
        """
        return self.request('/users/%s/vote' % username, method='DELETE')


class Api:
    """ Базовый класс для работы с API Хабрахабра.
    """
    def __init__(self, **settings):
        """ Инициализирует клиента API.
        """
        self.settings = settings
        if 'endpoint' not in self.settings:
            self.settings['endpoint'] = ENDPOINT
        self.services = [
            ('comments', CommentService),
            ('companies', CompanyService),
            ('feed', FeedResource),
            ('hubs', HubService),
            ('posts', PostService),
            ('search', SearchService),
            ('tracker', TrackerService),
            ('users', UserService),
        ]
        for service in self.services:
            self.__dict__[service[0]] = service[1](**self.settings)
