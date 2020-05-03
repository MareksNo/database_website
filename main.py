from config import app
import config

from routes import HomePageView, RegistrationView, LoginView, AddProductView, LogoutView

app.add_url_rule(
    rule='//',
    view_func=HomePageView.as_view('home_page'),
)

app.add_url_rule(
    rule='/register/',
    view_func=RegistrationView.as_view('register'),
)

app.add_url_rule(
    rule='/login/',
    view_func=LoginView.as_view('login'),
)

app.add_url_rule(
    rule='/add_product/',
    view_func=AddProductView.as_view('add_product'),
)

app.add_url_rule(
    rule='/logout/',
    view_func=LogoutView.as_view('logout'),
)

if __name__ == '__main__':
    app.run(debug=True)
