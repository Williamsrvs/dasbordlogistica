# Torre de Controle Logístico 🏗️

Dashboard interativo desenvolvido em Python com Streamlit para monitoramento em tempo real da cadeia de suprimentos. O projeto nasceu da necessidade de centralizar dados de transporte que estavam espalhados em planilhas, e transformar isso em algo que qualquer pessoa da operação consiga abrir e entender em segundos.

---

## Sobre o projeto

A ideia é simples: uma torre de controle logístico precisa entregar visibilidade rápida. Quem está atrasado? Qual transportadora está com mais ocorrências esse mês? Qual doca está sobrecarregada? Essas perguntas precisam de resposta em segundos, não em horas de análise manual.

O dashboard consolida 12.000 registros de viagens cobrindo clientes como Nestlé, Heineken, Ambev, BRF, Unilever, entre outros, com dados de tempo de espera, tempo em doca, ocorrências, rotas, frota e muito mais.

---

## Funcionalidades

- **KPIs em tempo real** — total de viagens, % de atrasos, SLA cumprido, valor transportado, peso total e tempo médio operacional
- **Filtros dinâmicos** — filtre por cliente, transportadora, status, prioridade, operação e ano; todos os gráficos atualizam instantaneamente
- **Análise temporal** — volume mensal de viagens cruzado com percentual de atrasos em eixo duplo
- **Performance por transportadora** — boxplot de tempos e ranking comparativo com taxa de atraso e ocorrências
- **Mapa de fluxo Sankey** — visualização das principais rotas origem × destino
- **Análise de docas** — quais docas concentram mais movimentação e quais horários são críticos
- **Ranking de transportadoras** — tabela consolidada com todos os indicadores por operador
- **Tabela de viagens recentes** — consulta rápida das últimas operações com todos os campos relevantes

---

## Tecnologias utilizadas

| Biblioteca | Versão recomendada | Finalidade |
|---|---|---|
| Python | 3.10+ | Linguagem base |
| Streamlit | 1.35+ | Interface web interativa |
| Pandas | 2.0+ | Manipulação e análise dos dados |
| Plotly | 5.20+ | Gráficos interativos |
| OpenPyXL | 3.1+ | Leitura do arquivo Excel |

---

## Como rodar localmente

**1. Clone ou baixe o projeto**

```bash
git clone https://github.com/seu-usuario/torre-controle-logistico.git
cd torre-controle-logistico
```

**2. Crie um ambiente virtual (recomendado)**

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

**3. Instale as dependências**

```bash
pip install streamlit pandas plotly openpyxl
```

**4. Coloque o arquivo de dados na pasta raiz**

O arquivo `torre_controle.xlsx` precisa estar na mesma pasta que o `app.py`. Se quiser usar outro caminho, basta ajustar a linha de `pd.read_excel()` no código.

**5. Execute o dashboard**

```bash
streamlit run app.py
```

O Streamlit abrirá automaticamente no navegador em `http://localhost:8501`.

---

## Estrutura do projeto

```
torre-controle-logistico/
│
├── app.py                  # Aplicação principal
├── torre_controle.xlsx     # Base de dados (não versionar em projetos reais)
├── README.md               # Este arquivo
└── requirements.txt        # Dependências (opcional)
```

Se quiser gerar o `requirements.txt` automaticamente:

```bash
pip freeze > requirements.txt
```

---

## Estrutura dos dados

O arquivo Excel deve conter as seguintes colunas para o dashboard funcionar corretamente:

| Coluna | Tipo | Descrição |
|---|---|---|
| ID_VIAGEM | texto | Identificador único da viagem |
| CLIENTE | texto | Nome do cliente |
| TRANSPORTADORA | texto | Nome da transportadora |
| PLACA | texto | Placa do veículo |
| MOTORISTA | texto | Nome do motorista |
| TIPO_VEICULO | texto | Truck, Bitrem, Toco, Carreta, VUC |
| OPERACAO | texto | Carga ou Descarga |
| STATUS | texto | Finalizado, Atrasado, Em Doca, etc. |
| DATA_REGISTRO | datetime | Data/hora do registro |
| DATA_AGENDAMENTO | datetime | Agendamento previsto |
| CHEGADA_REAL | datetime | Chegada real ao pátio |
| ENTRADA_PATIO | datetime | Entrada no pátio |
| ENTRADA_DOCA | datetime | Entrada na doca |
| SAIDA_DOCA | datetime | Saída da doca |
| LIBERACAO | datetime | Liberação final |
| TEMPO_ESPERA_MIN | inteiro | Tempo de espera no pátio (min) |
| TEMPO_DOCA_MIN | inteiro | Tempo operando na doca (min) |
| TEMPO_TOTAL_MIN | inteiro | Tempo total da operação (min) |
| PESO_KG | decimal | Peso da carga em kg |
| VALOR_CARGA | decimal | Valor da carga em reais |
| DOCA | texto | Identificação da doca utilizada |
| UF_ORIGEM | texto | UF de origem da carga |
| UF_DESTINO | texto | UF de destino da carga |
| PRIORIDADE | texto | Alta, Média ou Baixa |
| OCORRENCIA | texto | Tipo de ocorrência registrada |

---

## Definição de SLA

O dashboard considera SLA cumprido quando o **tempo total da operação é igual ou inferior a 240 minutos** (4 horas). Esse parâmetro pode ser ajustado diretamente na linha:

```python
df["SLA_OK"] = df["TEMPO_TOTAL_MIN"] <= 240
```

---

## Possíveis melhorias futuras

- [ ] Conexão direta com banco de dados (PostgreSQL, MySQL) em vez de Excel
- [ ] Atualização automática dos dados em intervalos configuráveis
- [ ] Exportação de relatórios em PDF com um clique
- [ ] Alertas por e-mail quando o percentual de atrasos ultrapassar um limite
- [ ] Autenticação de usuários por perfil (operacional, gerencial, diretoria)
- [ ] Versão mobile responsiva

---

## Observações

- O cache dos dados é feito com `@st.cache_data`, então o arquivo Excel é lido apenas uma vez por sessão. Se atualizar a planilha, pressione **C** no teclado ou clique em "Clear cache" no menu do Streamlit para recarregar.
- O dashboard foi desenvolvido com tema escuro. Para usar com tema claro, ajuste as variáveis de cor no bloco de CSS customizado no início do `app.py`.
- Em bases de dados muito grandes (acima de 100k linhas), considere aplicar filtros antes de carregar tudo em memória ou migrar para um banco de dados.

---

## Licença

Projeto desenvolvido para uso interno. Adapte, modifique e distribua como quiser.

---

Feito com Python, Streamlit e muito café. ☕
