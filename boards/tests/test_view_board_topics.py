from django.test import TestCase
from django.urls import reverse, resolve
from boards.models import Board
# from boards.views import board_topics
from boards.views import TopicListView


class BoardTopicsTests(TestCase):
    def setUp(self): #setUp: Run once for every test method to setup clean data.
       self.board = Board.objects.create(name='Django', description='Django board.')

    # #not work
    def test_board_topics_view_success_status_code(self):
        path = reverse('board_topics', kwargs={'pk': self.board.pk})
        # self.assertEquals(resolve(path).func, board_topics)
        self.assertEquals(resolve(path).func.view_class, TopicListView)
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)


    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TopicListView)
    #     self.assertEquals(view.func, board_topics)

    # # not work
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    # # not work
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
