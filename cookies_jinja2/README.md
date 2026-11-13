# Ordering App

_Part 8_

### 1. Description

In the previous activity we implemented part of our web client. But there was a lot of copy-pasting from one template to another. If we decide to change something we will have to change it everywhere. Also we are missing functionality for *login* and *register*. The goal is to add a *users router* that accepts data from our web client, learn how to reuse stuff from one template and how to make global functionality for all templates without having to pass it as *context* for each template.
The *Ordering app* api has its functionality already implemented:

- Product endpoints:
    - ✔ GET /api/products (*with optional query params*)
    - ✔ GET /api/products/{id}
    - ✔ POST /api/products
    - ✔ PUT /api/products/{id}
- Order endpoints:
    - ✔ GET /api/orders (*with optional query params*)
    - ✔ GET /api/orders/{id}
    - ✔ POST /api/orders
    - ✔ PUT /api/orders/{id}
    - ✔ DELETE /api/orders/{id}
    - ✔ PUT /api/orders/{id}/products
    - ✔ DELETE /api/orders/{id}/products
- Category endpoints:
    - ✔ GET /api/categories
    - ✔ GET /api/categories/{id}
    - ✔ POST /api/categories
- User Endpoints:
    - ✔ POST /api/users/login
    - ✔ GET /api/users/info
    - ✔ POST /api/users/register
    - ✔ GET /api/users/info

Web client functionality:

- Home endpoint:
    - ✔ GET / -> Serve index.html
- Product endpoints:
    - ✔ GET /products -> Serve products.html
    - ✔ GET /products/{id} -> Serve single-product.html
- Category endpoints:
    - ✔ GET /categories -> Serve categories.html 
    - ✔ GET /categories/{id} -> Serve single-category.html
- Missing functionality:
    - ✖ GET /users/login -> Serve login.html
    - ✖ POST /users/login -> Handle login data
    - ✖ POST /users/logout -> Handle logout
    - ✖ GET /users/register -> Serve register.html
    - ✖ POST /users/register -> Handle register data
    - ✖ GET /users/info -> Serve users.html
    - ✖ POST /users/delete -> Deletes a user

### 2. Goals  

- Practice working with jinja2 macros, custom jinja2 templates (not refering to HTML templates) and handle input from the client.
- Write the front-end router and change the existing HTML templates to fit the project.
- Integrate new features to an already functional project without breaking anything.

### 3. Add a `GET` `/users/login` endpoint

The api doesn't need a `GET` endpoint for this, but our *web client* needs one for our user to be able to input his/her login data. Just make the *users_router* and add this endpoint. You can name the function *serve_login*. It needs to return the `login.html` template.

### 4. Add a `POST` `/users/login` endpoint

This endpoint is not going to be very different from the one in the *api*.

Since we are accepting the login data from a *HTML Form* we need to use the **Form(...)** method from *FastAPI* for each of the fields.
```py
@users_router.post('/login')
def login(request: Request, username: str = Form(...), password: str = Form(...)):
```
If all is well with the login data we can create a token for the user and attach it as a cookie to a **RedirectResponse** and *return* that.
```py
response = RedirectResponse(url='/', status_code=302)
response.set_cookie('token', token)
```
But if the login fails we need to tell the user somehow that he/she has entered incorrect data. We can do that by modifying the `login.html` to display a "Wrong username or password!" message in case of an error. We will add that to the `login.html` later.

### 5. Add a `POST` `/users/logout` endpoint

This endpoint only needs to delete the cookie with the token and redirect the user back to the home page.

### 6. Add a `GET` `/users/register` endpoint

The api doesn't need a `GET` endpoint for this, but our *web client* needs one for our user to be able to input his/her register data. Just add this endpoint to the router. It is basically the same as the *login* one, but returns the `register.html` template.

### 7. Add a `POST` `/users/register` endpoint

This one is very similar to the `POST` `/users/login` endpoint, but here we need to try and create a new user instead of checking if the login data is correct.
- If the user is successfully created we can set the *token* as a *cookie* and *redirect* the user to the *home page*.
- The only reason for the register to fail (in this app) is if the username is taken. Same as before, we need to inform the user somehow.
>Note: Some sites redirect the user to the *login page* or require an email confirmation before the user can *log in*. In that case this enpoint doesn't need to attach the *token* as a cookie, but for our purposes this will work.

### 8. Add a `GET` `/users/info` endpoint

This endpoint is typically for a user to be able to view their info (e.g. name, address, orders, etc.) but for the purposes of this activity we won't go in so much details.

- Check if the request has a valid *token* and if so return `users.html`.
    - `users.html` will just have the same fields like the `login` and `register` pages, but the button will say "DELETE".
- If there isn't a *token* in the request cookies redirect the user to the `login` page.

### 9. Add a `POST` `/users/delete` endpoint

This endpoint probably looks wrong. If you are thinking that it should just be a `DELETE` HTTP verb you are correct. However HTML does **NOT** support HTTP verbs other than `GET` and `POST`. There are many workarounds (most modern websites use JavaScript), but in a pure HTML way we just use `POST` and alter the endpoint route.

- Users aren't typically deleted from a database, but for this activity we will delete some newly-created users. If you try to delete any of the existing users the database will raise an error, because of the foreign keys. There is no need to try and fix this. The focus of this activity is different.
- Extract a *token* from the request.
    - If there is one, get the user from the token.
    - If not, redirect the user to the `login` page.
- Compare the user's username and password to the ones entered by the user.
    - If they match delete the user, delete the cookie and redirect the user to the `home` page.
    - If not return an error message that they don't match.

### 10. Create `CustomJinja2Templates` class

We have already made a new function in the `auth.py` file named `get_user_if_token` that uses the `from_token` function in `users_service.py` and works with the `Request` object. Also the `from_token` function has been changed so it returns a `User` if the token is valid and `None` if it is not. In the `common` folder of the app you can find a new file named `template_config.py`.

Create a **CustomJinja2Templates** class that inherits **Jinja2Templates**. In the **__init__** of the class we need to use the **super().__init__** and pass the `directory` in which our templates are when we create the `templates` instance. After that we can add functions to the global env of the template engine.
```py
class CustomJinja2Templates(Jinja2Templates):
def __init__(self, directory: str):
    super().__init__(directory=directory)
    self.env.globals['get_user'] = get_user_if_token
```
Now we can access this function in any template without having to pass it or it's result as context in the `endpoints` of the `routers`. We access it by the name we have given it in the *square brackets* and not the name after the *equals* sign. Also notice that we simply give the name of the function without *braces* after it. Remember when we added python functions to dictionaries earlier in the program? This way we skip the need to have to get the `user` in every `endpoint` in every `router` in order to load the `header` correctly.

Whenever there's something we need in every, or almost every template we can add it to these `globals` and use it without having to pass it as `context` to the template.

You can add the `categories_dict` function from the `category_service` if you want, since we use them in multiple places. You can move it to the `template_config.py` file or straight up get it from the service.

### 11. Edit `macros.html`

We will have to edit the `header` to show the `Login` and `Register` links only if the user is not logged in. If he/she is logged in we can show a *Hello, 'username'* link that leads to `info` about the user and a `Logout` button. Also, the `login.html`, `register.html` and `users.html` all load the two fields for *username* and *password* and a button, which only differs in the text it has. We can use a *macro* for that.

- First, we can modify the `header` `macro`.
    - In order for the `header` to "know" what to display it needs to "know" if a user is logged in or not. We need to edit it so it accepts a `user` as a parameter.
    - Since `login.html` and `register.html` only apply when there isn't a logged in user it is assumed that there won't be a token in the request and that step can be skipped. That means that the `user` parameter for the `header` macro shouldn't be mandatory and can have a default value.
    - In case there is an active user the `header` should display "Hello, username" and "Logout".
        - "Hello, username" leading to `/users/info`.
        - "Logout" leading to `/users/logout`.
    - In case there isn't an active user the `header` should display "Login" and "Register".
- Now let's make the `macro` for the user input fields.
    - You can name it something like `load_user_data_fieldsets` or something similar.
    - The three pages load a field for `username`, a field for `password` and a button to submit the form.
        - The two fields are the same in all three.
        - The button varies in text and if you want you can style it a bit different (e.g. red text as a warning).
        - How can the `button` "know" what text to display?
    - What if a user enters wrong authentication information when trying to log in? Can we display an error message just in that case?
    - What if a user tries to register with an already taken username? Can we display an error message just in that case?

### 12. Edit all templates to call the `header` macro correctly

Unlike `macros` we don't need to import globals into the template.
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="../static/css/styles.css" type="text/css" rel="stylesheet">
    {% from 'macros.html' import load_header, load_footer %}
    <title>Tech Shop</title>
</head>
<body>
    {{ load_header(get_user(request)) }}
        <!-- page structure -->
    {{ load_footer() }}
</body>
```
>Note: Here we pass, to the `load_header`, the `get_user` function (which is actually the `get_user_if_token` function from the `common/auth.py` file) that we added to the global env in the `CustomJinja2Templates` class. But that function requires the `Request` object to work. Where does that object come from?

We can do this in all of the templates except the `login.html` and `register.html`, because if the `user` is on one of those pages he/she obviously isn't logged in and we can simply call the `macro` without passing anything to it (remember we made it so the user has a default value).

>Note: Someone can still access those pages even if he/she is logged in if he/she types the URL directly. We can handle that with simple logic in those `endpoints` of the router to redirect them to another page when there's a valid `token`, but that is not important now.

### 13. Edit the `login.html`, `register.html` and `users.html`

- We should call the `macro` in these and pass to it the text for the button and an error message.
    - The `endpoints` can pass an `error` message as context to the template in case there is one.
        - In case of wrong user authentication data.
        - In case the username is already taken when registering.
        - In case the username and password don't match the user from the token when attempting to delete a user.
    - Everything else is essentially identical in these three templates and an argument can be made for them to just be one template, but although HTML is not a programming language, sticking to the single responsibility principle is still good. If in the future each of these templates offers more specific functionality it would be easy to just add it to the specific template.
    
>Note: Remember that at the moment you can only delete new users (users that don't have orders), because of the database. Don't try and fix this at this point, just register a new user and then delete it.