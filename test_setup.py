#!/usr/bin/env python3
"""
Script de teste para verificar a instalação do ExtratorADK
"""
import sys
from pathlib import Path

def test_structure():
    """Verifica estrutura de diretórios"""
    print("🔍 Verificando estrutura de diretórios...")
    
    required_dirs = [
        "extrator_agent",
        "src/data",
        "src/models",
        "src/agents/adk_tools",
        "config",
        "data/processed",
        "models",
        "tests"
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)
    
    if missing:
        print(f"❌ Diretórios faltando: {', '.join(missing)}")
        return False
    
    print("✅ Estrutura de diretórios OK")
    return True


def test_files():
    """Verifica arquivos essenciais"""
    print("\n🔍 Verificando arquivos essenciais...")
    
    required_files = [
        "extrator_agent/__init__.py",
        "extrator_agent/agent.py",
        ".env",
        ".gitignore",
        "requirements.txt",
        "README.md"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"❌ Arquivos faltando: {', '.join(missing)}")
        return False
    
    print("✅ Arquivos essenciais OK")
    return True


def test_env():
    """Verifica configuração do .env"""
    print("\n🔍 Verificando arquivo .env...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Arquivo .env não encontrado")
        return False
    
    content = env_path.read_text()
    
    if "GOOGLE_API_KEY" not in content:
        print("❌ GOOGLE_API_KEY não encontrada no .env")
        return False
    
    if "AIzaSyBRruCqweQpdw2nAeaHQgqQ3HGGbosj4aI" in content:
        print("✅ API Key configurada")
    else:
        print("⚠️  API Key diferente da esperada (pode estar OK)")
    
    print("✅ Arquivo .env OK")
    return True


def test_agent_import():
    """Testa importação do agente"""
    print("\n🔍 Testando importação do agente...")
    
    try:
        from extrator_agent import root_agent
        print(f"✅ Agente importado: {root_agent.name}")
        print(f"   Modelo: {root_agent.model}")
        print(f"   Ferramentas: {len(root_agent.tools)} disponíveis")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar agente: {e}")
        print("   Execute: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("ExtratorADK - Teste de Instalação")
    print("=" * 60)
    
    tests = [
        test_structure,
        test_files,
        test_env,
        test_agent_import
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\nPróximos passos:")
        print("  1. Ative o ambiente virtual: source .venv/bin/activate")
        print("  2. Instale dependências: pip install -r requirements.txt")
        print("  3. Inicie o agente: adk web extrator_agent --port 8000")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("\nConsulte o QUICKSTART.md para ajuda")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
