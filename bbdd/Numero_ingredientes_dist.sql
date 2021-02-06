select count(distinct pi1.id_ingrediente)
from pizza_ing pi1
where pi1.id_pizza in (0,2,4)
