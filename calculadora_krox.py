import streamlit as st
import time
import os
import pandas as pd
from io import BytesIO

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Ecom Super Pro - Inteligência", layout="centered", page_icon="🛍️")

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    .caixa-resultado { background-color: #161b22; padding: 20px; border-radius: 12px; border-left: 6px solid; margin-bottom: 10px; text-align: center;}
    .ml { border-color: #f1c40f; } .shopee { border-color: #e67e22; } .amazon { border-color: #3498db; }
    .prejuizo-box { border-color: #ff6961; }
    .versao-software { text-align: center; color: #6e7681; font-size: 12px; margin-bottom: 20px; font-family: monospace;}
    hr { border: 0.1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
USUARIOS = {"admin": "KROX2026", "ox_marketing": "SUCESSO2026"}

col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
st.markdown("<p class='versao-software'>v.2026.1.10 (PRO + Full DRE %)</p>", unsafe_allow_html=True)

u = st.sidebar.text_input("Usuário:")
s = st.sidebar.text_input("Senha:", type="password")

if u not in USUARIOS or USUARIOS[u] != s:
    st.info("⬅️ Digite as credenciais na barra lateral para aceder ao sistema.")
    st.stop()

# --- INPUTS ---
with st.form("main_form"):
    st.markdown("### 📦 1. Custos e Operação")
    c1, c2, c3, c4 = st.columns(4)
    c_nf = c1.number_input("Custo NF R$", value=40.0)
    c_emb = c2.number_input("Embalagem R$", value=2.0)
    imp_p = c3.number_input("Imposto %", value=6.0)
    c_ext = c4.number_input("Outros Custos R$", value=0.0)

    st.markdown("### 🛒 2. Venda e Marketing")
    v1, v2, v3 = st.columns(3)
    preco_v = v1.number_input("Preço de Venda R$", value=120.0)
    sh_fg = v2.checkbox("Shopee Frete Grátis (+6%)", value=True)
    ads_p = v3.number_input("Verba Ads (%)", value=0.0)

    st.markdown("### 🚚 3. Logística (Cálculo Automático + Edição)")
    st.caption("O sistema sugere o frete padrão, mas podes ajustar o valor real abaixo:")
    l1, l2, l3 = st.columns(3)
    # Cálculo automático sugerido para facilitar a vida do lojista
    sugestao_ml = 23.90 if preco_v >= 79 else 0.0
    f_ml = l1.number_input("Frete M. Livre R$", value=sugestao_ml)
    f_sh = l2.number_input("Frete Shopee R$", value=0.0)
    f_amz = l3.number_input("Frete Amazon R$", value=15.0)

    btn = st.form_submit_button("🚀 PROCESSAR ALGORITMO DE LUCRO", use_container_width=True)

if btn:
    v_imp = preco_v * (imp_p / 100)
    v_ads = preco_v * (ads_p / 100)
    
    sh_comis_p = 26.0 if sh_fg else 20.0
    
    canais = {
        "Mercado Livre": {"p": 16.5, "comis": preco_v * 0.165, "fixa": 6.0 if preco_v < 79 else 0.0, "frete": f_ml, "cor": "ml", "logo": "ml_logo.png"},
        "Shopee": {"p": sh_comis_p, "comis": preco_v * (sh_comis_p/100), "fixa": 4.0, "frete": f_sh, "cor": "shopee", "logo": "sh_logo.png"},
        "Amazon": {"p": 15.0, "comis": preco_v * 0.15, "fixa": 0.0, "frete": f_amz, "cor": "amazon", "logo": "am_logo.png"}
    }

    cols = st.columns(3)
    dados_export = []

    for i, (nome, d) in enumerate(canais.items()):
        # Cálculos de Lucro
        custo_total_item = c_nf + c_emb + c_ext + v_imp + v_ads + d["comis"] + d["fixa"] + d["frete"]
        lucro = preco_v - custo_total_item
        margem = (lucro / preco_v * 100) if preco_v > 0 else 0
        
        # Guardar para Excel
        dados_export.append({"Canal": nome, "Venda": preco_v, "Lucro": lucro, "Margem %": round(margem, 2)})

        with cols[i]:
            if os.path.exists(d["logo"]): st.image(d["logo"], width=60)
            
            cor_txt = "#2ea043" if lucro > 0 else "#ff6961"
            status = d["cor"] if lucro > 0 else "prejuizo-box"
            
            st.markdown(f"<div class='caixa-resultado {status}'><h4>{nome}</h4><h2 style='color: {cor_txt};'>R$ {lucro:.2f}</h2><small>{margem:.1f}% Margem Real</small></div>", unsafe_allow_html=True)
            
            if lucro <= 0 and os.path.exists("dino.png"): st.image("dino.png", use_container_width=True)

            with st.expander(f"📊 DRE Completo (%)"):
                # Função para calcular % do preço de venda
                def pct(valor):
                    return (valor / preco_v * 100) if preco_v > 0 else 0

                st.write(f"**(+) Preço Venda:** R$ {preco_v:.2f} (100%)")
                st.write(f"**(-) Produto (NF):** R$ {c_nf:.2f} ({pct(c_nf):.1f}%)")
                st.write(f"**(-) Imposto:** R$ {v_imp:.2f} ({imp_p:.1f}%)")
                st.write(f"**(-) Comissão Site:** R$ {d['comis']:.2f} ({d['p']:.1f}%)")
                st.write(f"**(-) Frete Real:** R$ {d['frete']:.2f} ({pct(d['frete']):.1f}%)")
                
                if d['fixa'] > 0:
                    st.write(f"**(-) Taxa Fixa:** R$ {d['fixa']:.2f} ({pct(d['fixa']):.1f}%)")
                
                if v_ads > 0:
                    st.write(f"**(-) Marketing/Ads:** R$ {v_ads:.2f} ({ads_p:.1f}%)")
                
                custos_operacionais = c_emb + c_ext
                if custos_operacionais > 0:
                    st.write(f"**(-) Operação/Extras:** R$ {custos_operacionais:.2f} ({pct(custos_operacionais):.1f}%)")
                
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"**(=) SOBRA LÍQUIDA: R$ {lucro:.2f} ({margem:.1f}%)**")

    # --- BOTÃO EXPORTAR ---
    st.markdown("---")
    df = pd.DataFrame(dados_export)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Auditoria_Financeira')
    
    st.download_button(
        label="📥 Descarregar Relatório Detalhado (Excel)",
        data=output.getvalue(),
        file_name=f"ecom_super_auditoria.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
