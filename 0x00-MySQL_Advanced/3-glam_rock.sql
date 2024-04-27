-- LSQL script that lists all bands with Glam rock as their main style

SELECT band_name, COALESCE(split, 2022) - formed as lifespan
FROM metal_bands
WHERE style like '%Glam rock%';
