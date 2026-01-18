# ExtratorADK

**Extração Inteligente de Documentos Brasileiros (RG, CNH, CPF)**

ExtratorADK é um agente baseado em Google ADK e Gemini 2.0 Flash Vision, especializado em extrair e validar dados de documentos de identidade brasileiros usando OCR e IA.

---

## 🎯 Características

- ✅ **Extração OCR com IA:** Gemini Vision 2.0 Flash para análise de imagens
- ✅ **Documentos Suportados:** RG, CNH e CPF
- ✅ **Validação Automática:** CPF, CNH, datas (com dígitos verificadores)
- ✅ **Auto-detecção:** Identifica automaticamente o tipo de documento
- ✅ **Saída Estruturada:** JSON com todos os campos extraídos
- ✅ **Interface Conversacional:** Google ADK com chat web ou CLI
- ✅ **Processamento em Lote:** Múltiplos documentos de uma vez

---

## 📋 Pré-requisitos

- Python 3.11+
- Google AI Studio API Key (Gemini)
- pip para gerenciamento de pacotes

---

## 🔧 Instalação Rápida

### 1. Navegue até o projeto

```bash
cd /Users/MacBarroso/extratorADK
```

### 2. Crie ambiente virtual e instale dependências

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure a API Key (já configurada)

O arquivo `.env` já contém sua API Key do Gemini:

```bash
GOOGLE_API_KEY=AIzaSyBRruCqweQpdw2nAeaHQgqQ3HGGbosj4aI
```

### 4. Teste a instalação

```bash
python3 test_extractor.py
```

---

## 🚀 Como Usar

### Modo Web (Recomendado)

```bash
adk web extrator_agent --port 8000
```

Acesse: **http://localhost:8000**

### Modo CLI

```bash
adk run extrator_agent
```

---

## 💬 Exemplos de Uso

Coloque suas imagens de documentos na pasta `data/` e use comandos como:

### Extração de Documentos

```
"liste as imagens disponíveis"
→ Mostra todas as imagens em data/

"extraia o documento data/rg_joao.jpg"
→ Auto-detecta tipo e extrai dados

"processe a CNH data/cnh_maria.png"
→ Extrai dados da CNH com validação

"extraia o RG data/rg_frente.jpg"
→ Extrai dados do RG
```

### Validação de Dados

```
"valide o CPF 111.444.777-35"
→ Valida dígitos verificadores

"valide a CNH 12345678901"
→ Verifica dígitos da CNH
```

### Salvar Resultados

```
"salve a extração em data/processed/resultado.json"
→ Salva dados extraídos em JSON
```

---

## 📁 Estrutura do Projeto

```
extratorADK/
├── extrator_agent/
│   ├── __init__.py
│   └── agent.py              # Agente ADK com 8 ferramentas
├── src/
│   ├── document_extractor.py # Extração com Gemini Vision
│   └── validators.py         # Validadores de CPF, CNH, RG
├── data/                     # 📂 Coloque suas imagens aqui
│   ├── processed/            # Resultados JSON salvos
│   └── examples/
├── config/                   # Configurações
├── models/                   # Modelos futuros
├── tests/                    # Testes
├── .env                      # API Key (protegida)
├── requirements.txt
├── test_extractor.py         # Script de teste
└── README.md
```

---

## 🛠️ Ferramentas do Agente

O agente possui **8 ferramentas** especializadas:

### Extração de Documentos

| Ferramenta | Descrição |
|-----------|-----------|
| `extract_rg(image_path)` | Extrai dados de RG |
| `extract_cnh(image_path)` | Extrai dados de CNH |
| `extract_cpf_document(image_path)` | Extrai dados de CPF |
| `extract_document_auto(image_path)` | Auto-detecta tipo e extrai |

### Validação

| Ferramenta | Descrição |
|-----------|-----------|
| `validate_cpf_number(cpf)` | Valida CPF (dígitos verificadores) |
| `validate_cnh_number(cnh)` | Valida CNH (dígitos verificadores) |

### Utilitários

| Ferramenta | Descrição |
|-----------|-----------|
| `list_images(directory)` | Lista imagens disponíveis |
| `save_extraction(data, file)` | Salva resultados em JSON |

---

## 📊 Dados Extraídos

### RG (Registro Geral)
```json
{
  "tipo_documento": "RG",
  "numero_rg": "12.345.678-9",
  "orgao_emissor": "SSP",
  "uf_emissor": "SP",
  "data_emissao": "01/01/2020",
  "nome_completo": "João da Silva",
  "data_nascimento": "15/05/1990",
  "filiacao_pai": "José da Silva",
  "filiacao_mae": "Maria da Silva",
  "naturalidade": "São Paulo - SP",
  "cpf": "123.456.789-09"
}
```

### CNH (Carteira Nacional de Habilitação)
```json
{
  "tipo_documento": "CNH",
  "numero_registro": "12345678901",
  "nome_completo": "João da Silva",
  "data_nascimento": "15/05/1990",
  "cpf": "123.456.789-09",
  "data_primeira_habilitacao": "01/01/2010",
  "data_emissao": "01/01/2020",
  "data_validade": "01/01/2025",
  "categoria": "AB",
  "local_emissao": "São Paulo - SP",
  "orgao_emissor": "DETRAN/SP",
  "observacoes": "EAR"
}
```

### CPF
```json
{
  "tipo_documento": "CPF",
  "numero_cpf": "123.456.789-09",
  "nome_completo": "João da Silva",
  "data_nascimento": "15/05/1990",
  "situacao_cadastral": "Regular"
}
```

---

## ✅ Validações Realizadas

O sistema valida automaticamente:

- **CPF:** Calcula e verifica os 2 dígitos verificadores
- **CNH:** Verifica dígitos verificadores da CNH
- **Datas:** Valida formato e coerência (nascimento, emissão, validade)
- **CNH Vencida:** Detecta se CNH está vencida e informa dias para vencer
- **RG:** Validação básica de formato

---

## 🔒 Segurança

- ⚠️ **NUNCA** commite o arquivo `.env`
- API Key protegida no `.gitignore`
- Dados sensíveis processados localmente
- Regenere API Key se exposta

---

## 🧪 Testes

Execute o script de teste:

```bash
python3 test_extractor.py
```

Testa:
1. Importações de bibliotecas
2. Configuração da API
3. Módulos customizados
4. Validadores (CPF, CNH, datas)
5. DocumentExtractor
6. Agente ADK

---

## 🐛 Troubleshooting

### Erro: "GOOGLE_API_KEY não encontrada"
```bash
# Verifique se o .env existe e contém a chave
cat .env
```

### Erro: "Module not found"
```bash
# Reinstale dependências
pip install -r requirements.txt
```

### Erro ao processar imagem
- Verifique se a imagem está em formato suportado (JPG, PNG)
- Confirme que o caminho está correto
- Imagens com baixa qualidade podem ter extração imprecisa

---

## 📝 Roadmap

- [x] Extração de RG, CNH e CPF
- [x] Validação de documentos brasileiros
- [x] Interface ADK conversacional
- [ ] Suporte para CNH digital (QR Code)
- [ ] OCR offline com Tesseract
- [ ] API REST para integração
- [ ] Dashboard web de resultados
- [ ] Processamento batch automático

---

## 📧 Contato

- **Desenvolvedor:** Darlan Barroso
- **Email:** darlan.engemec@gmail.com

---

## 🙏 Agradecimentos

- Google ADK Team
- Google Gemini Vision API
- Comunidade validate-docbr

---

**Versão:** 1.0.0
**Última atualização:** 2026-01-17
**Licença:** Uso interno/pessoal
