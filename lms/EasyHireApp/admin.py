from django.contrib import admin

# Register your models here.
from EasyHireApp.models import *




class QuizHistoryAdmin(admin.ModelAdmin):
    list_display = ('quiz_name', 'is_blank', )
    #search_fields = ('username', )

admin.site.register(QuizHistory,QuizHistoryAdmin)

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('username', 'email_id', )
    search_fields = ('username', )



admin.site.register(Stream)
admin.site.register(Institute)
admin.site.register(Topic)
admin.site.register(Problem)
admin.site.register(Quiz)

class QuizStatusAdmin(admin.ModelAdmin):
    search_fields = ('applicant__name','applicant__email_id','applicant__phone_number')
    readonly_fields = ('assigned_date',)
    def get_queryset(self, request):
        return self.model.admin_objects.get_queryset()

admin.site.register(QuizStatus, QuizStatusAdmin)

admin.site.register(QuizSection)

class ProblemAttemptedAdmin(admin.ModelAdmin):
    readonly_fields = ('get_duration',)
    def get_queryset(self, request):
        return self.model.admin_objects.get_queryset()

admin.site.register(ProblemAttempted, ProblemAttemptedAdmin)

class QuizSectionResultAdmin(admin.ModelAdmin):
    search_fields = ('applicant__name','applicant__email_id','applicant__phone_number')
    readonly_fields = ('get_duration',)
    def get_queryset(self, request):
        return self.model.admin_objects.get_queryset()

admin.site.register(QuizSectionResult, QuizSectionResultAdmin)

class QuizResultAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.admin_objects.get_queryset()

admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(AppConfig)
admin.site.register(IdentityProof)
admin.site.register(Department)
admin.site.register(Event)
admin.site.register(VideoBatchProcessingTime)
