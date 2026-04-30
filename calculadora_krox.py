import streamlit as st
import time
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ecom Super Pro - Inteligência", layout="centered", page_icon="🛍️")

# --- CSS PERSONALIZADO (DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #c9d1d9; }
    .caixa-resultado { background-color: #161b22; padding: 20px; border-radius: 12px; border-left: 6px solid; margin-bottom: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.3);}
    .ml { border-color: #f1c40f; } .shopee { border-color: #e67e22; } .amazon { border-color: #3498db; }
    .prejuizo-box { border-color: #ff6961; }
    .prejuizo-texto { color: #ff6961; font-weight: bold; font-size: 20px; text-align: center; margin-top: 10px; }
    .versao-software { text-align: center; color: #6e7681; font-size: 12px; margin-top: -15px; margin-bottom: 30px; font-family: monospace;}
    div[data-testid="stExpander"] div[role="button"] p { font-weight: bold; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN COM LOGO ---
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center;'>ECOM SUPER</h1>", unsafe_allow_html=True)

st.markdown("<p class='versao-software'>v.2026.1.6 (Build PRO + Smart Ads) - Licença Ativa</p>", unsafe_allow_html=True)

senha = st.text_input("Chave de Segurança:", type="password", placeholder="Digite KROX2026")
if senha != "KROX2026":
    if senha != "": st.error("❌ Chave inválida ou expirada.")
    st.stop()

# --- INPUTS DE DADOS ---
with st.form("main_form"):
    st.markdown("### 📦 1. Custos de Origem e Operação")
    c1, c2, c3, c4 = st.columns(4)
    c_nf = c1.number_input("Custo NF R$", value=40.0)
    c_emb = c2.number_input("Embalagem R$", value=2.0)
    imp = c3.number_input("Imposto %", value=6.0)
    c_extra = c4.number_input("Outros Custos R$", value=0.0, help="Taxas extras, brindes, etc.")

    st.markdown("### 🛒 2. Estratégia de Venda")
    v1, v2 = st.columns(2)
    preco_v = v1.number_input("Preço de Venda R$", value=120.0)
    sh_fg = v2.checkbox("Shopee Frete Grátis (+6%)", value=True)

    f_ml = 0.0
    if preco_v >= 79:
        st.warning("⚠️ ML: Preço acima de R$ 79 exige frete por sua conta.")
        f_ml = st.number_input("Custo do Frete ML R$", value=23.90)

    st.markdown("### 📢 3. Tráfego Pago (Ads)")
    a1, a2, a3 = st.columns(3)
    verba_ads = a1.number_input("Verba Total da Campanha R$", value=0.0, help="Ex: R$ 100 por dia")
    vendas_estimadas = a2.number_input("Vendas Esperadas (Unid.)", value=1, min_value=1, help="Quantas unidades espera vender com essa verba?")
    
    # Exibe o CPA provisório na tela para o usuário ter noção
    cpa_estimado = verba_ads / vendas_estimadas if vendas_estimadas > 0 else 0
    a3.info(f"Custo por Venda (CPA): **R$ {cpa_estimado:.2f}**")

    btn = st.form_submit_button("🚀 PROCESSAR ALGORITMO FINANCEIRO", use_container_width=True)

# --- LÓGICA DE CÁLCULO E RESULTADOS ---
if btn:
    with st.spinner("Conectando motor de cálculo Ecom Super..."):
        time.sleep(1.2)

    v_imp = preco_v * (imp / 100)
    v_ads_por_unidade = verba_ads / vendas_estimadas if vendas_estimadas > 0 else 0
    custo_base_produto = c_nf + c_emb + c_extra
    custo_total_loja = custo_base_produto + v_imp + v_ads_por_unidade

    res = {
        "Mercado Livre": {"lucro": preco_v - custo_total_loja - (preco_v * 0.165) - (6.0 if preco_v < 79 else 0.0) - f_ml, "cor": "ml", "logo": "ml_logo.png", "comis": preco_v * 0.165, "fixa": (6.0 if preco_v < 79 else 0.0), "frete": f_ml},
        "Shopee": {"lucro": preco_v - custo_total_loja - (preco_v * (0.26 if sh_fg else 0.20)) - 4.0, "cor": "shopee", "logo": "sh_logo.png", "comis": preco_v * (0.26 if sh_fg else 0.20), "fixa": 4.0, "frete": 0},
        "Amazon": {"lucro": preco_v - custo_total_loja - (preco_v * 0.15), "cor": "amazon", "logo": "am_logo.png", "comis": preco_v * 0.15, "fixa": 0, "frete": 0}
    }

    cols = st.columns(3)
    for i, (nome, dados) in enumerate(res.items()):
        with cols[i]:
            # --- CARD TOPO (LOGOS) ---
            st.markdown("<div style='text-align: center; margin-bottom: 10px;'>", unsafe_allow_html=True)
            if os.path.exists(dados["logo"]):
                st.image(dados["logo"], width=70)
            else:
                st.caption(f"**{nome}**")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- CARD RESULTADO ---
            margem = (dados["lucro"] / preco_v * 100) if preco_v > 0 else 0
            custo_total_operacao = custo_total_loja + dados["comis"] + dados["fixa"] + dados["frete"]
            roi = (dados["lucro"] / custo_total_operacao * 100) if custo_total_operacao > 0 else 0

            if dados["lucro"] > 0:
                st.markdown(f"<div class='caixa-resultado {dados['cor']}'><h4>{nome}</h4><h2 style='color: #2ea043;'>R$ {dados['lucro']:.2f}</h2><p style='color: gray; margin: 0;'>{margem:.1f}% Margem</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='caixa-resultado prejuizo-box'><h4>{nome}</h4><h2 style='color: #ff6961;'>PREJUÍZO</h2><p style='color: gray; margin: 0;'>{margem:.1f}% Margem</p></div>", unsafe_allow_html=True)
                st.markdown("<p class='prejuizo-texto'>NÃO VALE A PENA!</p>", unsafe_allow_html=True)
                if os.path.exists("dino.png"):
                    st.image("dino.png", use_container_width=True)

            # --- EXTRATO FINANCEIRO COMPLETO ---
            with st.expander(f"📊 DRE Detalhado {nome}"):
                st.write(f"**(+) Preço Venda:** R$ {preco_v:.2f}")
                st.write(f"**(-) Custos Produto/Envio:** R$ {custo_base_produto:.2f}")
                st.write(f"**(-) Imposto Gov ({imp}%):** R$ {v_imp:.2f}")
                if v_ads_por_unidade > 0:
                    st.write(f"**(-) Ads (CPA/Unidade):** R$ {v_ads_por_unidade:.2f}")
                st.write(f"**(-) Comissão Site:** R$ {dados['comis']:.2f}")
                if dados['fixa'] > 0: st.write(f"**(-) Taxa Fixa:** R$ {dados['fixa']:.2f}")
                if dados['frete'] > 0: st.write(f"**(-) Frete Plataforma:** R$ {dados['frete']:.2f}")
                st.markdown("---")
                cor_final = "#2ea043" if dados["lucro"] > 0 else "#ff6961"
                st.markdown(f"**Lucro Líquido:** <span style='color:{cor_final}'>R$ {dados['lucro']:.2f}</span>", unsafe_allow_html=True)
                st.markdown(f"**ROI:** <span style='color:{cor_final}'>{roi:.1f}%</span>", unsafe_allow_html=True)

    if any(d["lucro"] > (preco_v * 0.25) for d in res.values()):
        st.balloons()