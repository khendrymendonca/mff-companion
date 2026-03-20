-- Tabelas de Metadados Dinâmicos
CREATE TABLE meta_types (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE meta_alignments (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE meta_genders (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL);
CREATE TABLE meta_tags (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL);

-- Inserir dados iniciais para você não começar do zero
INSERT INTO meta_types (name) VALUES ('Combat'), ('Blast'), ('Speed'), ('Universal');
INSERT INTO meta_alignments (name) VALUES ('Hero'), ('Villain'), ('Neutral');
INSERT INTO meta_genders (name) VALUES ('Male'), ('Female'), ('Other');
INSERT INTO meta_tags (name) VALUES ('Weapon'), ('Agility'), ('Spider-Sense'), ('Strong');
