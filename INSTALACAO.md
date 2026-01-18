# 📦 Guia de Instalação - ExtratorADK

## ✅ Status da Criação do Projeto

O projeto ExtratorADK foi criado com sucesso! Todos os arquivos e estrutura estão prontos.

---

## 📋 O que foi criado:

### ✅ Estrutura de diretórios
```
extratorADK/
├── extrator_agent/          # Agente principal com 4 ferramentas
├── src/                     # Código fonte modular
├── config/                  # Configurações
├── data/                    # Diretório para documentos
├── models/                  # Modelos (futuro)
└── tests/                   # Testes
```

### ✅ Arquivos criados
- ✅ `extrator_agent/agent.py` - Agente ADK com 4 ferramentas
- ✅ `.env` - API Key configurada (AIzaSyBRruCqweQpdw2nAeaHQgqQ3HGGbosj4aI)
- ✅ `requirements.txt` - Todas as dependências
- ✅ `.gitignore` - Proteção de arquivos sensíveis
- ✅ `README.md` - Documentação completa
- ✅ `QUICKSTART.md` - Guia rápido
- ✅ `test_setup.py` - Script de validação

### ✅ Ferramentas do Agente
1. `extract_pdf(file_path)` - Extração de PDFs
2. `analyze_document(text)` - Análise com IA
3. `list_documents(directory)` - Listagem de arquivos
4. `save_extraction(data, output_file)` - Salvar resultados

---

## 🚀 Próximos Passos (Você precisa executar):

### 1️⃣ Criar ambiente virtual

```bash
cd /Users/MacBarroso/extratorADK
python3 -m venv .venv
```

### 2️⃣ Ativar ambiente virtual

```bash
source .venv/bin/activate
```

Você verá `(.venv)` no início do prompt.

### 3️⃣ Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Isso vai instalar:
- google-adk (Google Agent Development Kit)
- PyPDF2, pdfplumber (extração de PDFs)
- python-docx (DOCX)
- pandas, numpy (processamento)
- E outras bibliotecas

**⏱️ Tempo estimado:** 2-5 minutos

### 4️⃣ Verificar instalação

```bash
python3 test_setup.py
```

Se todos os testes passarem, você verá:
```
🎉 TODOS OS TESTES PASSARAM!
```

### 5️⃣ Iniciar o agente

**Opção A: Interface Web**
```bash
adk web extrator_agent --port 8000
```

Depois acesse: http://localhost:8000

**Opção B: CLI**
```bash
adk run extrator_agent
```

---

## 🔧 Solução de Problemas

### Problema: "command not found: adk"

**Solução:**
```bash
# Verifique se o ambiente virtual está ativo
which python3  # Deve mostrar o caminho do .venv

# Se não estiver, ative:
source .venv/bin/activate

# Reinstale o ADK
pip install google-adk==1.15.1
```

### Problema: Erro de importação do Google Protobuf

**Solução:**
```bash
pip uninstall protobuf -y
pip install protobuf==4.25.1
```

### Problema: "GOOGLE_API_KEY não encontrada"

**Solução:**
```bash
# Verifique se o .env existe
cat .env

# Se não existir, crie:
echo "GOOGLE_API_KEY=AIzaSyBRruCqweQpdw2nAeaHQgqQ3HGGbosj4aI" > .env
```

---

## 📊 Diferenças do Projeto Original

| Aspecto | ADK_BeSolution_LLM | ExtratorADK |
|---------|-------------------|-------------|
| **Propósito** | Análise de dados educacionais MEC | Extração de documentos/PDFs |
| **API Key** | darlan.engemec@gmail.com (antiga) | darlan.engemec@gmail.com (nova) |
| **Ferramentas** | 12 ferramentas (pipeline ML) | 4 ferramentas (extração) |
| **Modelo** | gemini-2.0-flash | gemini-2.0-flash |
| **Foco** | Machine Learning + Clustering | Processamento de documentos |

---

## 🎯 Comandos Rápidos

```bash
# Navegar para o projeto
cd /Users/MacBarroso/extratorADK

# Ativar ambiente
source .venv/bin/activate

# Instalar
pip install -r requirements.txt

# Testar
python3 test_setup.py

# Rodar
adk web extrator_agent --port 8000
```

---

## ✨ Pronto para Usar!

O projeto está **100% configurado** e pronto para:

1. ✅ Instalar dependências
2. ✅ Rodar o agente
3. ✅ Começar a extrair documentos

**Tempo total necessário:** ~5 minutos para instalação

---

## 📞 Suporte

- **Email:** darlan.engemec@gmail.com
- **Projeto base:** ADK_BeSolution_LLM

---

**Data de criação:** 2026-01-17  
**Status:** ✅ Pronto para instalação
