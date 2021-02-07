select p1.id, p2.id, p3.id
from (SELECT pz1.id FROM PIZZAS pz1 LEFT JOIN EQUIPO_PIZZA epz1 ON pz1.id = epz1.id_pizza WHERE epz1.id_pizza is null) p1
cross join (SELECT pz2.id FROM PIZZAS pz2 LEFT JOIN EQUIPO_PIZZA epz2 ON pz2.id = epz2.id_pizza WHERE epz2.id_pizza is null) p2
cross join (SELECT pz3.id FROM PIZZAS pz3 LEFT JOIN EQUIPO_PIZZA epz3 ON pz3.id = epz3.id_pizza WHERE epz3.id_pizza is null) p3
WHERE p1.id <> p2.id AND p1.id <> p3.id AND p2.id <> p3.id
AND p2.id > p1.id 
AND p3.id > p2.id