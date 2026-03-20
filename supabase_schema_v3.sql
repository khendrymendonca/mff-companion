-- Atualizar tabela de personagens com detalhes granulares
ALTER TABLE characters ADD COLUMN gender TEXT DEFAULT 'Male'; -- Male, Female, Other
ALTER TABLE characters ADD COLUMN tags TEXT[] DEFAULT '{}'; -- ['Weapon', 'Spider', 'Agility']

-- Limpar e recriar tabela de andares para suportar múltiplas salas
DROP TABLE IF EXISTS sl_floors CASCADE;
CREATE TABLE sl_rooms (
    id SERIAL PRIMARY KEY,
    floor_number INTEGER NOT NULL,
    room_name TEXT NOT NULL, -- Ex: Relay, Rumble, Boss
    req_type TEXT DEFAULT 'Any',
    req_alignment TEXT DEFAULT 'Any',
    req_gender TEXT DEFAULT 'Any',
    req_tags TEXT[] DEFAULT '{}',
    notes TEXT
);

-- Indexar para busca rápida
CREATE INDEX idx_rooms_floor ON sl_rooms(floor_number);
