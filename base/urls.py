from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, UserLoginView, UserLogoutView, user_register, TaskReorder

urlpatterns = [
    path('login', UserLoginView.as_view(), name="login"),
    path('logout', UserLogoutView.as_view(), name="logout"),
    path('register', user_register, name='register'),

    path('', TaskList.as_view(), name="tasklist"),
    path('task-detail/<int:pk>/', TaskDetail.as_view(), name="task-detail"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]
