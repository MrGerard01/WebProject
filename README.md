# Database and users

## Migrations

First, you need to create the database migrations by running:

```
python manage.py makemigrations
```

Then, apply the migrations to create the database schema:

```
python manage.py migrate
```

You should see a database file called `db.sqlite3`.

## Superuser

To create a superuser account for accessing the Django admin interface, run:

```
python manage.py createsuperuser
```

Once created, you can log in at: [localhost:8000/admin](http://localhost:8000/admin)

## Models

You can now modify the `web/models.py` file as you desire. For more info on what kinds of fields you can use in the models, check: [Django model fields](https://docs.djangoproject.com/en/stable/ref/models/fields/)

Don't forget to run the migrations commands so the changes take effect:

```
python manage.py makemigrations
python manage.py migrate
```

Register the new models in the admin panel by modifying the `web/admin.py` file to include them. For example, in our case it would be:

```
from .models import Author, Book, Review

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
```

# Pages and styles

Create your website templates in `web/templates`(such as `login.html`) and your styles in `web/static` (such as `style.css`).

## Templates

Django uses a template inheritance system. Here's how it works:

1. **Base template (`base.html`)**:
   - Contains the common structure (header, navigation, footer)
   - Defines blocks that child templates can override:
     ```html
     {% block title %}Library{% endblock %}
     {% block content %}{% endblock %}
     ```
   - Handles authentication display:
     ```html
     {% if user.is_authenticated %}
         <a href="{% url 'logout' %}">Logout</a>
     {% else %}
         <a href="{% url 'login' %}">Login</a>
     {% endif %}
     ```

2. **Child templates (like `login.html`)**:
   - Extend the base template:
     ```html
     {% extends 'base.html' %}
     ```
   - Override specific blocks:
     ```html
     {% block title %}Login - Library{% endblock %}
     {% block content %}
         <!-- Your login form here -->
     {% endblock %}
     ```

## Static files

1. **Loading Static Files**:
   - In templates, first load the static tag:
     ```html
     {% load static %}
     ```
   - Then reference your static files:
     ```html
     <link rel="stylesheet" href="{% static 'style.css' %}">
     ```

## Required configuration

1. **settings.py**:

We need to make sure that in `TEMPLATES` we have:

```python
TEMPLATES = [
    {
        ...
        'APP_DIRS': True,
        ...
    },
]
```

This will allow Django to locate the templates in the `web/templates` directory.

We need to set the `STATIC_URL` to `static/` and add the `STATICFILES_DIRS` to the `BASE_DIR / "web/static"` directory so that Django can find the static files in our project and in the `web/static` directory:

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "web/static",
]
```

We want the login/logout to redirect to the home page, so we set:

```python
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

2. **urls.py (project level)**:
   ```python
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('web.urls')), # this loads our 'web' app urls
   ]
   ```

This loads our 'web' app urls so we can load the urls that we will define in the `web/urls.py` file.

3. **urls.py (app level)**:

We add the desired urls to the `web/urls.py` file. The first one is the home page (root directory, aka `''`), then we will use the Django auth views for login and a custom logout view (this will be defined in the `views.py` file).

   ```python
   from django.contrib.auth import views as auth_views
   
   urlpatterns = [
       path('', views.home, name='home'),
       path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
       path('logout/', views.logout_view, name='logout'),
   ]
   ```

4. **views.py**:

We define the views for the home page and the logout view. The home page will be the default page and we should render the `home.html` template we created. The logout view will be used to log out the user and redirect to the home page, we implement this logic by using the `auth_logout` function and redirecting to the `home` url (named as such in the `web/urls.py` file):

```python
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')
```

# User registration

To add user registration functionality to our project, we do the following:

1. **Create the registration template**:
   Create `web/templates/register.html`:
   ```html
   {% extends 'base.html' %}
   {% block content %}
   <div class="login-container">
       <h1>Register</h1>
       <form method="post" class="login-form">
           {% csrf_token %}
           <!-- Form fields for username, email, and password -->
       </form>
   </div>
   {% endblock %}
   ```

2. **Add the registration view**:
   In `web/views.py`, add:
   ```python
   from django.contrib.auth.forms import UserCreationForm
   from django.contrib import messages

   def register(request):
       if request.method == 'POST':
           form = UserCreationForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect('login')
       else:
           form = UserCreationForm()
       return render(request, 'register.html', {'form': form})
   ```

3. **Add URL for registration**:
   In `web/urls.py`, add:
   ```python
   path('register/', views.register, name='register'),
   ```

4. **Update the navigation bar**:
   In `base.html`, add register link for non-authenticated users:
   ```html
   {% if not user.is_authenticated %}
       <a href="{% url 'register' %}">Register</a>
   {% endif %}
   ```

5. **Add form styles**:
   In `style.css`, add styles for form links and messages, i.e.:
   ```css
   .form-link {
       margin-top: 1rem;
       text-align: center;
   }
   ```

# Books page (or any other DB element) with database interaction

To create a page that displays books from our database (only for logged-in users), we'll follow these steps:

1. **Create the template**:
   In our case, we create `web/templates/books.html` with a basic structure:
   ```html
   {% extends 'base.html' %}
   {% block title %}Books - Library{% endblock %}

   {% block content %}
   <div class="books-container">
       <h1>Our Books</h1>
       {% if books %}
           <div class="books-grid">
               <!-- Books will be displayed here -->
           </div>
       {% else %}
           <p class="no-books">No books available at the moment.</p>
       {% endif %}
   </div>
   {% endblock %}
   ```

2. **Create the protected view**:
   In `web/views.py`, add a view that queries the database:
   ```python
   from django.contrib.auth.decorators import login_required
   from .models import Book # we import the Book model

   @login_required
   def books(request):
       # Using select_related for efficient querying of foreign keys
       books = Book.objects.select_related('author').all()
       return render(request, 'books.html', {'books': books})
   ```

3. **Add URL pattern**:
   In `web/urls.py`, connect the view:
   ```python
   path('books/', views.books, name='books'),
   ```

4. **Update navigation**:
   In `base.html`, add the books link for authenticated users:
   ```html
   {% if user.is_authenticated %}
       <a href="{% url 'books' %}">Books</a>
   {% endif %}
   ```

5. **Complete the template with database fields**:
   Update the books template to iterate over the DB books and display the desired fields:
   ```html
   {% for book in books %}
       <div class="book-card">
           <h2>{{ book.title }}</h2>
           <p class="author">by {{ book.author.name }}</p>
           {% if book.co_authors.exists %}
               <p class="co-authors">
                   Co-authors: 
                   {% for co_author in book.co_authors.all %}
                       {{ co_author.name }}{% if not forloop.last %}, {% endif %}
                   {% endfor %}
               </p>
           {% endif %}
           <p class="book-details">
               <span class="category">{{ book.get_category_display }}</span>
               <span class="pages">{{ book.page_count }} pages</span>
           </p>
           <p class="price">${{ book.price }}</p>
           <div class="book-footer">
               <span class="availability {% if book.in_stock %}available{% else %}unavailable{% endif %}">
                   {% if book.in_stock %}In Stock{% else %}Out of Stock{% endif %}
               </span>
               <span class="isbn">ISBN: {{ book.isbn }}</span>
           </div>
       </div>
   {% endfor %}
   ```

6. **Add styling**:
   In `style.css`, style the book cards and grid, i.e.:
   ```css
   .books-grid {
       display: grid;
       grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
       gap: 2rem;
   }

   .book-card {
       background: white;
       border-radius: 8px;
       padding: 1.5rem;
       box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
   }
   ```
