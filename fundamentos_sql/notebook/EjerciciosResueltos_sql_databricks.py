# Databricks notebook source
# MAGIC %md
# MAGIC # Práctica SQL 01 — Ejercicios
# MAGIC
# MAGIC **Dataset:** tienda minorista ficticia NovaMarket · **Plataforma:** Databricks SQL (Databricks Free Edition)
# MAGIC
# MAGIC 20 ejercicios: **15 básicos** y **5 intermedios**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Objetivo de la práctica
# MAGIC
# MAGIC Practicar consultas SQL progresivas sobre un conjunto de datos relacional ficticio, usando Databricks SQL en Databricks Free Edition. Al finalizar, el estudiante deberá poder filtrar, ordenar, resumir, relacionar y analizar datos mediante consultas reproducibles.
# MAGIC
# MAGIC > **Recomendación de trabajo:** resuelve los ejercicios en orden. Los primeros quince consolidan fundamentos; los últimos cinco combinan varias tablas, agrupaciones, CTE y funciones de ventana.
# MAGIC
# MAGIC ## 2. Escenario
# MAGIC
# MAGIC La empresa ficticia **NovaMarket** vende productos de tecnología, oficina, hogar, deportes y accesorios. El dataset registra clientes, empleados, productos, pedidos, líneas de pedido y pagos realizados durante 2026. Todos los datos son inventados y se incluyen exclusivamente con fines educativos.
# MAGIC
# MAGIC ## 3. Tablas y esquema
# MAGIC
# MAGIC | Tabla | Columnas y tipos recomendados | Descripción |
# MAGIC |---|---|---|
# MAGIC | `categorias` | `category_id INT`; `category_name STRING` | Catálogo de categorías. |
# MAGIC | `clientes` | `customer_id INT`; `full_name STRING`; `email STRING`; `city STRING`; `registration_date DATE`; `segment STRING` | Clientes ficticios. |
# MAGIC | `empleados` | `employee_id INT`; `full_name STRING`; `area STRING`; `hire_date DATE` | Personal que atiende pedidos. |
# MAGIC | `productos` | `product_id INT`; `product_name STRING`; `category_id INT`; `unit_price DECIMAL(10,2)`; `stock INT`; `active BOOLEAN` | Catálogo de productos. |
# MAGIC | `pedidos` | `order_id INT`; `customer_id INT`; `employee_id INT`; `order_date DATE`; `status STRING`; `channel STRING` | Cabecera de pedidos. |
# MAGIC | `detalle_pedidos` | `order_detail_id INT`; `order_id INT`; `product_id INT`; `quantity INT`; `unit_price DECIMAL(10,2)`; `discount_pct INT` | Líneas de cada pedido. |
# MAGIC | `pagos` | `payment_id INT`; `order_id INT`; `payment_date DATE`; `payment_method STRING`; `amount DECIMAL(10,2)`; `payment_status STRING` | Pagos asociados. |
# MAGIC
# MAGIC ## 4. Relaciones entre tablas
# MAGIC
# MAGIC ```
# MAGIC categorias (1) ---- (N) productos
# MAGIC clientes   (1) ---- (N) pedidos
# MAGIC empleados  (1) ---- (N) pedidos
# MAGIC pedidos    (1) ---- (N) detalle_pedidos
# MAGIC productos  (1) ---- (N) detalle_pedidos
# MAGIC pedidos    (1) ---- (1) pagos
# MAGIC ```
# MAGIC
# MAGIC ## 5. Carga de datos
# MAGIC
# MAGIC Antes de comenzar, ejecuta el notebook **`00_ddl_carga_datos`**, que crea las 7 tablas con sus tipos de datos y carga los archivos de la carpeta `datos_txt/`.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## 0. Configuración
# MAGIC
# MAGIC Las consultas usan nombres de tablas **sin catálogo ni esquema**. Ejecuta la siguiente celda para trabajar sobre el catálogo `workspace` y el esquema `novamarket` creados en el notebook `00_ddl_carga_datos`. Si usaste otros nombres, cámbialos aquí.
# MAGIC
# MAGIC Debes ver las 7 tablas: `categorias`, `clientes`, `detalle_pedidos`, `empleados`, `pagos`, `pedidos` y `productos`.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG workspace;
# MAGIC USE SCHEMA novamarket;
# MAGIC
# MAGIC SHOW TABLES;

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## 6. Ejercicios básicos

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 1. Listado de categorías
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** SELECT
# MAGIC
# MAGIC **Pregunta:** Muestra todos los registros de la tabla `categorias`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM categorias;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 2. Columnas específicas de productos
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** SELECT de columnas
# MAGIC
# MAGIC **Pregunta:** Muestra el nombre, el precio unitario y el stock de todos los productos.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT product_name, unit_price, stock
# MAGIC FROM productos;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 3. Productos activos
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** WHERE, BOOLEAN
# MAGIC
# MAGIC **Pregunta:** Lista los productos que se encuentran activos.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM productos
# MAGIC WHERE active = TRUE;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 4. Rango de precios
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** BETWEEN
# MAGIC
# MAGIC **Pregunta:** Muestra los productos cuyo precio unitario se encuentre entre 50 y 200 soles, incluyendo ambos límites.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM productos
# MAGIC WHERE unit_price BETWEEN 50 AND 200;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 5. Clientes por ciudad
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** WHERE, IN
# MAGIC
# MAGIC **Pregunta:** Muestra los clientes que viven en Arequipa o Lima.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM clientes
# MAGIC WHERE city IN ('Arequipa', 'Lima');

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 6. Clientes registrados en un periodo
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** Fechas, BETWEEN
# MAGIC
# MAGIC **Pregunta:** Lista los clientes que se registraron durante el primer trimestre de 2026, desde el 1 de enero hasta el 31 de marzo.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM clientes
# MAGIC WHERE registration_date BETWEEN DATE'2026-01-01' AND DATE'2026-03-31';

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 7. Ciudades sin duplicados
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** DISTINCT
# MAGIC
# MAGIC **Pregunta:** Obtén la lista de ciudades distintas en las que existen clientes.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT city
# MAGIC FROM clientes
# MAGIC ORDER BY city;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 8. Productos más costosos
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** ORDER BY
# MAGIC
# MAGIC **Pregunta:** Ordena todos los productos desde el precio más alto hasta el más bajo.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM productos
# MAGIC ORDER BY unit_price DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 9. Productos con menor stock
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** ORDER BY, LIMIT
# MAGIC
# MAGIC **Pregunta:** Muestra los cinco productos con menor cantidad disponible en stock.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT product_name, stock
# MAGIC FROM productos
# MAGIC ORDER BY stock ASC
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 10. Valor del inventario
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** Columnas calculadas, alias
# MAGIC
# MAGIC **Pregunta:** Calcula el valor del inventario de cada producto multiplicando `unit_price` por `stock`. Muestra el resultado con el alias `inventory_value` y redondéalo a dos decimales.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT product_id,
# MAGIC        product_name,
# MAGIC        ROUND(unit_price * stock, 2) AS inventory_value
# MAGIC FROM productos;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 11. Cantidad total de pedidos
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** COUNT
# MAGIC
# MAGIC **Pregunta:** Cuenta cuántos pedidos existen en total.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS total_pedidos
# MAGIC FROM pedidos;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 12. Resumen de precios
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** MIN, MAX, AVG, ROUND
# MAGIC
# MAGIC **Pregunta:** Obtén el precio mínimo, el precio máximo y el precio promedio de los productos. Redondea el promedio a dos decimales.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT MIN(unit_price)           AS precio_minimo,
# MAGIC        MAX(unit_price)           AS precio_maximo,
# MAGIC        ROUND(AVG(unit_price), 2) AS precio_promedio
# MAGIC FROM productos;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 13. Productos por categoría
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** GROUP BY, COUNT
# MAGIC
# MAGIC **Pregunta:** Cuenta cuántos productos pertenecen a cada `category_id`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT category_id,
# MAGIC        COUNT(*) AS total_productos
# MAGIC FROM productos
# MAGIC GROUP BY category_id
# MAGIC ORDER BY category_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 14. Productos con nombre de categoría
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** INNER JOIN
# MAGIC
# MAGIC **Pregunta:** Muestra cada producto junto con el nombre de su categoría y su precio unitario.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT p.product_name,
# MAGIC        c.category_name,
# MAGIC        p.unit_price
# MAGIC FROM productos p
# MAGIC INNER JOIN categorias c
# MAGIC         ON p.category_id = c.category_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 15. Detalle general de pedidos
# MAGIC
# MAGIC **Nivel:** Básico &nbsp;|&nbsp; **Conceptos:** JOIN de tres tablas
# MAGIC
# MAGIC **Pregunta:** Lista cada pedido mostrando `order_id`, fecha, estado, canal, nombre del cliente y nombre del empleado responsable.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT o.order_id,
# MAGIC        o.order_date,
# MAGIC        o.status,
# MAGIC        o.channel,
# MAGIC        c.full_name AS cliente,
# MAGIC        e.full_name AS empleado
# MAGIC FROM pedidos o
# MAGIC INNER JOIN clientes  c ON o.customer_id = c.customer_id
# MAGIC INNER JOIN empleados e ON o.employee_id = e.employee_id
# MAGIC ORDER BY o.order_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## 7. Ejercicios intermedios
# MAGIC
# MAGIC > En estos ejercicios un pedido **no cancelado** es aquel cuyo `status` es distinto de `'cancelado'`.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 16. Importe neto por pedido
# MAGIC
# MAGIC **Nivel:** Intermedio &nbsp;|&nbsp; **Conceptos:** JOIN, SUM, fórmula de descuento, GROUP BY
# MAGIC
# MAGIC **Pregunta:** Calcula el importe neto de cada pedido **no cancelado**. Cada línea vale `quantity * unit_price * (1 - discount_pct / 100)`. Muestra `order_id`, cliente, fecha y `net_order_amount`, redondeado a dos decimales.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT o.order_id,
# MAGIC        c.full_name AS cliente,
# MAGIC        o.order_date,
# MAGIC        ROUND(SUM(d.quantity * d.unit_price * (1 - d.discount_pct / 100)), 2) AS net_order_amount
# MAGIC FROM pedidos o
# MAGIC INNER JOIN clientes c         ON o.customer_id = c.customer_id
# MAGIC INNER JOIN detalle_pedidos d  ON o.order_id = d.order_id
# MAGIC WHERE o.status <> 'cancelado'
# MAGIC GROUP BY o.order_id, c.full_name, o.order_date
# MAGIC ORDER BY o.order_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 17. Clientes frecuentes y su gasto
# MAGIC
# MAGIC **Nivel:** Intermedio &nbsp;|&nbsp; **Conceptos:** JOIN, GROUP BY, HAVING, COUNT DISTINCT
# MAGIC
# MAGIC **Pregunta:** Encuentra los clientes que tienen más de dos pedidos **no cancelados**. Muestra su nombre, número de pedidos y gasto neto total, ordenando desde el mayor gasto.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT c.customer_id,
# MAGIC        c.full_name AS cliente,
# MAGIC        COUNT(DISTINCT o.order_id) AS num_pedidos,
# MAGIC        ROUND(SUM(d.quantity * d.unit_price * (1 - d.discount_pct / 100)), 2) AS gasto_neto_total
# MAGIC FROM clientes c
# MAGIC INNER JOIN pedidos o         ON c.customer_id = o.customer_id
# MAGIC INNER JOIN detalle_pedidos d ON o.order_id = d.order_id
# MAGIC WHERE o.status <> 'cancelado'
# MAGIC GROUP BY c.customer_id, c.full_name
# MAGIC HAVING COUNT(DISTINCT o.order_id) > 2
# MAGIC ORDER BY gasto_neto_total DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 18. Productos nunca vendidos
# MAGIC
# MAGIC **Nivel:** Intermedio &nbsp;|&nbsp; **Conceptos:** LEFT JOIN, NULL
# MAGIC
# MAGIC **Pregunta:** Identifica los productos que nunca aparecen en `detalle_pedidos`. Muestra `product_id`, `product_name` y `category_id`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT p.product_id,
# MAGIC        p.product_name,
# MAGIC        p.category_id
# MAGIC FROM productos p
# MAGIC LEFT JOIN detalle_pedidos d
# MAGIC        ON p.product_id = d.product_id
# MAGIC WHERE d.product_id IS NULL;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 19. Ventas mensuales por canal
# MAGIC
# MAGIC **Nivel:** Intermedio &nbsp;|&nbsp; **Conceptos:** CTE, DATE_TRUNC, agregación
# MAGIC
# MAGIC **Pregunta:** Calcula las ventas netas mensuales por canal para los pedidos **no cancelados**. Muestra el mes, el canal, la cantidad de pedidos y las ventas netas.

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH ventas_pedido AS (
# MAGIC     SELECT o.order_id,
# MAGIC            DATE_TRUNC('MONTH', o.order_date) AS mes,
# MAGIC            o.channel,
# MAGIC            SUM(d.quantity * d.unit_price * (1 - d.discount_pct / 100)) AS net_order_amount
# MAGIC     FROM pedidos o
# MAGIC     INNER JOIN detalle_pedidos d ON o.order_id = d.order_id
# MAGIC     WHERE o.status <> 'cancelado'
# MAGIC     GROUP BY o.order_id, DATE_TRUNC('MONTH', o.order_date), o.channel
# MAGIC )
# MAGIC SELECT CAST(mes AS DATE)              AS mes,
# MAGIC        channel                        AS canal,
# MAGIC        COUNT(*)                       AS cantidad_pedidos,
# MAGIC        ROUND(SUM(net_order_amount), 2) AS ventas_netas
# MAGIC FROM ventas_pedido
# MAGIC GROUP BY mes, channel
# MAGIC ORDER BY mes, canal;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 20. Producto líder por categoría
# MAGIC
# MAGIC **Nivel:** Intermedio &nbsp;|&nbsp; **Conceptos:** CTE, función de ventana, DENSE_RANK
# MAGIC
# MAGIC **Pregunta:** Determina el producto o productos con mayor cantidad de unidades vendidas dentro de cada categoría, considerando solo pedidos **no cancelados**. Si existe empate, muestra todos los empatados.

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH unidades AS (
# MAGIC     SELECT c.category_name,
# MAGIC            p.product_id,
# MAGIC            p.product_name,
# MAGIC            SUM(d.quantity) AS unidades_vendidas
# MAGIC     FROM detalle_pedidos d
# MAGIC     INNER JOIN pedidos o    ON d.order_id = o.order_id
# MAGIC     INNER JOIN productos p  ON d.product_id = p.product_id
# MAGIC     INNER JOIN categorias c ON p.category_id = c.category_id
# MAGIC     WHERE o.status <> 'cancelado'
# MAGIC     GROUP BY c.category_name, p.product_id, p.product_name
# MAGIC ),
# MAGIC ranking AS (
# MAGIC     SELECT *,
# MAGIC            DENSE_RANK() OVER (PARTITION BY category_name
# MAGIC                               ORDER BY unidades_vendidas DESC) AS rk
# MAGIC     FROM unidades
# MAGIC )
# MAGIC SELECT category_name, product_id, product_name, unidades_vendidas
# MAGIC FROM ranking
# MAGIC WHERE rk = 1
# MAGIC ORDER BY category_name, product_name;

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## 8. Lista de verificación
# MAGIC
# MAGIC - [ ] Las siete tablas fueron cargadas correctamente.
# MAGIC - [ ] Las fechas se reconocen como `DATE` y los precios como valores numéricos.
# MAGIC - [ ] Los `JOIN` no generan duplicados inesperados.
# MAGIC - [ ] Los resultados intermedios fueron validados con conteos.
# MAGIC - [ ] Las consultas finales tienen alias claros y un ordenamiento útil.