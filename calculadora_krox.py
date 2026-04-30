import streamlit as st
import pandas as pd
import time
import os
from io import BytesIO

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ecom Super Pro - Inteligência", layout="centered", page_icon="🛍️")

# --- CSS PERSONALIZADO (VISUAL DARK PREMIUM) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    .caixa-resultado { background-color: #161b22; padding: 20px; border-radius: 12px; border-left: 6px solid; margin-bottom: 10px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5);}
    .ml { border-color: #f1c40f; } .shopee { border-color: #e67e22; } .amazon { border-color: #3498db; }
    .prejuizo-box { border-color: #ff6961; }
    .prejuizo-texto { color: #ff6961; font-weight: bold; font-size: 20px; text-align: center; margin-top: 10px; }
    .versao-software { text-align: center; color: #6e7681; font-size: 12px; margin-top: -15px; margin-bottom: 30px; font-family: monospace;}
    hr { border: 0.1px solid #333; }
    div[data-testid="stExpander"] div[role="button"] p { font-weight: bold; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO (USUÁRIOS) ---
USUARIOS = {
    "admin": "KROX2026",
    "ox_marketing": "SUCESSO2026",
    "leon_secco": "PRO2026"
}

# --- CABEÇALHO ---
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center;'>ECOM SUPER</h1>", unsafe_allow_html=True)

st.markdown("<p class='versao-software'>v.2026.1.11 (Build PRO + Full DRE % + Excel)</p>", unsafe_allow_html=True)

# --- SIDEBAR LOGIN ---
st.sidebar.header("🔐 Acesso Restrito")
user_input = st.sidebar.text_input("Usuário:")
senha_input = st.sidebar.text_input("Senha:", type="password")

if user_input not in USUARIOS or USUARIOS[user_input] != senha_input:
    st.info("⬅️ Digite seu usuário e senha na barra lateral para liberar a ferramenta.")
    st.stop()

st.sidebar.success(f"Logado como: {user_input}")

# --- FORMULÁRIO DE ENTRADA ---
with st.form("form_calculadora"):
    st.markdown("### 📦 1. Custos de Origem e Operação")
    c1, c2, c3, c4 = st.columns(4)
    custo_nf = c1.number_input("Custo NF R$", value=40.0, step=1.0)
    embalagem = c2.number_input("Embalagem R$", value=2.0, step=0.5)
    imposto_pct = c3.number_input("Imposto (%)", value=6.0, step=0.5)
    custo_extra = c4.number_input("Outros Custos R$", value=0.0, step=1.0)

    st.markdown("### 🛒 2. Estratégia de Venda e Marketing")
    v1, v2, v3 = st.columns(3)
    preco_venda = v1.number_input("Preço de Venda R$", value=120.0, step=5.0)
    sh_fg_check = v2.checkbox("Participo do Frete Grátis Shopee (+6%)", value=True)
    ads_pct = v3.number_input("Verba para Ads (%)", value=0.0, step=1.0)

    st.markdown("### 🚚 3. Logística Individual (Frete Real)")
    st.caption("O sistema sugere o frete padrão, mas você pode ajustar conforme sua realidade:")
    l1, l2, l3 = st.columns(3)
    sugestao_ml = 23.90 if preco_venda >= 79 else 0.0
    frete_ml = l1.number_input("Frete Mercado Livre R$", value=sugestao_ml)
    frete_shopee = l2.number_input("Frete Shopee R$", value=0.0)
    frete_amazon = l3.number_input("Frete Amazon R$", value=15.0)

    calcular = st.form_submit_button("🚀 PROCESSAR RAIO-X FINANCEIRO", use_container_width=True)

# --- PROCESSAMENTO ---
if calcular:
    with st.spinner("Analisando taxas vigentes..."):
        time.sleep(0.8)

    # Função auxiliar para porcentagem
    def calc_pct(valor):
        return (valor / preco_venda * 100) if preco_venda > 0 else 0

    # Valores em Reais
    valor_imposto = preco_venda * (imposto_pct / 100)
    valor_ads = preco_venda * (ads_pct / 100)
    
    # Comissão Shopee
    comis_sh_pct = 26.0 if sh_fg_check else 20.0

    canais = {
        "Mercado Livre": {
            "comis_p": 16.5, 
            "comis_r": preco_venda * 0.165, 
            "fixa": 6.0 if preco_venda < 79 else 0.0, 
            "frete": frete_ml, 
            "cor": "ml", 
            "logo": "ml_logo.png"
        },
        "Shopee": {
            "comis_p": comis_sh_pct, 
            "comis_r": preco_venda * (comis_sh_pct / 100), 
            "fixa": 4.0, 
            "frete": frete_shopee, 
            "cor": "shopee", 
            "logo": "sh_logo.png"
        },
        "Amazon": {
            "comis_p": 15.0, 
            "comis_r": preco_venda * 0.15, 
            "fixa": 0.0, 
            "frete": frete_amazon, 
            "cor": "amazon", 
            "logo": "am_logo.png"
        }
    }

    cols = st.columns(3)
    dados_excel = []

    for i, (nome, d) in enumerate(canais.items()):
        # Lucro = Venda - (NF + Emb + Extra + Imp + Ads + Comis + Fixa + Frete)
        lucro = preco_venda - (custo_nf + embalagem + custo_extra + valor_imposto + valor_ads + d["comis_r"] + d["fixa"] + d["frete"])
        margem_r = calc_pct(lucro)
        
        dados_excel.append({"Canal": nome, "Preço Venda": preco_venda, "Lucro R$": round(lucro, 2), "Margem %": round(margem_r, 2)})

        with cols[i]:
            if os.path.exists(d["logo"]): st.image(d["logo"], width=65)
            
            cor_card = d["cor"] if lucro > 0 else "prejuizo-box"
            cor_fonte = "#2ea043" if lucro > 0 else "#ff6961"
            
            st.markdown(f"""
                <div class='caixa-resultado {cor_card}'>
                    <p style='margin:0;'>{nome}</p>
                    <h2 style='color: {cor_fonte}; margin:0;'>R$ {lucro:.2f}</h2>
                    <small>{margem_r:.1f}% Margem Real</small>
                </div>
            """, unsafe_allow_html=True)

            if lucro <= 0:
                st.markdown("<p class='prejuizo-texto'>NÃO VALE A PENA!</p>", unsafe_allow_html=True)
                if os.path.exists("dino.png"): st.image("dino.png", use_container_width=True)

            with st.expander("📊 DRE Completo (%)"):
                st.write(f"**(+) Preço Venda:** R$ {preco_venda:.2f} (100%)")
                st.write(f"**(-) Produto (NF):** R$ {custo_nf:.2f} ({calc_pct(custo_nf):.1f}%)")
                st.write(f"**(-) Imposto Gov:** R$ {valor_imposto:.2f} ({imposto_pct:.1f}%)")
                st.write(f"**(-) Comissão Site:** R$ {d['comis_r']:.2f} ({d['comis_p']:.1f}%)")
                st.write(f"**(-) Frete Plataforma:** R$ {d['frete']:.2f} ({calc_pct(d['frete']):.1f}%)")
                
                if d['fixa'] > 0:
                    st.write(f"**(-) Taxa Fixa Item:** R$ {d['fixa']:.2f} ({calc_pct(d['fixa']):.1f}%)")
                
                if valor_ads > 0:
                    st.write(f"**(-) Verba Ads:** R$ {valor_ads:.2f} ({ads_pct:.1f}%)")
                
                outros_total = embalagem + custo_extra
                if outros_total > 0:
                    st.write(f"**(-) Operação/Extras:** R$ {outros_total:.2f} ({calc_pct(outros_total):.1f}%)")
                
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"**(=) SOBRA NO BOLSO: R$ {lucro:.2f} ({margem_r:.1f}%)**")

    # --- EXPORTAÇÃO EXCEL ---
    st.markdown("---")
    df = pd.DataFrame(dados_excel)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='EcomSuper_Auditoria')
    
    st.download_button(
        label="📥 Baixar Auditoria em Excel (Relatório PRO)",
        data=output.getvalue(),
        file_name=f"ecom_super_relatorio_{int(time.time())}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
