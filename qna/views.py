from django.shortcuts import render, redirect
from .decorators import unauthentiated_user
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from django.core.paginator import Paginator

#  - upvote downvote
def index(request):
    questions = Question.objects.all().order_by('-point')[:40]
    # print(questions)
    # Paginatior
    p = Paginator(questions, 8)
    page_num = request.GET.get('p', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {'questions':page, 'pageNo': range(p.num_pages)}
    return render(request, 'qna/index.html', context)

@ unauthentiated_user
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

    form = CreateUserForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

def about(request):
    return render(request, 'qna/about.html')
    
@login_required
def newQuestion(request):

    if request.method=='POST':
        title = request.POST.get('title', '').strip()
        if(title != ''):
            description = request.POST.get('description', '').strip()
            q = Question.objects.create(user=request.user, title=title, description=description)
            return redirect(f'/{q.slug}')

    return render(request, 'qna/newQuestion.html')

def question(request, slug):
    # find the question
    try:
        ques = Question.objects.get(slug=slug)
    except:
        return render(request, 'qna/404.html')

    if request.method == 'POST':
        answer = request.POST.get('answer', '').strip()
        if answer != '' and request.user.is_authenticated:
            newAnswer = Answer.objects.create(question=ques, user=request.user, body=answer)


    context = {'question': ques}
    # print(ques.answer_set.all())
    return render(request, 'qna/question.html', context)

@login_required
def myQuestions(request):
    questions = Question.objects.filter(user=request.user)

    # Paginatior
    p = Paginator(questions, 8)
    page_num = request.GET.get('p', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {'questions':page, 'pageNo': range(p.num_pages)}
    return render(request, 'qna/myQuestions.html', context)

@login_required
def myAnswers(request):
    answers = Answer.objects.filter(user = request.user)
    questions = Question.objects.filter(answer__in = answers)
    print(questions)
    # Paginatior
    p = Paginator(questions, 8)
    page_num = request.GET.get('p', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {'questions':page, 'pageNo': range(p.num_pages)}
    return render(request, 'qna/myAnswers.html', context)

def search(request):
    query = request.GET.get('q', '').strip()
    if(query == ''):
        return redirect('index')
    questions = Question.objects.filter(title__contains = query)
    print(questions)
    # Paginatior
    p = Paginator(questions, 8)
    page_num = request.GET.get('p', 1)
    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {'questions':page, 'pageNo': range(p.num_pages), 'query': query}
    return render(request, 'qna/search.html', context)

@login_required
def updateVote(request):    
    slug = request.GET.get('slug')
    isAnswer = request.GET.get('isAnswer', False)
    answerId = request.GET.get('answerId')
    voteType = request.GET.get('voteType')

    if(slug and voteType):
        try:
            question = Question.objects.get(slug=slug)
        except:
            return render(request, 'qna/404.html')
        if(isAnswer):
            if(answerId):
                try:
                    answer = Answer.objects.get(id=answerId)
                    # update vote of answer
                    if(voteType == 'up'):
                        if request.user not in answer.likedUsers.all():
                            answer.likedUsers.add(request.user)
                            if request.user in answer.disLikedUsers.all():
                                answer.disLikedUsers.remove(request.user) 
                        else:
                            answer.likedUsers.remove(request.user)
                        answer.point = len(answer.likedUsers.all()) - len(answer.disLikedUsers.all())
                        answer.save()
                    else:
                        if request.user not in answer.disLikedUsers.all():
                            answer.disLikedUsers.add(request.user)
                            if request.user in answer.likedUsers.all():
                                answer.likedUsers.remove(request.user)
                        else:
                            answer.disLikedUsers.remove(request.user)
                        answer.point = len(answer.likedUsers.all()) - len(answer.disLikedUsers.all())
                        answer.save()
                    return redirect(f"/{slug}/")
                except:
                    print("Hello")
                    return render(request, 'qna/404.html')
            else:
                return render(request, 'qna/404.html')
        else:
            # update vote of question
            if(voteType == 'up'):
                if request.user not in question.likedUsers.all():
                    question.likedUsers.add(request.user)
                    if request.user in question.disLikedUsers.all():
                        question.disLikedUsers.remove(request.user)
                else:
                    question.likedUsers.remove(request.user)
                question.point = len(question.likedUsers.all()) - len(question.disLikedUsers.all())
                question.save()
            else:
                if request.user not in question.disLikedUsers.all():
                    question.disLikedUsers.add(request.user)
                    if request.user in question.likedUsers.all():
                        question.likedUsers.remove(request.user)
                else:
                    question.disLikedUsers.remove(request.user)
                question.point = len(question.likedUsers.all()) - len(question.disLikedUsers.all())
                question.save()
            return redirect(f"/{slug}/")

    return render(request, 'qna/404.html')
    # GET method
    # question slug, isAnswer, if answer then answer id, vote type
    # if already voted(both for up and down) then doesn't increase