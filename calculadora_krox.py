import streamlit as st
import time
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ecom Super Pro - Inteligência", layout="centered", page_icon="🛍️")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    .caixa-resultado { background-color: #161b22; padding: 20px; border-radius: 12px; border-left: 6px solid; margin-bottom: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3);}
    .ml { border-color: #f1c40f; } .shopee { border-color: #e67e22; } .amazon { border-color: #3498db; }
    .prejuizo-box { border-color: #ff6961; }
    .prejuizo-texto { color: #ff6961; font-weight: bold; font-size: 20px; text-align: center; margin-top: 10px; }
    .versao-software { text-align: center; color: #6e7681; font-size: 12px; margin-top: -15px; margin-bottom: 30px; font-family: monospace;}
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO MULTI-USUÁRIO ---
USUARIOS_PERMITIDOS = {
    "admin": "KROX2026",
    "ox_marketing": "SUCESSO2026",
    "vendedor_pro": "ML2026"
}

col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
st.markdown("<p class='versao-software'>v.2026.1.8 (Build PRO + Logística Individual)</p>", unsafe_allow_html=True)

col_u, col_s = st.columns(2)
user_id = col_u.text_input("Usuário:")
senha_digitada = col_s.text_input("Senha:", type="password")

if user_id not in USUARIOS_PERMITIDOS or USUARIOS_PERMITIDOS[user_id] != senha_digitada:
    if user_id != "": st.error("❌ Acesso negado.")
    st.stop()

st.success(f"🔓 Logado como: {user_id}")

# --- INPUTS DE DADOS ---
with st.form("main_form"):
    st.markdown("### 📦 1. Custos de Produto e Impostos")
    c1, c2, c3, c4 = st.columns(4)
    c_nf = c1.number_input("Custo NF R$", value=40.0)
    c_emb = c2.number_input("Embalagem R$", value=2.0)
    imp = c3.number_input("Imposto %", value=6.0)
    c_extra = c4.number_input("Outros Custos R$", value=0.0)

    st.markdown("### 🛒 2. Preço e Anúncios")
    v1, v2, v3 = st.columns(3)
    preco_v = v1.number_input("Preço de Venda R$", value=120.0)
    sh_fg = v2.checkbox("Shopee Frete Grátis (+6%)", value=True)
    ads_pct = v3.number_input("Verba Ads (%)", value=0.0)

    st.markdown("### 🚚 3. Logística Individual (Custo de Frete por Canal)")
    st.caption("Insira quanto você paga de frete em cada marketplace para este produto.")
    l1, l2, l3 = st.columns(3)
    f_ml = l1.number_input("Frete Mercado Livre R$", value=23.90 if preco_v >= 79 else 0.0)
    f_sh = l2.number_input("Frete Shopee R$", value=0.0)
    f_amz = l3.number_input("Frete Amazon R$", value=15.00)

    btn = st.form_submit_button("🚀 PROCESSAR RAIO-X FINANCEIRO", use_container_width=True)

# --- CÁLCULOS ---
if btn:
    v_imp = preco_v * (imp / 100)
    v_ads = preco_v * (ads_pct / 100)
    custo_base_operacional = c_nf + c_emb + c_extra + v_imp + v_ads

    res = {
        "Mercado Livre": {"lucro": preco_v - custo_base_operacional - (preco_v * 0.165) - (6.0 if preco_v < 79 else 0.0) - f_ml, "cor": "ml", "logo": "ml_logo.png", "comis": preco_v * 0.165, "fixa": (6.0 if preco_v < 79 else 0.0), "frete": f_ml},
        "Shopee": {"lucro": preco_v - custo_base_operacional - (preco_v * (0.26 if sh_fg else 0.20)) - 4.0 - f_sh, "cor": "shopee", "logo": "sh_logo.png", "comis": preco_v * (0.26 if sh_fg else 0.20), "fixa": 4.0, "frete": f_sh},
        "Amazon": {"lucro": preco_v - custo_base_operacional - (preco_v * 0.15) - f_amz, "cor": "amazon", "logo": "am_logo.png", "comis": preco_v * 0.15, "fixa": 0, "frete": f_amz}
    }

    cols = st.columns(3)
    for i, (nome, d) in enumerate(res.items()):
        with cols[i]:
            if os.path.exists(d["logo"]): st.image(d["logo"], width=60)
            
            if d["lucro"] > 0:
                st.markdown(f"<div class='caixa-resultado {d['cor']}'><h4>{nome}</h4><h2 style='color: #2ea043;'>R$ {d['lucro']:.2f}</h2></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='caixa-resultado prejuizo-box'><h4>{nome}</h4><h2 style='color: #ff6961;'>PREJUÍZO</h2></div>", unsafe_allow_html=True)
                if os.path.exists("dino.png"): st.image("dino.png", use_container_width=True)

            with st.expander("📊 Detalhes DRE"):
                st.write(f"Venda: R$ {preco_v:.2f}")
                st.write(f"Imposto: -R$ {v_imp:.2f}")
                st.write(f"Comissão: -R$ {d['comis']:.2f}")
                st.write(f"Frete: -R$ {d['frete']:.2f}")
                if d['fixa'] > 0: st.write(f"Taxa Fixa: -R$ {d['fixa']:.2f}")
                st.markdown(f"**Líquido: R$ {d['lucro']:.2f}**")
