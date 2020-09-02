"""Themis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.viewsstatic import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from tool import views
from tool.auto_login_app import AutoAppLogin
from tool.push_k2_workflow import ChangeK2TravelWorkflowStatus, ChangeK2SupplierWorkflowStatus

urlpatterns = [
    url(r'^toolpage', views.ToolPage, name="tool"),
    url(r'^AutoAppLogin', AutoAppLogin.as_view(), name="AutoAppLogin"),
    url(r'^ChangeK2TravelWorkflowStatus', ChangeK2TravelWorkflowStatus.as_view(), name="ChangeK2TravelWorkflowStatus"),  # 修改考察状态
    url(r'^ChangeK2SupplierWorkflowStatus', ChangeK2SupplierWorkflowStatus.as_view(), name="ChangeK2SupplierWorkflowStatus"),  # 修改考察状态

]
