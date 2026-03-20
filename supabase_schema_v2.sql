-- Tabela de Andares da Shadowland
CREATE TABLE sl_floors (
    id SERIAL PRIMARY KEY,
    floor_number INTEGER UNIQUE NOT NULL,
    room_name TEXT NOT NULL,
    req_type TEXT, -- Combat, Blast, Speed, Universal, etc.
    req_alignment TEXT, -- Hero, Villain
    notes TEXT
);

-- Tabela de Histórico (Para saber quem você usou na semana passada)
CREATE TABLE sl_history (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    floor_number INTEGER,
    character_id INTEGER REFERENCES characters(id),
    week_start DATE DEFAULT CURRENT_DATE
);

-- Adicionar coluna de 'Last Floor' no Inventário para facilitar a consulta
ALTER TABLE user_inventory ADD COLUMN last_floor_used INTEGER DEFAULT 0;
