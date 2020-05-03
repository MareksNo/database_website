from config import app
import config

from routes import (
    HomePageView,
    RegistrationView,
    LoginView,
    AddProductView,
    LogoutView,
    DisplayProductView,
    SearchProductView,
)

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

app.add_url_rule(
    rule='/product/<int:product_id>',
    view_func=DisplayProductView.as_view('display_product'),
)

app.add_url_rule(
    rule='/product/<search_name>',
    view_func=SearchProductView.as_view('search_product'),
)

if __name__ == '__main__':
    app.run(debug=True)
