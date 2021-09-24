from django.urls import path,include
from .views import HomePageView,IndexPageView, KmlCreatorView, DataManView,exportview, exportsite, \
                uploadsiteview,uploadsectorview,uploadtableview, UploadingView,runqueryview, cleartableview, showtablesview, \
                exportkml,upfileview, colorview,colorviewsec, createkmlview, clearmapview, downkml,creatingview,upfieldview,filterview,MapView,powerBIreportView

urlpatterns = [
                path('kmlcreator/', KmlCreatorView.as_view(), name='kmlcreator'),
                path('datamanagment/', DataManView.as_view(), name='datamanagment'),
                path('', HomePageView.as_view(),name='home'),
                path('mapview', MapView.as_view(),name='mapview'),
                path('login/', include('django.contrib.auth.urls')),
                path('index/', IndexPageView.as_view(), name='index'),
                path('downloadsec/',exportview,name='exportsec'),
                path('downloadsit/',exportsite,name='exportsit'),
                path('uploadsit/',uploadsiteview,name='uploadsit'),
                path('uploadsec/',uploadsectorview,name='uploadsec'),
                path('uploadtab/',uploadtableview,name='uploadtab'),
                path('loading/',UploadingView.as_view(),name='loading'),
                path('report/',powerBIreportView.as_view(),name='report'),
                path('runquery/',runqueryview,name='runquery'),
                path('cleartb/',cleartableview,name='cleartb'),
                path('lsttb/',showtablesview,name='lsttb'),
                path('exportkml/',exportkml,name='exportkml'),
                path('downkml/',downkml,name='downkml'),
                path('upfile/',upfileview,name='upfile'),
                path('colorsite/',colorview,name='colorsite'),
                path('colorsector/',colorviewsec,name='colorsector'),
                path('kmlgenerator/',createkmlview,name='kmlgenerator'),
                path('clearmap/',clearmapview,name='clearmap'),
                path('creatingviews/',creatingview,name='creatingviews'),
                path('fltables/',upfieldview,name='fltables'),
                path('filtertbl/',filterview,name='filtertbl'),
                 ]

# urlpatterns contém a lista de roteamentos de URLs
