from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View

from django.apps import apps
from courses.forms import ModuleFormSet
from courses.models import Course, Module, Content


class CreateCourse(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'subject', 'slug', 'overview', 'course_image']
    template_name = 'courses/create_course.html'
    permission_required = 'courses.add_course'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'courses/update_course.html'
    model = Course
    login_url = reverse_lazy('users:login')
    raise_exception = True
    context_object_name = 'course'
    permissions_required = 'courses.change_course'
    fields = ['title', 'subject', 'slug', 'overview', 'course_image']
    success_url = reverse_lazy('home')


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    permission_required = 'courses.delete_course'
    template_name = 'courses/delete_course.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('users:login')


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/add_modules_course.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('home')
        return self.render_to_response({'course': self.course, 'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/module_contents.html'
    module = None
    model = None
    obj = None

    @staticmethod
    def get_model(model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    @staticmethod
    def get_form(model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)

        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            if not id:
                Content.objects.create(module=self.module, item=obj)

            return redirect('courses:course-detail', self.module.id)

        return self.render_to_response({'form': form, 'object': self.obj})
