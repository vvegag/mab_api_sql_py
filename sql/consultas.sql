-- Consulta de agregação usada para alimentar o cálculo de recomendação.
SELECT
    v.nome_variante,
    COALESCE(SUM(CASE WHEN e.tipo_evento = 'impressao' THEN 1 ELSE 0 END), 0) AS impressos,
    COALESCE(SUM(CASE WHEN e.tipo_evento = 'clique' THEN 1 ELSE 0 END), 0) AS cliques
FROM variantes v
LEFT JOIN eventos_brutos e
    ON e.id_variante = v.id_variante
   AND e.id_experimento = v.id_experimento
   AND e.timestamp_evento >= :data_inicio
   AND e.timestamp_evento <= :data_base
WHERE v.id_experimento = :id_experimento
GROUP BY v.nome_variante
ORDER BY v.nome_variante;
