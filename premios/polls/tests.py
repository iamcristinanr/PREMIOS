import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Con quién te gustaría ir a tu destino favorito?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=32)
        """import pdb; pdb.set_trace()"""
        past_question = Question(question_text="¿Con quién te gustaría ir a tu destino favorito?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the present"""
        time = timezone.now() - datetime.timedelta(hours=1)
        present_question = Question(question_text="¿Con quién te gustaría ir a tu destino favorito?", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the give "question_text", and published the given number of days
    offset to now (negative for questions published in past, positive for questions that have
    yet to be publised)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choice(pk, choice_text, votes=0):
    """
    Create a choice that have the pk(primary key is a number) of a specific question
    with the given "choice_text" and with the given "votes"(votes starts in zero)
    """
    question = Question.objects.get(pk=pk)
    return question.choice_set.create(choice_text=choice_text, votes=votes)

  
class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on the index page.
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page
        """
        question = create_question("Past question", days=-10)
        choice1 = create_choice(pk=question.id, choice_text="España", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="Noruega", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        past_question = create_question(question_text="Past question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        choice1 = create_choice(pk=past_question.id, choice_text="España", votes=0)
        choice2 = create_choice(pk=past_question.id, choice_text="Noruega", votes=0)
        choice1 = create_choice(pk=future_question.id, choice_text="España", votes=0)
        choice2 = create_choice(pk=future_question.id, choice_text="Noruega", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        past_question1 = create_question(question_text="Past question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        choice1 = create_choice(pk=past_question1.id, choice_text="España", votes=0)
        choice2 = create_choice(pk=past_question1.id, choice_text="Noruega", votes=0)
        choice1 = create_choice(pk=past_question2.id, choice_text="España", votes=0)
        choice2 = create_choice(pk=past_question2.id, choice_text="Noruega", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_questions(self):
        """
        The questions index page display any questions.
        """
        future_question1 = create_question(question_text="Furure question 1", days=30)
        future_question2 = create_question(question_text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_question_without_choices(self):
        """
        The user never can create questions with less than two choices
        """
        question = create_question("Cuál es tu país favorito?", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_question_with_choices(self):
        """
        Question with choices are displayed in the index view
        """
        question = create_question("Cuál es tu país favorito?", days=-30)
        choice1 = create_choice(pk=question.id, choice_text="España", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="Noruega", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


class QuestionDetailVieWTest(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 error 
        not found
        """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
   
    def test_past_question(self):
        """
        The detail view of a quesetion with a pub_date in the past displays the quetion's 
        text
        """
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultVieWTest(TestCase):
    def test_show_result_past_question(self):
        """
        The result view display the question's text for a question from the pass
        """
        past_question = create_question("past question", days=-15)
        url = reverse("polls:results", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_not_show_result_future_question(self):
        """
        The result view aren't displayed for a question from the future and this return a 404 error
        """
        future_question = create_question("this is a future question", days=30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)