from poll.models import Question

def polls_count(request):
    count=Question.objects.count()
    # print('polls count-----',count)
    return {'polls_count':count}
