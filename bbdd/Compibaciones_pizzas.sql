select p1.id, p2.id, p3.id
from PIZZAS p1
cross join PIZZAS p2
cross join PIZZAS p3
where p1.id <> p2.id and p1.id <> p3.id and p2.id <> p3.id
and p2.id > p1.id 
and p3.id > p2.id