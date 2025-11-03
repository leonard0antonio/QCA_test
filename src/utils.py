import pandas as pd
import os
from datetime import datetime
import re

def converter_valor_para_numero(secao, valor):
    """Tenta converter o valor em número, se aplicável à seção."""
    try:
        if secao in ["População", "Educação", "Economia"]:
            # Remove espaços e caracteres estranhos
            valor_limpo = str(valor).strip()

            # Remove símbolos e letras
            valor_limpo = re.sub(r"[^0-9,.\-]", "", valor_limpo)

            if not valor_limpo:
                return valor  # nada pra converter

            # Corrige formato BR → padrão float
            # Exemplo: "1.271 R$" → "1271"
            # Exemplo: "830.018" → "830018"
            # Primeiro, se tiver mais de um ponto, assume que são milhares
            partes_ponto = valor_limpo.split(".")
            if len(partes_ponto) > 1:
                # Junta os milhares e mantém só a parte decimal, se houver
                valor_limpo = "".join(partes_ponto[:-1]) + "." + partes_ponto[-1]

            valor_limpo = valor_limpo.replace(",", ".")
            return float(valor_limpo)
        else:
            return valor
    except:
        return valor

def salvar_em_excel(dados):
    """Reorganiza os dados coletados e salva em um Excel no formato:
    Estado | Seção | Título | Valor
    """
    linhas = []

    for estado_info in dados:
        estado = estado_info.get("Estado", "Desconhecido")

        for secao, conteudo in estado_info.items():
            if secao == "Estado":
                continue

            if isinstance(conteudo, dict):
                for titulo, valor in conteudo.items():
                    valor_convertido = converter_valor_para_numero(secao, valor)
                    linhas.append({
                        "Estado": estado,
                        "Seção": secao,
                        "Título": titulo,
                        "Valor": valor_convertido
                    })
            else:
                valor_convertido = converter_valor_para_numero(secao, conteudo)
                linhas.append({
                    "Estado": estado,
                    "Seção": secao,
                    "Título": "",
                    "Valor": valor_convertido
                })

    if not linhas:
        print("⚠️ Nenhuma linha foi gerada. Verifique se os dados estão corretos.")
        return

    df = pd.DataFrame(linhas)

    # garante que o diretório data existe
    pasta_data = os.path.join(os.getcwd(), "data")
    os.makedirs(pasta_data, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    caminho_arquivo = os.path.join(pasta_data, f"estados_info_detalhado_{timestamp}.xlsx")

    df.to_excel(caminho_arquivo, index=False)
    print(f"✅ Dados salvos em: {caminho_arquivo}")
