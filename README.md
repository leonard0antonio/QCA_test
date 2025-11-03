# 📊 Coleta de Dados IBGE (Playwright)

Projeto automatizado para coletar informações do site do **IBGE** sobre todos os estados do Brasil, extraindo dados de:

- **População**
- **Educação**
- **Economia**
- **Trabalho e Rendimento**
- **Território**

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **Playwright**
- **Pandas**
- **OpenPyXL**

---

## 🚀 Como Executar

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/leonard0antonio/QCA_test.git
   cd QCA_test
   ```
2. **Crie o ambiente virtual e instale as dependências:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   playwright install chromium
   ```
3.**Execute o script principal:**
   ```bash
   python src/main.py
   ````
4.**Saída dos dados:**
```bash
data/estados_info_detalhado.xlsx
````

---

## 📝 Observações

O script utiliza o navegador Chromium via Playwright.

Todos os 27 estados brasileiros (incluindo o Distrito Federal) são contemplados.

As seções “Saúde” e “Meio Ambiente” não estão explicitamente disponíveis no site do IBGE na aba “Panorama”, portanto não foi possível coletar essas informações.

Não é utilizada nenhuma API — apenas automação web e extração de dados direta do site do IBGE.

---

## 📎 Links para Teste
- [Repositório GitHub:](https://github.com/leonard0antonio/QCA_test)
- [Planilha Gerada (Google Sheets):](https://docs.google.com/spreadsheets/d/1Du5ZDtIN1MHhyHSNPfDJ_IN5Ln1I9PrO/edit?usp=sharing&ouid=118133169166389818601&rtpof=true&sd=true
)  
