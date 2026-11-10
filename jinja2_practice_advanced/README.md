# Ordering App

_Part 7_

### 1. Description

In the previous activity we implemented part of our web client. But there was a lot of copy-pasting from one template to another. If we decide to change something we will have to change it everywhere. The goal is to learn how to use macros in order to reuse functionality in different templates and how to use built-in filters.
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

### 2. Goals  

- Practice working with jinja2 macros and filters.
- Create and reuse functionality in different HTML files.
- Integrate new features to an already functional project without breaking anything.

### 3. Create macros in `macros.html`

Currently, the `header` and the `footer` are present in every HTML file in our project. Luckily they are both quite simple and we have a total of seven files so it won't be that difficult to alter them in all locations one by one. But what if we have more complex functionalities and much more files? The concept is the same as Python functions. Why write the same code in various locations when you can write it once and reuse it? This is were `macros.html` comes in. We will define all the repetitive or potentially repetitive functionality as functions in this file and just import them and use them where they are needed.

Since this file is not a template to be returned by jinja2 it does not require the typical HTML structure and you can write the macros directly. In case you choose to include it, remember that you must define the macros in the **body** part of the HTML.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <!-- macro definitions here -->
</body>
</html>
```
Macros are just like Python functions, but for HTML and with a slightly different syntax. Let's start with macros for the `header` and the `footer`. We declare a `macro` with the following syntax:
```html
{% macro *macro name*() %}
<!-- macro body -->
{% endmacro %}
```
It is like a python function declaration, but instead of *def* we use *macro*. In this case we can name them *load_header* and *load_footer*.
```html
{% macro load_header() %}
<!-- header structure  -->
{% endmacro %}
{% macro load_footer() %}
<!-- footer structure  -->
{% endmacro %}
```
We will come back to the `macros.html` to add one more later. For now we will call these two in all our templates.

### 4. Add the `macros` for the `header` and `footer` to all the templates

Before we can call the `macros` like typical Python functions in our templates we need to import them in the template. We do that in the `head` part of the HTML file. And then we can just call them like functions where we want the structure to be loaded. Do this in every template in the project.
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="../static/css/styles.css" type="text/css" rel="stylesheet">
    {% from 'macros.html' import load_header, load_footer %}
    <title>Tech Shop</title>
</head>
<body>
    {{ load_header() }}
        <!-- page structure -->
    {{ load_footer() }}
</body>
```
>Notice that we call them inside **double curly braces** and not with a *curly brace* and *percent*.

### 5. Edit the `products.html` and `single-category.html`

Both of these templates load a list of products. We can use a macro for that, but there's a difference. In `products.html` we also display the **category** of each **product**, but in `single-category.html` we just list the **products**, because we are already viewing that **category** - no need for it's name to be displayed after every **product**.

1. Let's head to the `macros.html` and create a new `macro`.
    - We can name it `load_products_table` or just `load_products` or something similar.
    - We need to pass a list of `products` to the `macro`.
    - We have two usage cases for this `macro`.
        - In the first case we want to use it to load all `products` with their respective `categories`. Here we will need all the `categories`.
        - In the second case we want to use it to load all `products` in a specific `category`. Here we do not need all the `categories` and we already have the specific one.
        - Since Jinja2 macros are essentially Python functions we can have default values for macro params. The presence of a `categories` list will be the distinguishing marker that determines if a category name is loaded or not.
    - We can add one more detail. In `single-category.html` we can add the number of products in the specific category. For that we will need the `category` itself, but since we will not need it in `products.html` we can set a default value for it as well.
    - Some `categories` might not have any `products` yet, so this is the first thing we need to check.
        - Depending on the structure and style of the page there might be different options, but we are still going for a HTML table with the `products`.
        - If there are **no** `products` in the list we are obviously dealing with `single-category.html` and that specific category is empty so we should just load the message that the `category` is empty.
        - In case the `products` list is **not** empty we would want to load them, but there's a difference between the two HTML templates.
            - In `single-category.html` we want to load a message with the number of `products` in this category.
                - Remember that we can use the `categories` list to determine whether to load the message or not.
                - We can use the built-in [length](https://tedboy.github.io/jinja2/templ14.html#length) filter on the `products` list.
                - ```
                  {{ products|length }} products in {{ category.name }}
                  ```
            - In `products.html` we skip this message.
            - In both cases we load the HTML table headers for *Name*, *Description* and *Price*.
    - At the moment we load a HTML table with the `products` in both templates and the only difference being that in the `products.html` we also load the name of the `category` for each `product`. We are going to switch it up a bit and sort the `products` by *price*.
        - In `products.html` we want to order the `products` by `category` and separate them each with a row with the category name. Meaning our table will have a row with the name of the `category` followed by the `products` only in that `category` then another row with the name of the next `category` and its `products` following and so on.
            - We can use the built-in [groupby](https://tedboy.github.io/jinja2/templ14.html#groupby) filter on the `products` list.
            - ```
              {% for cat_id, product_groups in products|groupby('category_id') %}
              ```
            - Again, the `categories` list is the determining factor for including a row in the HTML table with the *Category name*.
        - In both HTML templates we load the `products` information in a HTML table sorted by *price*.
            - We can use the built-in [sort](https://tedboy.github.io/jinja2/templ14.html#sort) filter on the `products` list.
            - ```
              {% for product in product_groups|sort(attribute='price') %}
              ```
    - The end structure of the macro should be something like this and depending on the structure and style you've chosen you can fill in the gaps:
        ```
        if products:
            if not categories:
                products|length in category.name
            Name
            Description
            Price
            for cat_id, product_groups in products|groupby('category_id'):
                if categories:
                    category.name
                for product in product_groups|sort(attribute='price'):
                    product.name
                    product.description
                    product.price
        else:
            No products in this Category
        ```
>Don't forget to end the if statements and for loops in the macro.
1. Let's use the `macro` in `products.html`.
    - Just like with the `header` and `footer` macros, we need to import this one as well.
    - Unlike the `header` and `footer` macros, here we need to pass the `products` list when we call the macro.
    - In this template we want the *category name* to be loaded so we pass the `categories` list as well.
1. Now in `single-category.html`.
    - Import the `macro`.
    - Once again we pass the list of `products` to the `macro`. The list might be empty, but that doesn't matter because the `macro` has logic to handle that.
    - We need to pass the `category` as well. You can pass arguments with keywords in Jinja2 `macros` just like with Python functions.
    - ```
      {{ load_products_table(products = products, category = category) }}
      ```
    - In this case we don't pass a list of `categories` when we call the `macro`.

