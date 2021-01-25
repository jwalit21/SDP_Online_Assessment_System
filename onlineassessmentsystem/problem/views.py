from django.shortcuts import render, redirect
from .models import Problem, ProblemComment, TestCase
from classroom.models import ClassroomStudents, Classroom
from contest.models import Contest
from lab.models import Lab
from users.decorators import faculty_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
'''
    Function for Role based authorization of Problem; upon provided the pid to the request parameter 
'''


def customRoleBasedProblemAuthorization(request, problem, isItLab):
    user = request.user

    # If Faculty hasn't created classroom
    # or Student is not enrolled to the classroom
    if user.isStudent:
        try:
            if isItLab:
                classroomStudents = ClassroomStudents.objects.get(student=user, classroom=problem.lab.classroom)
            else:
                classroomStudents = ClassroomStudents.objects.get(student=user, classroom=problem.contest.classroom)
        except ObjectDoesNotExist:
            return False
    else:
        if ((isItLab and problem.lab.classroom.user != user ) or (not isItLab and problem.contest.classroom.user != user)):
            return False

    return True

'''
    Function for Role based authorization of Lab; upon provided the labId to the request parameter 
'''


def customRoleBasedLabAuthorization(request, lab):
    user = request.user

    # If Faculty hasn't created classroom
    # or Student is not enrolled to the classroom
    if user.isStudent:
        try:
            classroomStudents = ClassroomStudents.objects.get(student=user, classroom=lab.classroom)
        except ObjectDoesNotExist:
            return False
    else:
        if lab.classroom.user != user:
            return False
    return True


'''
    Function for Role based authorization of Contest; upon provided the contestId to the request parameter 
'''


def customRoleBasedContestAuthorization(request, contest):
    user = request.user

    # If Faculty hasn't created the classroom for which current contest belongs
    # or If Student is not enrolled to the classroom for which current contest belongs
    if user.isStudent:
        try:
            classroomStudents = ClassroomStudents.objects.get(student=user, classroom=contest.classroom)
        except ObjectDoesNotExist:
            return False
    else:
        if contest.classroom.user != user:
            return False
    return True

'''
    Function to get Problem based on provided pid
'''


def getProblem(request):
    try:

        # If request method is GET
        if request.method == "GET":
            pid = request.GET["pid"]
        else:
            pid = request.POST["pid"]
        problem = Problem.objects.get(problemId=pid)
        return True, pid, problem
    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        return False, None, None

'''
    Function to get Contest/Lab based on provided Id
'''


def getContestOrLab(request):
    try:
        isItLab = False
        labId = None
        contestId = None

        if request.method == "GET":
            if (request.GET.get('labId')):
                labId = request.GET["labId"]
            else:
                contestId = request.GET["contestId"]
        else:
            if (request.POST.get('contestId')):
                contestId = request.POST["contestId"]
            else:
                labId = request.POST["labId"]

        if (not labId and contestId):
            contest = Contest.objects.get(contestId=contestId)
            isItLab = False
            return True, contestId, contest, isItLab
        elif (not contestId and labId):
            lab = Lab.objects.get(labId=labId)
            isItLab = True
            return True, labId, lab, isItLab
        else:
            return False, None, None, False

    except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
        print('exception')
        return False, None, None, False


'''
    Function which will convert Django DateTime to HTML DateTime
'''


def convertDjangoDateTimeToHTMLDateTime(contest):
    # Converting Datetime field into HTML formatted string
    startTimeString = str(contest.startTime.strftime("%Y-%m-%dT%H:%M"))
    endTimeString = str(contest.endTime.strftime("%Y-%m-%dT%H:%M"))
    return startTimeString, endTimeString


'''
    Function to get all Classroom list details
'''


@login_required(login_url='/users/login')
def list(request):
    # If classroom not exist and If Classroom is not belonging to Faculty or Student
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    idName = ""
    # Problem list will be shown belonging to the particular contest or lab
    if isItLab:
        idName = "labId"
        problems = Problem.objects.filter(lab=object, doesBelongToContest=False)
    else:
        idName = "contestId"
        problems = Problem.objects.filter(contest=object,  doesBelongToContest=True)

    return render(request, 'problem/list.html', {'problems': problems, 'idName': idName, 'idValue': objectId})


'''
    Function to create Classroom
'''


@faculty_required()
def create(request):
    # If classroom not exist and If Classroom is not belonging to Faculty or Student
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    idName = ""
    if isItLab:
        idName = "labId"
    else:
        idName = "contestId"

    if request.method == 'GET':
        return render(request, 'problem/create.html', {'idName': idName, 'idValue': objectId})

    # Saving the Problem data
    title = request.POST['title']
    description = request.POST['description']
    difficulty = request.POST['difficulty']
    points = request.POST['points']
    timeLimit = request.POST['timeLimit']

    if isItLab:
        newProblem = Problem(title=title, description=description, difficulty=difficulty, points=points,
                             timeLimit=timeLimit, doesBelongToContest=False, lab=object)
    else:
        newProblem = Problem(title=title, description=description, difficulty=difficulty, points=points,
                             timeLimit=timeLimit, doesBelongToContest=True, contest=object)

    newProblem.save()
    return redirect("/problems/?" + idName + "=" + objectId)


'''
    Function to get Classroom details
'''


@login_required(login_url='/users/login')
def view(request):
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, isItLab):
        return render(request, 'accessDenied.html', {})

    idName = ""
    if isItLab:
        idName = "labId"
    else:
        idName = "contestId"
    return render(request, 'problem/view.html', {'problem': problem, 'idName': idName, 'idValue': objectId})


'''
    Function to edit the Classroom details
'''


@faculty_required()
def edit(request):
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, isItLab):
        return render(request, 'accessDenied.html', {})

    idName = ""
    if isItLab:
        problem.doesBelongToContest = False
        idName = "labId"
    else:
        problem.doesBelongToContest = True
        idName = "contestId"

    if request.method == 'GET':
        return render(request, 'problem/edit.html', {'problem': problem, 'idName': idName, 'idValue': objectId})

    # Saving the Problem data
    problem.title = request.POST['title']
    problem.description = request.POST['description']
    problem.difficulty = request.POST['difficulty']
    problem.points = request.POST['points']
    problem.timeLimit = request.POST['timeLimit']
    problem.save()
    return redirect('/problems/view?pid=' + str(problem.problemId) + "&&" + idName + "=" + objectId)

'''
    Function to delete particular Problem
'''


@faculty_required()
def delete(request):
    result, objectId, object, isItLab = getContestOrLab(request)
    if not result:
        return render(request, '404.html', {})
    if isItLab:
        if not customRoleBasedLabAuthorization(request, object):
            return render(request, 'accessDenied.html', {})
    else:
        if not customRoleBasedContestAuthorization(request, object):
            return render(request, 'accessDenied.html', {})

    # If problem not exist and If Contest/Lab is not belonging to Faculty or Student
    result, pid, problem = getProblem(request)
    if not result:
        return render(request, '404.html', {})
    if not customRoleBasedProblemAuthorization(request, problem, isItLab):
        return render(request, 'accessDenied.html', {})

    idName = ""
    if isItLab:
        problem.doesBelongToContest = False
        idName = "labId"
    else:
        problem.doesBelongToContest = True
        idName = "contestId"

    if request.method == 'GET':
        return render(request, 'problem/delete.html', {'problem': problem, 'idName': idName, 'idValue': objectId})

    problem.delete()
    return redirect('/problems?' + idName + "=" + objectId)
