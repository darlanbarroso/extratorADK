# 🚀 QUICKSTART - ExtratorADK

**Extração de Documentos Brasileiros em 5 minutos!**

---

## ⚡ Setup Rápido

### 1. Prepare o ambiente

```bash
cd /Users/MacBarroso/extratorADK

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Teste a instalação

```bash
python3 test_extractor.py
```

Deve mostrar:
```
✅ TODOS OS TESTES PASSARAM!
```

---

## 🎯 Iniciando o Agente

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

## 📸 Preparando Documentos

### 1. Coloque imagens na pasta data/

```bash
# Crie a pasta se não existir
mkdir -p data

# Copie suas imagens
cp ~/Downloads/meu_rg.jpg data/
cp ~/Downloads/minha_cnh.png data/
```

### 2. Formatos suportados

- JPG/JPEG
- PNG
- BMP
- TIFF

---

## 💬 Primeiros Comandos

### Listar imagens

```
"liste as imagens disponíveis"
```

**Resposta:**
```
Encontradas 2 imagens:
- data/meu_rg.jpg
- data/minha_cnh.png
```

### Extrair RG

```
"extraia o RG data/meu_rg.jpg"
```

**Resposta:**
```
✅ DADOS EXTRAÍDOS:
- Nome: João da Silva
- RG: 12.345.678-9
- CPF: 111.444.777-35
- Data Nascimento: 15/05/1990
- Órgão Emissor: SSP/SP

🔍 VALIDAÇÕES:
- CPF: ✅ Válido
- RG: ✅ Formato válido
- Data: ✅ Válida (35 anos)
```

### Extrair CNH

```
"processe a CNH data/minha_cnh.png"
```

**Resposta:**
```
✅ DADOS EXTRAÍDOS:
- Nome: Maria Santos
- CNH: 12345678901
- CPF: 987.654.321-00
- Categoria: AB
- Validade: 15/06/2028

🔍 VALIDAÇÕES:
- CNH: ✅ Válida
- CPF: ✅ Válido
- Status: ✅ Válida (928 dias para vencer)
```

### Auto-detectar documento

```
"extraia o documento data/documento.jpg"
```

O agente identifica automaticamente se é RG, CNH ou CPF.

---

## 📊 Exemplos Práticos

### 1. Validar CPF manualmente

```
"valide o CPF 111.444.777-35"
```

**Resposta:**
```
✅ CPF Válido
- Número: 11144477735
- Formatado: 111.444.777-35
- Dígitos verificadores: OK
```

### 2. Validar CNH

```
"valide a CNH 12345678901"
```

### 3. Salvar resultados

```
"salve a extração em data/processed/resultado.json"
```

**Resposta:**
```
✅ Dados salvos em: data/processed/resultado.json
```

Arquivo JSON gerado:
```json
{
  "status": "success",
  "tipo_documento": "RG",
  "data": {
    "nome_completo": "João da Silva",
    "numero_rg": "12.345.678-9",
    "cpf": "111.444.777-35",
    ...
  },
  "validations": {
    "cpf": {"valid": true},
    "rg": {"valid": true}
  }
}
```

---

## 🔍 Comandos Úteis

### Processamento em lote

```
"extraia todos os documentos da pasta data"
```

### Análise específica

```
"extraia apenas o CPF desta imagem"
"qual a data de validade da CNH?"
"o documento está vencido?"
```

---

## 🛠️ Workflow Completo

### Exemplo: Processar CNH

```bash
# 1. Liste imagens
"quais imagens temos?"

# 2. Extraia documento
"extraia a CNH data/cnh_joao.jpg"

# 3. Analise resultado
# O agente mostra dados + validações automaticamente

# 4. Salve resultado
"salve em data/processed/cnh_joao.json"
```

---

## 🆘 Troubleshooting

### Problema: "API Key não encontrada"

```bash
cat .env  # Verifica se existe

# Deve conter:
# GOOGLE_API_KEY=AIzaSyBRruCqweQpdw2nAeaHQgqQ3HGGbosj4aI
```

### Problema: "Erro ao processar imagem"

**Causas comuns:**
- Imagem muito escura/borrada
- Arquivo corrompido
- Formato não suportado

**Solução:**
- Use imagens nítidas e bem iluminadas
- Prefira PNG ou JPG
- Resolução mínima: 800x600

### Problema: "Dados extraídos incorretos"

**Solução:**
- Use imagens de boa qualidade
- Evite reflexos e sombras
- CNH: fotografe frente E verso separadamente
- RG: fotografe frente E verso separadamente

---

## 📋 Checklist de Uso

- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Teste executado com sucesso
- [ ] Imagens na pasta data/
- [ ] Agente iniciado (web ou CLI)
- [ ] Primeiro documento extraído

---

## 💡 Dicas de Uso

**Qualidade da Imagem:**
- Iluminação uniforme
- Foco nítido
- Sem reflexos
- Documento completo visível

**Comandos:**
- Use linguagem natural
- Seja específico: "extraia o RG" é melhor que "extraia isso"
- O agente entende português e inglês

**Validação:**
- Sempre verifique os dados extraídos
- CPF e CNH têm validação automática de dígitos
- Datas são validadas quanto ao formato

---

## 📚 Próximos Passos

1. Teste com seus documentos reais
2. Explore diferentes tipos (RG, CNH, CPF)
3. Use validação para conferir dados
4. Automatize processos repetitivos
5. Leia o [README.md](README.md) completo

---

## 🎯 Casos de Uso

- Digitalização de documentos
- Validação de identidade
- Cadastro de clientes
- Auditoria de documentos
- Arquivo digital organizado

---

**Pronto para extrair documentos! 🎉**

Dúvidas: darlan.engemec@gmail.com
