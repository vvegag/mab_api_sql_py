-- Schema principal do desafio: experimento, variantes, eventos brutos, agregados e recomendacoes.
CREATE TABLE IF NOT EXISTS experimentos (
    id_experimento BIGSERIAL PRIMARY KEY,
    codigo_experimento VARCHAR(120) NOT NULL UNIQUE,
    nome_experimento VARCHAR(255) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Variantes concorrentes do experimento, incluindo o controle.
CREATE TABLE IF NOT EXISTS variantes (
    id_variante BIGSERIAL PRIMARY KEY,
    id_experimento BIGINT NOT NULL,
    nome_variante VARCHAR(120) NOT NULL,
    eh_controle BOOLEAN NOT NULL DEFAULT FALSE,
    metadata_variante JSONB NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_variantes_experimentos FOREIGN KEY (id_experimento) REFERENCES experimentos(id_experimento),
    CONSTRAINT uq_variante_experimento_nome UNIQUE (id_experimento, nome_variante)
);

-- Histórico linha a linha dos eventos recebidos pela API.
CREATE TABLE IF NOT EXISTS eventos_brutos (
    id_evento BIGSERIAL PRIMARY KEY,
    id_experimento BIGINT NOT NULL,
    id_variante BIGINT NOT NULL,
    tipo_evento VARCHAR(30) NOT NULL,
    timestamp_evento TIMESTAMP NOT NULL,
    usuario_id VARCHAR(120) NULL,
    contexto JSONB NULL,
    id_evento_externo VARCHAR(120) NULL UNIQUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_eventos_experimentos FOREIGN KEY (id_experimento) REFERENCES experimentos(id_experimento),
    CONSTRAINT fk_eventos_variantes FOREIGN KEY (id_variante) REFERENCES variantes(id_variante)
);

-- Visão consolidada por dia e variante para agilizar a recomendação.
CREATE TABLE IF NOT EXISTS agregados_diarios (
    id_agregado BIGSERIAL PRIMARY KEY,
    id_experimento BIGINT NOT NULL,
    id_variante BIGINT NOT NULL,
    data_referencia TIMESTAMP NOT NULL,
    impressos INTEGER NOT NULL DEFAULT 0,
    cliques INTEGER NOT NULL DEFAULT 0,
    atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_agregados_experimentos FOREIGN KEY (id_experimento) REFERENCES experimentos(id_experimento),
    CONSTRAINT fk_agregados_variantes FOREIGN KEY (id_variante) REFERENCES variantes(id_variante),
    CONSTRAINT uq_agregado_diario UNIQUE (id_experimento, id_variante, data_referencia)
);

-- Registro auditável das alocações calculadas pelo algoritmo.
CREATE TABLE IF NOT EXISTS recomendacoes_diarias (
    id_recomendacao BIGSERIAL PRIMARY KEY,
    id_experimento BIGINT NOT NULL,
    data_referencia TIMESTAMP NOT NULL,
    metodo VARCHAR(120) NOT NULL,
    payload_json JSONB NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recomendacoes_experimentos FOREIGN KEY (id_experimento) REFERENCES experimentos(id_experimento)
);

-- Índices para acelerar os joins e as consultas temporais.
CREATE INDEX IF NOT EXISTS idx_variantes_experimento ON variantes (id_experimento);
CREATE INDEX IF NOT EXISTS idx_eventos_experimento_timestamp ON eventos_brutos (id_experimento, timestamp_evento);
CREATE INDEX IF NOT EXISTS idx_eventos_variante_timestamp ON eventos_brutos (id_variante, timestamp_evento);
CREATE INDEX IF NOT EXISTS idx_agregados_experimento_data ON agregados_diarios (id_experimento, data_referencia);
