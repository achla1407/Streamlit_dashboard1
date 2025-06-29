-- SELECT * FROM  summerproject
--units sold region_wise
SELECT
  region,
  SUM(units_sold) AS total_sold
FROM
  summerproject
GROUP BY
  region
ORDER BY
  total_sold DESC;
 --stock_level calculation Across ALL stores 
 SELECT
  store_id,
  SUM(inventory_level) AS total_stock
FROM
  summerproject
GROUP BY
  store_id
ORDER BY
  total_stock DESC;
--REorder point
WITH store_thresholds AS (
  SELECT
    store_id,
    percentile_cont(0.10) 
      WITHIN GROUP (ORDER BY inventory_level) 
      AS p10_threshold
  FROM summerproject
  GROUP BY store_id
)
SELECT
  s.store_id,
  s.product_id,
  s.inventory_level,
  t.p10_threshold
FROM
  summerproject AS s
  JOIN store_thresholds AS t
    ON s.store_id = t.store_id
WHERE
  s.inventory_level <= t.p10_threshold
ORDER BY
  s.store_id,
  s.inventory_level;
---Stock out rates


  



 
