-- Tabela de Personagens Base (Global)
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    base_type TEXT NOT NULL, -- Combat, Blast, Speed, Universal
    base_alignment TEXT NOT NULL, -- Hero, Villain, Neutral
    abilities TEXT[] -- ['Weapon', 'Agility', etc]
);

-- Tabela de Inventário do Usuário
CREATE TABLE user_inventory (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    character_id INTEGER REFERENCES characters(id),
    current_tier TEXT DEFAULT 'T1',
    level INTEGER DEFAULT 60,
    is_used BOOLEAN DEFAULT FALSE,
    UNIQUE(user_id, character_id)
);

-- Inserir alguns personagens de exemplo
INSERT INTO characters (name, base_type, base_alignment) VALUES
('Capitão América', 'Combat', 'Hero'),
('Homem de Ferro', 'Blast', 'Hero'),
('Thanos', 'Universal', 'Villain'),
('Duende Verde', 'Speed', 'Villain'),
('Magneto', 'Blast', 'Villain');
