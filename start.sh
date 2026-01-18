#!/bin/bash
# Script de inicialização rápida do ExtratorADK

echo "=================================================="
echo "🚀 ExtratorADK - Sistema de Extração de Documentos"
echo "=================================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verifica se está no diretório correto
if [ ! -f "extrator_agent/agent.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script no diretório raiz do projeto${NC}"
    exit 1
fi

# Verifica se ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtual não encontrado. Criando...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
fi

# Ativa ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Verifica se dependências estão instaladas
if ! python3 -c "import google.adk" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Dependências não instaladas. Instalando...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dependências instaladas${NC}"
else
    echo -e "${GREEN}✅ Dependências já instaladas${NC}"
fi

# Verifica API Key
if ! grep -q "GOOGLE_API_KEY=" .env 2>/dev/null; then
    echo -e "${RED}❌ API Key não configurada no arquivo .env${NC}"
    exit 1
fi
echo -e "${GREEN}✅ API Key configurada${NC}"

echo ""
echo "=================================================="
echo "Escolha o modo de execução:"
echo "=================================================="
echo ""
echo "1) 🌐 Modo Web (http://localhost:8000)"
echo "2) 💻 Modo CLI (linha de comando)"
echo "3) 🧪 Executar testes"
echo "4) 📋 Apenas ativar ambiente"
echo ""
read -p "Digite a opção [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "🌐 Iniciando modo web..."
        echo "Acesse: http://localhost:8000"
        echo ""
        adk web extrator_agent --port 8000
        ;;
    2)
        echo ""
        echo "💻 Iniciando modo CLI..."
        echo ""
        adk run extrator_agent
        ;;
    3)
        echo ""
        echo "🧪 Executando testes..."
        echo ""
        python3 test_extractor.py
        ;;
    4)
        echo ""
        echo -e "${GREEN}✅ Ambiente ativado!${NC}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  - adk web extrator_agent --port 8000  (Modo web)"
        echo "  - adk run extrator_agent              (Modo CLI)"
        echo "  - python3 test_extractor.py           (Testes)"
        echo ""
        # Mantém shell ativo
        exec $SHELL
        ;;
    *)
        echo -e "${RED}❌ Opção inválida${NC}"
        exit 1
        ;;
esac
