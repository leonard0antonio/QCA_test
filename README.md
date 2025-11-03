# Coleta de Dados IBGE (Playwright)

Projeto automatizado para coletar informações do IBGE sobre todos os estados do Brasil,
extraindo dados de **População**, **Educação**, **Economia**, **Trabalho e Rendimento** e **Território**.

## 🧰 Tecnologias
- Python 3.10+
- Playwright
- Pandas
- OpenPyXL

## 🚀 Como executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/coleta-ibge.git
   cd coleta-ibge

2. Crie o ambiente virtual e instale as dependências:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  playwright install chromium

3. Execute o script principal:
 ```bash
  python src/main.py

4. A planilha será salva automaticamente em:
 data/estados_info_detalhado.xlsx
