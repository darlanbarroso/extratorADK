# 🏗️ ARQUITETURA - ExtratorADK

**Documentação Técnica do Sistema**

---

## 📐 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    USUÁRIO                                   │
│                 (Web ou CLI)                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Linguagem Natural
                        │ "extraia o RG data/rg.jpg"
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              GOOGLE ADK FRAMEWORK                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │    root_agent (extrator_agent)                      │    │
│  │    - Modelo: gemini-2.0-flash-exp                   │    │
│  │    - 8 ferramentas registradas                      │    │
│  │    - Instructions: Prompts do agente                │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Seleciona ferramenta apropriada
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              CAMADA DE FERRAMENTAS                           │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ extract_rg   │extract_cnh   │extract_cpf   │            │
│  │ extract_auto │list_images   │save_extract  │            │
│  │ validate_cpf │validate_cnh  │              │            │
│  └──────────────┴──────────────┴──────────────┘            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Chama módulos
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              MÓDULOS CORE                                    │
│  ┌─────────────────────┐  ┌──────────────────────┐         │
│  │ DocumentExtractor   │  │ DocumentValidator     │         │
│  │                     │  │                       │         │
│  │ - extract_rg()      │  │ - validate_cpf()     │         │
│  │ - extract_cnh()     │  │ - validate_cnh()     │         │
│  │ - extract_cpf()     │  │ - validate_date()    │         │
│  │ - extract_auto()    │  │ - validate_rg()      │         │
│  │ - extract_batch()   │  │                       │         │
│  └─────────────────────┘  └──────────────────────┘         │
└───────────────────────┬─────────────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
┌─────────────────────┐  ┌──────────────────────┐
│  GEMINI VISION API  │  │  VALIDAÇÃO LOCAL     │
│                     │  │                      │
│  - Analisa imagem   │  │  - Algoritmo CPF     │
│  - Extrai texto     │  │  - Algoritmo CNH     │
│  - Retorna JSON     │  │  - Parser de datas   │
│  - OCR contextual   │  │  - Instant (< 1ms)   │
└─────────────────────┘  └──────────────────────┘
            │                       │
            └───────────┬───────────┘
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              RESULTADO ESTRUTURADO                           │
│                                                              │
│  {                                                           │
│    "status": "success",                                      │
│    "data": { ... },      // Dados extraídos                 │
│    "validations": { ... } // Validações aplicadas           │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Extração de Documento

### Exemplo: Extrair CNH

```
1️⃣ USUÁRIO
   │
   ├─ Comando: "extraia a CNH data/cnh_joao.jpg"
   │
   ▼

2️⃣ AGENTE ADK
   │
   ├─ Interpreta comando
   ├─ Identifica: extract_cnh()
   ├─ Parâmetros: image_path="data/cnh_joao.jpg", validate=True
   │
   ▼

3️⃣ FERRAMENTA extract_cnh()
   │
   ├─ Chama: extractor.extract_cnh(image_path)
   │
   ▼

4️⃣ DocumentExtractor
   │
   ├─ Abre imagem com PIL
   ├─ Seleciona prompt especializado para CNH
   ├─ Envia para Gemini Vision API
   │
   ▼

5️⃣ GEMINI VISION API
   │
   ├─ Analisa imagem
   ├─ Identifica campos (nome, CPF, categoria, etc)
   ├─ Retorna JSON estruturado
   │
   ▼

6️⃣ DocumentExtractor (parsing)
   │
   ├─ Remove markdown code blocks
   ├─ Parseia JSON
   ├─ Retorna para ferramenta
   │
   ▼

7️⃣ FERRAMENTA extract_cnh() (validação)
   │
   ├─ Se validate=True:
   │   ├─ validator.validate_cnh(numero_registro)
   │   ├─ validator.validate_cpf(cpf)
   │   ├─ validator.validate_date(data_nascimento)
   │   └─ validator.validate_cnh_expiration(emissao, validade)
   │
   ├─ Adiciona validações ao resultado
   │
   ▼

8️⃣ AGENTE ADK (formatação)
   │
   ├─ Formata resposta estruturada:
   │   │
   │   ├─ ✅ DADOS EXTRAÍDOS:
   │   │   - Nome: João da Silva
   │   │   - CNH: 12345678901
   │   │   - CPF: 111.444.777-35
   │   │   ...
   │   │
   │   └─ 🔍 VALIDAÇÕES:
   │       - CNH: ✅ Válida
   │       - CPF: ✅ Válido
   │       - Status: ✅ Válida (928 dias para vencer)
   │
   ▼

9️⃣ USUÁRIO
   │
   └─ Recebe resultado formatado
```

---

## 🧩 Componentes Detalhados

### 1. Agente ADK (root_agent)

**Localização:** `extrator_agent/agent.py`

```python
root_agent = Agent(
    name="extrator_agent",
    model="gemini-2.0-flash-exp",
    description="...",
    instruction="...",  # Instruções detalhadas
    tools=[
        extract_rg,
        extract_cnh,
        extract_cpf_document,
        extract_document_auto,
        list_images,
        save_extraction,
        validate_cpf_number,
        validate_cnh_number,
    ]
)
```

**Responsabilidades:**
- Interpretar comandos do usuário
- Selecionar ferramenta apropriada
- Formatar respostas
- Gerenciar contexto da conversa

---

### 2. DocumentExtractor

**Localização:** `src/document_extractor.py`

```python
class DocumentExtractor:
    PROMPTS = {
        "rg": "...",    # Prompt especializado para RG
        "cnh": "...",   # Prompt especializado para CNH
        "cpf": "...",   # Prompt especializado para CPF
        "auto": "..."   # Prompt auto-detecção
    }

    def extract_from_image(self, image_path, document_type):
        # 1. Abre imagem com PIL
        image = Image.open(image_path)

        # 2. Seleciona prompt
        prompt = self.PROMPTS[document_type]

        # 3. Envia para Gemini Vision
        response = self.model.generate_content([prompt, image])

        # 4. Parseia resposta
        data = json.loads(response.text)

        return {"status": "success", "data": data}
```

**Responsabilidades:**
- Gerenciar prompts especializados
- Integração com Gemini Vision API
- Processamento de imagens
- Parsing de JSON

---

### 3. DocumentValidator

**Localização:** `src/validators.py`

```python
class DocumentValidator:
    @staticmethod
    def validate_cpf(cpf: str) -> Dict:
        # 1. Remove formatação
        cpf_numbers = re.sub(r'\D', '', cpf)

        # 2. Verifica comprimento
        if len(cpf_numbers) != 11:
            return {"valid": False}

        # 3. Calcula primeiro dígito verificador
        soma = sum(int(cpf_numbers[i]) * (10 - i) for i in range(9))
        primeiro_digito = 11 - (soma % 11)
        if primeiro_digito >= 10:
            primeiro_digito = 0

        # 4. Calcula segundo dígito verificador
        soma = sum(int(cpf_numbers[i]) * (11 - i) for i in range(10))
        segundo_digito = 11 - (soma % 11)
        if segundo_digito >= 10:
            segundo_digito = 0

        # 5. Valida dígitos
        if (int(cpf_numbers[9]) != primeiro_digito or
            int(cpf_numbers[10]) != segundo_digito):
            return {"valid": False}

        return {"valid": True, "formatted": "..."}
```

**Responsabilidades:**
- Validar CPF (algoritmo oficial)
- Validar CNH (algoritmo DETRAN)
- Validar datas (coerência temporal)
- Validar RG (formato básico)

---

## 🎨 Prompts Engineering

### Estrutura dos Prompts

Cada prompt segue a estrutura:

```
1. OBJETIVO
   - "Analise esta imagem de um [TIPO] brasileiro"

2. FORMATO DE SAÍDA
   - JSON estruturado com campos específicos

3. INSTRUÇÕES
   - Extraia apenas texto visível
   - Mantenha formatação original
   - Use null para campos não visíveis
   - Retorne APENAS JSON

4. EXEMPLO DE ESTRUTURA
   {
     "tipo_documento": "...",
     "campo1": "...",
     "campo2": "..."
   }
```

### Exemplo: Prompt CNH

```python
PROMPTS["cnh"] = """
Analise esta imagem de uma CNH (Carteira Nacional de Habilitação) brasileira
e extraia TODAS as informações visíveis.

Retorne um JSON com a seguinte estrutura:

{
  "tipo_documento": "CNH",
  "numero_registro": "XXXXXXXXXXX",
  "nome_completo": "Nome completo",
  "data_nascimento": "DD/MM/AAAA",
  "cpf": "XXX.XXX.XXX-XX",
  "data_primeira_habilitacao": "DD/MM/AAAA",
  "data_emissao": "DD/MM/AAAA",
  "data_validade": "DD/MM/AAAA",
  "categoria": "AB",
  "local_emissao": "Cidade - UF",
  "orgao_emissor": "DETRAN/XX",
  "observacoes": "Ex: EAR, OD, etc"
}

INSTRUÇÕES:
- Extraia apenas texto visível e legível
- A CNH tem informações frente e verso - extraia tudo que conseguir ver
- Mantenha formatação original de números
- Se um campo não estiver visível, use null
- Retorne APENAS o JSON, sem explicações
"""
```

**Por que funciona:**
- Contexto claro (CNH brasileira)
- Estrutura exata esperada
- Instruções específicas
- Formato de saída definido

---

## 🔐 Segurança e Validação

### Camadas de Segurança

```
┌─────────────────────────────────────┐
│  1. API KEY PROTECTION              │
│     - Armazenada em .env            │
│     - Não commitada (gitignore)     │
│     - Carregada via python-dotenv   │
└─────────────────────────────────────┘
            ▼
┌─────────────────────────────────────┐
│  2. INPUT VALIDATION                │
│     - Verifica existência de arquivo│
│     - Valida formato de imagem      │
│     - Checa permissões de leitura   │
└─────────────────────────────────────┘
            ▼
┌─────────────────────────────────────┐
│  3. OCR EXTRACTION                  │
│     - Gemini Vision API             │
│     - Timeout configurável          │
│     - Error handling                │
└─────────────────────────────────────┘
            ▼
┌─────────────────────────────────────┐
│  4. DATA VALIDATION                 │
│     - CPF: Dígitos verificadores    │
│     - CNH: Algoritmo oficial        │
│     - Datas: Formato e coerência    │
│     - RG: Formato básico            │
└─────────────────────────────────────┘
            ▼
┌─────────────────────────────────────┐
│  5. OUTPUT SANITIZATION             │
│     - JSON estruturado              │
│     - Campos validados              │
│     - Erros tratados                │
└─────────────────────────────────────┘
```

---

## 📊 Fluxo de Dados

### Estrutura de Dados Completa

```python
# Entrada
{
    "image_path": "data/cnh_joao.jpg",
    "validate": True
}

# Processamento
DocumentExtractor → Gemini Vision API
                ↓
        Extração OCR
                ↓
        Parsing JSON
                ↓
    DocumentValidator
                ↓
    Validações Aplicadas

# Saída
{
    "status": "success",
    "message": "Documento processado com sucesso",
    "image_path": "data/cnh_joao.jpg",
    "document_type": "cnh",

    "data": {
        "tipo_documento": "CNH",
        "numero_registro": "12345678901",
        "nome_completo": "João da Silva",
        "data_nascimento": "15/05/1990",
        "cpf": "111.444.777-35",
        "data_primeira_habilitacao": "01/01/2010",
        "data_emissao": "01/01/2020",
        "data_validade": "01/01/2025",
        "categoria": "AB",
        "orgao_emissor": "DETRAN/SP"
    },

    "validations": {
        "cnh": {
            "valid": True,
            "cnh": "12345678901"
        },
        "cpf": {
            "valid": True,
            "cpf": "11144477735",
            "formatted": "111.444.777-35"
        },
        "data_nascimento": {
            "valid": True,
            "date": "1990-05-15",
            "age_years": 35
        },
        "validade_cnh": {
            "valid": True,
            "status": "válida",
            "dias_para_vencer": 928,
            "vencida": False
        }
    }
}
```

---

## 🚀 Performance e Otimização

### Métricas

| Operação | Tempo | Custo |
|----------|-------|-------|
| Extração (Gemini Vision) | 2-5s | ~R$ 0,0015/imagem |
| Validação CPF | < 1ms | Gratuito |
| Validação CNH | < 1ms | Gratuito |
| Validação Datas | < 1ms | Gratuito |
| Salvamento JSON | < 10ms | Gratuito |

### Otimizações Implementadas

1. **Validação Local:**
   - Algoritmos implementados localmente
   - Sem chamadas de API para validação
   - Instant validation (< 1ms)

2. **Prompts Especializados:**
   - Reduz ambiguidade
   - Melhora precisão
   - Diminui retries

3. **Error Handling:**
   - Try/catch em todas operações
   - Mensagens de erro claras
   - Fallbacks quando possível

4. **Caching (futuro):**
   - Cache de resultados
   - Evita reprocessamento
   - Reduz custos de API

---

## 🔄 Extensibilidade

### Adicionar Novo Tipo de Documento

```python
# 1. Adicionar prompt em document_extractor.py
PROMPTS["passaporte"] = """
Analise esta imagem de um Passaporte brasileiro...
{
  "tipo_documento": "Passaporte",
  ...
}
"""

# 2. Criar função de extração em agent.py
def extract_passaporte(image_path: str, validate: bool = True):
    result = extractor.extract_from_image(image_path, "passaporte")
    # Adicionar validações específicas
    return result

# 3. Adicionar validador em validators.py (se necessário)
@staticmethod
def validate_passaporte(numero: str):
    # Lógica de validação
    pass

# 4. Registrar ferramenta no agente
root_agent.tools.append(extract_passaporte)
```

---

## 📝 Logs e Debugging

### Estrutura de Logs

```python
from loguru import logger

# Níveis de log usados:
logger.info("Processando imagem: {}", image_path)     # INFO
logger.error("Erro ao extrair: {}", error)            # ERROR
logger.warning("Validação falhou: {}", message)      # WARNING
logger.debug("Dados brutos: {}", raw_data)           # DEBUG
```

### Exemplo de Saída

```
2026-01-17 10:30:15 | INFO | Extraindo CNH: data/cnh_joao.jpg
2026-01-17 10:30:17 | INFO | Enviando para Gemini Vision (tipo: cnh)
2026-01-17 10:30:20 | INFO | Extração concluída com sucesso
2026-01-17 10:30:20 | INFO | Validando CPF: 111.444.777-35
2026-01-17 10:30:20 | INFO | CPF válido
2026-01-17 10:30:20 | INFO | Validando CNH: 12345678901
2026-01-17 10:30:20 | INFO | CNH válida
```

---

## 🎯 Decisões de Arquitetura

### Por que esta arquitetura?

| Decisão | Justificativa |
|---------|---------------|
| **Gemini Vision** | API Key disponível, alta precisão, sem setup local |
| **Modularização** | Separação clara: extractor, validator, agent |
| **Validação local** | Performance, custo zero, controle total |
| **Prompts especializados** | Maior precisão, menos ambiguidade |
| **Google ADK** | Interface conversacional nativa, fácil uso |
| **Python 3.11+** | Ecossistema rico, type hints, performance |

### Trade-offs

| Aspecto | Vantagem | Desvantagem | Mitigação |
|---------|----------|-------------|-----------|
| **Gemini Vision** | Alta precisão | Depende de internet | Pode adicionar Tesseract offline |
| **API paga** | Qualidade alta | Custo (baixo) | Cache de resultados |
| **Validação local** | Gratuita, rápida | Código próprio | Testes unitários |
| **JSON parsing** | Estruturado | Pode falhar | Error handling robusto |

---

**FIM DA DOCUMENTAÇÃO DE ARQUITETURA**
