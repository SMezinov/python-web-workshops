<img src="https://webassets.telerikacademy.com/images/default-source/logos/telerik-academy.svg" alt="logo" width="300px" style="margin-top: 20px;"/>

# Ordering App

_Part 5_

### 1. Description
The Ordering app has some of its functionality already implemented
- Product endpoints:
    - ✔ GET /products (*with optional query params*)
    - ✔ GET /products/{id}
    - ✔ POST /products
    - ✔ PUT /products/{id}
- Order endpoints:
    - ✔ GET /orders (*with optional query params*)
    - ✔ GET /orders/{id}
    - ✔ POST /orders
    - ✔ PUT /orders/{id}
    - ✔ DELETE /orders/{id}
    - ✔ PUT /orders/{id}/products
    - ✔ DELETE /orders/{id}/products
- Category endpoints:
    - ✔ GET /categories
    - ✔ GET /categories/{id}
    - ✔ POST /categories
- User Endpoints:
    - ✔ POST /users/login
    - ✔ GET /users/info
    - ✖ POST /users/register
    - ✖ GET /users/info

- Missing functionality:
    - Web client (*will be added later by the Frontend team*)
    - Console client (*will be added later by whoever is available*)


### 2. Goals  
- Practice working with users
- Rewrite the user_service to work with mariadb
- Integrate new features to an already functional project without breaking anything

### 3. Alter the database schema
Currently, users data resides in-memory in the `data.in_memory_users` module. Create `users` table in the relational db to persist that data
1. Determine the required columns
2. Consider adding passwords, which should be stored in db
    - passwords are best stored as hashes for security reasons. Although this is a course project and security isn't a priority, you can optionally take a look at the `hashlib` module for cryptographic password hashing. We repeat, this is optional. 
3. Determine the `users` -> `orders` relation. The `orders` table may also require changes.
    - if you change the `orders` table, the Order model in the application might also have to change to accommodate for new or deleted columns.

### 4. Rewrite the `user_service`
Change the functions' implementation to query the database. 
- Start function by function and make sure they no longer use the orders imported list from the in-memory module. 
- After you have refactored a function, use the global search to determine where it is used. Manually test the code paths to ascertain that no existing functionality is broken.
- After all functions are rewritten, delete the `data.in_memory_users` module as users data should now reside in the database.

### 5. Add a `POST` `/users/register` endpoint
- Refactor the LoginData model to also accept a password field. 
    - Think about suitable validation.
- Create the endpoint in the users_router and add a function in the users_service that will save the user data to the database. 
    - Decide if you would prefer to hash the password.
    - Use `customer` for default role.

### 6. Refactor the `POST` `/users/login` endpoint
- Now that we register users with passwords, we need to refactor this endpoint to also accept passwords from the HTTP request body
- The users_service function that determines if logindata is correct should also change to work with username/password combinations.
    - If you store the passwords as hashes in the DB, you will need to also hash the input password, else the login attempt will always fail.

### 7. Add a `GET` `/users/orders` endpoint
- Create this endpoint to return all orders for the authenticated user
- This endpoint should accept no parameters except tht `x-token` header with the authentication info.

### 8. Make sure the orders functionality is not broken
- The new relation `users` -> `orders` may have lead to problems in the orders service and router
- Manually test all the affected endpoints to find if any problems exist

