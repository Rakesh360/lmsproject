from django.urls import path
from . import views

urlpatterns = [
    #API
    path('macleods-signup/', views.MacleodsSignUp, name="macleods-signup-api"),

    path('', views.HomePage),
    path('logout/', views.UserLogout, name="user-logout"),
    # Applicants
    path('login/', views.ApplicantLoginPage, name="applicant-login"),
    path('signup/', views.ApplicantSignupPage, name="applicant-signup-page"),
    path('applicant/verify', views.ApplicantVerification,name='applicant-verification-api'),
    path('applicant/signup', views.ApplicantSignUp, name="applicant-signup-api"),
    path('applicant/signup/success', views.ApplicantSignUpSuccess,name="signup-success-page"),
    path('authenticate-applicant/', views.ApplicantAuthentication,name="applicant-authentication-api"),
    path('applicant/dashboard/', views.ApplicantDashboard,name='applicant-dashboard'),
    path('forgot-password', views.ForgotPasswordPage, name='forgot-password'),
    path('reset-password/<int:phone_number>',views.ResetPassword, name="reset-password-api"),
    # Edit Applicants
    path('master-list/edit-applicants/', views.EditApplicantsPage),
    
    path('master-list/get-applicant-quiz/', views.GetApplicantQuizzes),
    path('master-list/update-applicant-task/', views.UpdateApplicantTask),
    path('administrator/update-applicant-profile/', views.UpdateApplicantProfile),

    # Manager
    path('administrator/login/', views.AdministratorLoginPage,name="administrator-login-page"),
    path('authenticate-administrator/', views.AdministratorAuthentication,name="administrator-authentication-api"),
    path('administrator/manage-applicants/',views.ManageApplicantsPage, name='manage-applicants-page'),
    path('administrator/assign-task/', views.AssignTask, name="task-assign-api"),
    path('administrator/accepted-applicant/',views.AcceptedApplicant, name="accepted-applicant-api"),
    path('administrator/rejected-applicant/',views.RejectedApplicant, name="rejected-applicant-api"),
    path('administrator/reset-applicant-account/',views.ResetApplicantAccount, name="reset-applicant-account-api"),
    path('administrator/applicant-report-card/<int:applicant_pk>/',views.ApplicantReportCard),
    path('administrator/quiz-result/',views.GetQuizResult, name="quiz-result-api"),
    path('administrator/deassigned-quiz-result/' , views.GetDeassignedResultAPI , name="GetDeassignedResultAPI"),

    #path('administrator/deactivate-institute/', views.DeactivateInstitute),
    #path('administrator/activate-institute/', views.ActivateInstitute),
    path('administrator/download-applicant-report/', views.DownloadApplicantReport),
    path('administrator/save-applicant-at-irecruit/', views.SaveApplicantAtIRecruit),
    path('administrator/deactivate-administrator/', views.DeactivateAdministrator),
    path('administrator/activate-administrator/', views.ActivateAdministrator),
    path('administrator/deactivate-event/', views.DeactivateEvent),
    path('administrator/activate-event/', views.ActivateEvent),
    path('administrator/download-event-excel/', views.DownloadEventExcel),
    # Institute Master
    #path('master-list/institutes/', views.MasterInstitutes,name='master-list-institutes'),
    #path('master-list/add-institutes/',views.AddMasterInstitutes, name='add-institutes'),
    path('master-list/create-applicants/',views.MasterApplicants, name='add-institutes'),
    path('master-list/create-applicants-excel/',views.CreateApplicantExcel, name="create-applicants-excel"),
    path('master-list/streams/', views.MasterStreams,name='master-list-stream'),
    path('master-list/add-streams/',views.AddMasterStreams, name='add-stream'),
    path('master-list/delete-stream/',views.DeleteMasterStreams, name='delete-stream'),
    path('master-list/create-administrator/',views.MasterAdministrator, name='master-administrator'),
    path('master-list/create-new-administrator/',views.CreateAdministrator, name='create-administrator'),
    path('master-list/events/', views.MasterEvents,name='master-list-event'),
    path('master-list/add-events/',views.AddMasterEvents, name='add-event'),
    path('master-list/delete-events/',views.DeleteMasterEvents, name='delete-event'),
    path('master-list/departments/', views.MasterDepartments,name='master-list-department'),
    path('master-list/add-departments/',views.AddMasterDepartments, name='add-department'),
    path('master-list/delete-departments/',views.DeleteMasterDepartments, name='delete-department'),
    path('get-quiz-section-list/', views.GetQuizSectionList, name='get-quiz-section-list'),
    path('master-list/edit-events/',views.EditMasterEvents, name='edit-event'),


    path('master-list/tags/', views.MasterTags, name='master-list-tag'),
    path('master-list/save-tag/', views.SaveTag, name='master-list-save-tag'),
    path('manage-quiz/change-topic-tag/', views.ChangeTopicTag),
    path('administrator/assign-tag/', views.AssignTag, name="tag-assign-api"),  

    # Quiz
    path('manage-quiz/', views.ManageQuiz, name="manage-quiz"),
    path('manage-quiz/add-quiz/', views.AddQuizConfig, name="add-quiz-api"),
    path('manage-quiz/delete-quiz/', views.DeleteQuiz, name="delete-quiz-api"),
    path('manage-quiz/topics/', views.ManageTopics, name="manage-topics-page"),
    path('manage-quiz/topic/<int:topic_pk>', views.RenderTopicProblem),
    path('manage-quiz/add-topic/', views.AddTopic, name="add-topic-api"),
    path('manage-quiz/delete-topic/', views.DeleteTopic, name="delete-topic-api"),
    path('manage-quiz/rename-topic/', views.RenameTopic, name="rename-topic-api"),
    path('manage-quiz/problem/add/', views.AddProblem),
    path('manage-quiz/problem/edit/<int:problem_pk>', views.EditProblem),
    path('manage-quiz/save-problem/', views.SaveProblem),
    path('manage-quiz/topic/upload-questions-excel/',views.UploadQuestionsExcel, name="upload-questions-excel"),
    path('manage-quiz/delete-problem/<int:topic_pk>',views.DeleteProblem, name="delete-problem"),
    path('manage-quiz/quiz/edit/<int:quiz_config_pk>', views.RenderQuizConfig),
    path('manage-quiz/add-quiz-section/',views.AddQuizSection, name="add-quiz-section-api"),
    path('manage-quiz/delete-quiz-section/<int:quiz_section_pk>/',views.DeleteQuizSection, name="delete-quiz-section-api"),
    path('manage-quiz/save-quiz-config/', views.SaveQuizConfig),
    path('manage-quiz/get-text-analysis-attempted-problem/', views.GetTextAnalysisOfAttemptedProblem),
    path('manage-quiz/save-topic-category/', views.SaveTopicCategory),
    path('manage-quiz/toggle-problem-visibility/', views.ToggleProblemVisibility, name="toggle-problem-visibility-api"),

    path('manage-quiz/deactivate-quiz/', views.DeactivateQuiz),
    path('manage-quiz/activate-quiz/', views.ActivateQuiz),

    path('manage-quiz/deactivate-topic/', views.DeactivateTopic),
    path('manage-quiz/activate-topic/', views.ActivateTopic),

    path('manage-quiz/copy-quiz/', views.CopyQuizContent),
    path('manage-quiz/topic/import-topic-questions/', views.ImportTopicQuestions, name="import-topic-questions"),

    #Quiz Paper
    path('applicant/get-quiz-config/', views.GetQuizConfig),
    path('applicant/get-quiz-section/', views.GetQuizSection),
    path('applicant/quiz-paper/<uuid:quiz_uuid>', views.QuizPaper),
    path('applicant/start-test/<uuid:quiz_uuid>', views.StartTestPage),
    path('applicant/fetch-next-problem/',views.FetchNextProblem, name="fetch-next-problem-api"),
    path('applicant/test-complete/', views.TestComplete, name="test-complete-api"),
    path('applicant/sync-remaining-quiz-time/',views.SyncRemainingQuizTime, name="quiz-time-sync-api"),
    path('applicant/save-screenshots/', views.SaveApplicantScreenShot,name="save-applicant-screenshots"),
    path('administrator/save-remarks/',views.SaveRemarks, name="save-remarks-api"),
    path('manage-quiz/save-modified-descriptive-score/',views.SaveModifiedScoreOfAttemptedProblem),
    path('applicant/save-video/',views.SaveApplicantVideo,name="save-video"),

    path('applicant/save-logout-time/', views.SaveQuizReloadTime),

    #Sign-up Events filter with category: Campus, Walkin etc
    path('get-event-list/', views.GetEventList),

    #### Downloading Complete Database 
    path('master-list/database/', views.GetDatabasePage),
    path('administrator/download-database/', views.DownloadDatabaseExcel),

    #### Downlaod Question Bank topic wise

    path('manage-quiz/get-topic-problem-excel/', views.GetTopicProblemExcel),

]

