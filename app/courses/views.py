from django.shortcuts import render, redirect
from .models import Course, Enrollment, Annoucement, Lesson, Material
from django.shortcuts import render, get_object_or_404
from .forms import ContactCourse, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import enrollment_required


def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {"courses": courses}
    return render(request, template_name, context)


def details(request, slug):  # detalhar o curso buscado na primeira página / detalhe a ser configurado
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context["course"] = course
    context["form"] = form
    template_name = 'courses/details.html'
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        enrollment.active()
        messages.success(request, "Inscrição Realizada com Sucesso")
    else:
        messages.info(request, 'Você já está inscrito neste Curso')
    return redirect('dashboard')


@login_required
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course
        )
        if not enrollment.is_approved():
            messages.error(request, 'Sua inscrição ainda está pendente')
            return redirect('dashboard')
    template_name = 'courses/announcements.html'
    context = {"course": course, "announcements": course.announcements.all()}
    return render(request, template_name, context)


@login_required
@enrollment_required
def undo_enrollment(request, slug):
    course = request.course
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, "Inscrição Cancelada!")
        return redirect('dashboard')
    template_name = 'courses/undo_enrollment.html'
    context = {"enrollment": enrollment, "course": course}
    return render(request, template_name, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk, *args, **kwarg):
    course = request.course
    if not enrollment.is_approved():
        messages.error(request, 'Sua inscrição ainda está pendente')
        return redirect('dashboard')
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Comentário Enviado!')
    template_name = 'courses/show_announcements.html'
    context = {"course": course, "announcements": announcement, "form": form}
    return render(request, template_name, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    template_name = 'courses/lessons.html'
    context = {'course': course, 'lessons': lessons}
    return render(request, template_name, context)


@login_required
@enrollment_required
def lesson(request, slug, pk, *args, **kwargs):
    course = request.course
    material = get_object_or_404(Material, pk=pk,
                                 lesson__course=course
                                 )
    if not request.user.is_staff and not lesson.is_available:
        messages.error(request, 'Aula Indisponível')
        return redirect('lessons')
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Aula não disponível')
        return redirect('lessons', slug=course.slug)
    if not material.is_embedded():
        return redirect(material.file.url)
    template_name = 'courses/lesson.html'
    context = {'course': course, 'lesson': lesson, 'material': material}
    return render(request, template_name, context)
