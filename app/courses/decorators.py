from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from app.courses.models import Course, Enrollment


def enrollment_required(view_func):
    def _wrapper(request, *args, **kwargs):
        slug = kwargs['slug']
        course = get_object_or_404(Course, slug=slug)
        has_permission = request.user.is_staff
        if not has_permission:
            try:
                enrollment = Enrollment.objects.get(
                    user=request.user, course=course
                )
            except Enrollment.DoesNotExists:
                message = 'Desculpe, você não tem permissão'
            else:
                if enrollment.is_approved():
                    has_permission = True
                else:
                    message = 'Sua inscrição no curso ainda está pendente'
        if not has_permission:
            messages.error(request, message)
            return redirect('dashboard')
        request.course = course
        return view_func(request, *args, **kwargs)
    return _wrapper
