from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    
    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.IndexView, name='index'),
    path(route='addreview/', view=views.AddReviewView, name='addreview'),
    path(route='dealer_details/', view=views.DealerDetailsView, name='dealer_details'),
    path(route='registration/', view=views.RegistrationView, name='registration'),
    path(route='about_us/', view=views.AboutUsView, name='about_us'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))