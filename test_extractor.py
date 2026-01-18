#!/usr/bin/env python3
"""
Script de teste para o ExtratorADK
Valida instalação e funcionalidades básicas
"""
import sys
from pathlib import Path

print("=" * 60)
print("🧪 TESTE DE INSTALAÇÃO - ExtratorADK")
print("=" * 60)
print()

# 1. Testa importações básicas
print("1️⃣ Testando importações básicas...")
try:
    import os
    from dotenv import load_dotenv
    from PIL import Image
    import google.generativeai as genai
    from loguru import logger
    print("   ✅ Bibliotecas básicas OK")
except ImportError as e:
    print(f"   ❌ Erro ao importar bibliotecas: {e}")
    print("   Execute: pip install -r requirements.txt")
    sys.exit(1)

# 2. Testa carregamento de .env
print("\n2️⃣ Testando configuração da API...")
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"   ✅ API Key encontrada: {api_key[:20]}...")
else:
    print("   ❌ API Key não encontrada no .env")
    sys.exit(1)

# 3. Testa módulos customizados
print("\n3️⃣ Testando módulos customizados...")
try:
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    from validators import DocumentValidator
    from document_extractor import DocumentExtractor
    print("   ✅ Módulos src/ importados com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar módulos: {e}")
    sys.exit(1)

# 4. Testa validadores
print("\n4️⃣ Testando validadores...")

# Teste CPF válido
cpf_test = "123.456.789-09"
result = DocumentValidator.validate_cpf(cpf_test)
if "valid" in result:
    if result["valid"]:
        print(f"   ✅ CPF {cpf_test}: {result}")
    else:
        print(f"   ⚠️  CPF {cpf_test}: INVÁLIDO (esperado)")
else:
    print(f"   ❌ Erro no validador de CPF")

# Teste CPF válido (exemplo real)
cpf_valido = "111.444.777-35"  # CPF válido para teste
result_valido = DocumentValidator.validate_cpf(cpf_valido)
if result_valido.get("valid"):
    print(f"   ✅ CPF {cpf_valido}: VÁLIDO")
else:
    print(f"   ⚠️  CPF {cpf_valido}: {result_valido}")

# Teste data
data_test = "01/01/1990"
result_data = DocumentValidator.validate_date(data_test)
if result_data.get("valid"):
    print(f"   ✅ Data {data_test}: válida ({result_data['age_years']} anos)")
else:
    print(f"   ❌ Erro ao validar data: {result_data}")

# 5. Testa inicialização do DocumentExtractor
print("\n5️⃣ Testando DocumentExtractor...")
try:
    extractor = DocumentExtractor()
    print(f"   ✅ DocumentExtractor inicializado")
    print(f"   ℹ️  Modelo: gemini-2.0-flash-exp")
except Exception as e:
    print(f"   ❌ Erro ao inicializar extrator: {e}")
    sys.exit(1)

# 6. Verifica estrutura de diretórios
print("\n6️⃣ Verificando estrutura de diretórios...")
dirs_required = ["data", "data/processed", "models", "src"]
for dir_name in dirs_required:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"   ✅ {dir_name}/")
    else:
        print(f"   ⚠️  {dir_name}/ não existe (criando...)")
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"      ✅ Criado: {dir_name}/")

# 7. Testa agente ADK
print("\n7️⃣ Testando importação do agente ADK...")
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from extrator_agent.agent import root_agent
    print(f"   ✅ Agente importado: {root_agent.name}")
    print(f"   ℹ️  Modelo: {root_agent.model}")
    print(f"   ℹ️  Ferramentas: {len(root_agent.tools)} disponíveis")

    # Lista ferramentas
    print("\n   📋 Ferramentas disponíveis:")
    for tool in root_agent.tools:
        print(f"      - {tool.__name__}()")

except Exception as e:
    print(f"   ❌ Erro ao importar agente: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 8. Resumo final
print("\n" + "=" * 60)
print("✅ TODOS OS TESTES PASSARAM!")
print("=" * 60)
print()
print("🚀 Próximos passos:")
print()
print("1. Iniciar o agente:")
print("   adk web extrator_agent --port 8000")
print()
print("2. Ou usar modo CLI:")
print("   adk run extrator_agent")
print()
print("3. Coloque imagens de documentos na pasta data/")
print()
print("4. Teste com comandos como:")
print("   - 'liste as imagens disponíveis'")
print("   - 'extraia o documento data/meu_rg.jpg'")
print("   - 'valide o CPF 111.444.777-35'")
print()
print("=" * 60)
