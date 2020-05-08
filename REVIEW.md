# Code review


### ticketing/settings.py

`23:` ```SECRET_KEY = '$!=n6m1w4@4m150d0w(++hye!ndv4v-l6o$u7y4v7r4l*-pu#j'```

This poses a security risk it would be much safer to fetch the key from environmental variable and leave the current value as 
default if it is not present on the host like so:

```SECRET_KEY = os.getenv('SECRET_KEY',default='$!=n6m1w4@4m150d0w(++hye!ndv4v-l6o$u7y4v7r4l*-pu#j)'```


---
### ticketing/url.py
```python
urlpatterns = [
    url('getOrders/(?P<user_id>[0-9]*)', views.getOrders),
    url('users/', views.get_users),
    url('update-user', views.update_user),
]
```

##### Issue 1
`6:` ```url('getOrders/(?P<user_id>[0-9]*)', views.getOrders)```

This is an old syntax for catching parameters I think it would make the code more readable if we express the parameter type clearly:

```url('getOrders/<int:user_id>', views.getOrders),```

##### Issue 2 URI names

URI names in REST architecture should not contain verbs so a proper resource URI should be
```url('orders/(?P<user_id>[0-9]*)', views.getOrders)```

Also there seems to be a lack of general naming convention as camel case and spinal case is used in URI naming. I would opt for
using snake casing but either is fine just need to stick to one (on personal note not a big fan of camel casing in URI).

#### Issue 3
This is not a RESTful approach `url('update-user', views.update_user),`  I would suggest changing it to
`url('update-user/<int:user_id>/', views.update_user),`
 



---
### ticketing/views.py

#### Line 7 `getOrders(request, user_id)`:
```python
@api_view(['GET', 'POST', 'PUT']) # Too many methods declared
def getOrders(request, user_id): #def getOrders(request, user_id=None):
    if user_id == '': # if user_id is None:
        orders = OrderSerializer(Order.objects.all(), many=True) #prefetch_related
    elif user_id != '': # else:
        orders = OrderSerializer(Order.objects.filter(user_id=user_id), many=True) #prefetch_related
    for order in orders.data:
        order['user'] = UserSerializer(User.objects.get(id=order['user_id'])).data
    return Response(orders.data)
```
- This endpoint consumes only `GET` in the current state sending `POST` or `PUT` will result in `HTTP_200`. Also `OPTIONS` request
will confuse API users as it will show `POST` and `PUT` as valid
 - There seems to be a lack of handling of nonexistent object. Querying with nonexistent `user_id` returns empty list not 404 is this on purpose?
 - I would suggest a default value for `user_id` this would nicely change the `if ... elif` statement, example follows:
 ```python
 if user_id is None:
        orders = OrderSerializer(Order.objects.all(), many=True) 
 else:
        orders = OrderSerializer(Order.objects.filter(user_id=user_id), many=True) 
```
 
 **Current**
```SQL
(0.000) SELECT "ticketing_api_order"."id", "ticketing_api_order"."user_id" FROM "ticketing_api_order"; args=()
(0.000) SELECT "ticketing_api_ticket"."id", "ticketing_api_ticket"."name", "ticketing_api_ticket"."price", "ticketing_api_ticket"."reward_points" FROM "ticketing_api_ticket" INNER JOIN "ticketing_api_order_tickets" ON ("ticketing_api_ticket"."id" = "ticketing_api_order_tickets"."ticket_id") WHERE "ticketing_api_order_tickets"."order_id" = 1; args=(1,)
(0.000) SELECT "ticketing_api_ticket"."id", "ticketing_api_ticket"."name", "ticketing_api_ticket"."price", "ticketing_api_ticket"."reward_points" FROM "ticketing_api_ticket" INNER JOIN "ticketing_api_order_tickets" ON ("ticketing_api_ticket"."id" = "ticketing_api_order_tickets"."ticket_id") WHERE "ticketing_api_order_tickets"."order_id" = 2; args=(2,)
(0.000) SELECT "ticketing_api_user"."id", "ticketing_api_user"."name", "ticketing_api_user"."points" FROM "ticketing_api_user" WHERE "ticketing_api_user"."id" = 1 LIMIT 21; args=(1,)
(0.000) SELECT "ticketing_api_user"."id", "ticketing_api_user"."name", "ticketing_api_user"."points" FROM "ticketing_api_user" WHERE "ticketing_api_user"."id" = 2 LIMIT 21; args=(2,)

```
**With `OrderSerializer(Order.objects.filter(user_id=user_id).prefetch_related('tickets'), many=True)`**
```SQL
(0.000) SELECT "ticketing_api_order"."id", "ticketing_api_order"."user_id" FROM "ticketing_api_order"; args=()
(0.000) SELECT ("ticketing_api_order_tickets"."order_id") AS "_prefetch_related_val_order_id", "ticketing_api_ticket"."id", "ticketing_api_ticket"."name", "ticketing_api_ticket"."price", "ticketing_api_ticket"."reward_points" FROM "ticketing_api_ticket" INNER JOIN "ticketing_api_order_tickets" ON ("ticketing_api_ticket"."id" = "ticketing_api_order_tickets"."ticket_id") WHERE "ticketing_api_order_tickets"."order_id" IN (1, 2); args=(1, 2)
(0.000) SELECT "ticketing_api_user"."id", "ticketing_api_user"."name", "ticketing_api_user"."points" FROM "ticketing_api_user" WHERE "ticketing_api_user"."id" = 1 LIMIT 21; args=(1,)
(0.015) SELECT "ticketing_api_user"."id", "ticketing_api_user"."name", "ticketing_api_user"."points" FROM "ticketing_api_user" WHERE "ticketing_api_user"."id" = 2 LIMIT 21; args=(2,)
```
 This difference will increase with the number of orders
 
-
#### Line 21 `def get_users(request)`:

```python
@api_view(['GET', 'POST', 'PUT']) # Too many methods declared
def get_users(request):
    response = []

    for user in User.objects.all():
        response.append({
            'id': user.id,
            'name': user.name,
            'points': user.points,
        })

    return Response(response) # Response(UserSerializer(User.objects.all(),many=True).data)
```
- Same as in `getOrders(request, user_id)` `POST` and `PUT` should be removed
- There is already a `UserSerializer` which should be used for consistency and the whole function will become a oneliner


#### Line 34 `update_user(request):`
```python
@api_view(['POST'])
def update_user(request):
    user = User.objects.get(id=request.data['user_id'])
    user.points += request.data['add_points']
    user.save()

    return Response({})
```
 - There is no handling for nonexistent user_id `POST` for such IDs will cause `Server Error 500`
 - I would also suggest returning the new `User` or at least `user.points` instead of empty dict
 - If we are sticking with returning an empty dict status code should be changed to `204 No Content`
 
 ---
### ticketing/serializers.py

Just a general note. Is there any particular reason why `serializers.Serializers` where used instead of `serializers.ModelSerializer`?

---
### ticketing/ticketing_api/management/commands/setup_data.py

Just a side note `factory_boy` is an awesome library for `Model` test data generation
 