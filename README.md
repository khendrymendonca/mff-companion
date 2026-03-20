# MFF Companion - Shadowland Master

Um assistente web para Marvel Future Fight focado em gestão de recursos e otimização da Terra das Sombras (Shadowland).

## 🚀 Como Rodar Localmente

1.  **Clone o projeto e entre na pasta:**
    ```bash
    cd mff_companion
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute o servidor:**
    ```bash
    uvicorn api.index:app --reload
    ```
    Acesse: `http://127.0.0.1:8000`

## ☁️ Deploy na Vercel

O projeto já está configurado para a Vercel. Basta conectar seu repositório GitHub na plataforma e as configurações no `vercel.json` farão o resto.

## 🗄️ Configuração do Supabase

1.  Crie um projeto no Supabase.
2.  Execute o script `supabase_schema.sql` no Editor SQL.
3.  Copie a URL e a KEY do projeto para o arquivo `.env` (use o `.env.example` como base).

## 🛠️ Tecnologias Utilizadas

- **Python (FastAPI):** Backend de alta performance.
- **Jinja2:** Templates HTML dinâmicos.
- **Tailwind CSS:** Design visual premium e responsivo.
- **Supabase:** Banco de dados e autenticação.
- **Vercel:** Hospedagem Serverless.
