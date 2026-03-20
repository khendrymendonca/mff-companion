-- Tabela de Tiers com Prioridade (Poder)
CREATE TABLE meta_tiers (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    priority INTEGER NOT NULL DEFAULT 1 -- 1: Usar primeiro (Fraco), 10: Poupar (Forte)
);

-- Inserir Tiers Atuais com escalas de prioridade
INSERT INTO meta_tiers (name, priority) VALUES 
('T1', 1), 
('T2', 2), 
('Transcended', 3), 
('T3', 4), 
('T4', 5);
