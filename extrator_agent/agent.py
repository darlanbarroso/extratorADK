"""
ExtratorADK Agent - Extração de Documentos Brasileiros (RG, CNH, CPF)
Powered by Google ADK e Gemini Vision 2.0 Flash
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Dict, Any
from loguru import logger

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from document_extractor import DocumentExtractor
from validators import DocumentValidator

# Inicializa extrator e validador
extractor = DocumentExtractor()
validator = DocumentValidator()

# ==================== FERRAMENTAS DE EXTRAÇÃO ====================

def extract_rg(image_path: str, validate: bool = True) -> Dict[str, Any]:
    """
    Extrai dados de um RG brasileiro.

    Args:
        image_path: Caminho para a imagem do RG
        validate: Se True, valida os dados extraídos

    Returns:
        Dict com dados extraídos e validações
    """
    try:
        logger.info(f"Extraindo RG: {image_path}")
        result = extractor.extract_rg(image_path)

        if result["status"] == "error":
            return result

        # Validação opcional
        if validate and result.get("data"):
            data = result["data"]
            validations = {}

            # Valida CPF se presente
            if data.get("cpf"):
                validations["cpf"] = validator.validate_cpf(data["cpf"])

            # Valida data de nascimento
            if data.get("data_nascimento"):
                validations["data_nascimento"] = validator.validate_date(data["data_nascimento"])

            # Valida data de emissão
            if data.get("data_emissao"):
                validations["data_emissao"] = validator.validate_date(data["data_emissao"])

            # Valida RG
            if data.get("numero_rg"):
                validations["rg"] = validator.validate_rg(
                    data["numero_rg"],
                    data.get("uf_emissor")
                )

            result["validations"] = validations

        return result

    except Exception as e:
        logger.error(f"Erro ao extrair RG: {e}")
        return {
            "status": "error",
            "message": f"Erro ao extrair RG: {str(e)}"
        }


def extract_cnh(image_path: str, validate: bool = True) -> Dict[str, Any]:
    """
    Extrai dados de uma CNH brasileira.

    Args:
        image_path: Caminho para a imagem da CNH
        validate: Se True, valida os dados extraídos

    Returns:
        Dict com dados extraídos e validações
    """
    try:
        logger.info(f"Extraindo CNH: {image_path}")
        result = extractor.extract_cnh(image_path)

        if result["status"] == "error":
            return result

        # Validação opcional
        if validate and result.get("data"):
            data = result["data"]
            validations = {}

            # Valida CNH
            if data.get("numero_registro"):
                validations["cnh"] = validator.validate_cnh(data["numero_registro"])

            # Valida CPF
            if data.get("cpf"):
                validations["cpf"] = validator.validate_cpf(data["cpf"])

            # Valida data de nascimento
            if data.get("data_nascimento"):
                validations["data_nascimento"] = validator.validate_date(data["data_nascimento"])

            # Valida datas de emissão e validade
            if data.get("data_emissao") and data.get("data_validade"):
                validations["validade_cnh"] = validator.validate_cnh_expiration(
                    data["data_emissao"],
                    data["data_validade"]
                )

            result["validations"] = validations

        return result

    except Exception as e:
        logger.error(f"Erro ao extrair CNH: {e}")
        return {
            "status": "error",
            "message": f"Erro ao extrair CNH: {str(e)}"
        }


def extract_cpf_document(image_path: str, validate: bool = True) -> Dict[str, Any]:
    """
    Extrai dados de um documento de CPF.

    Args:
        image_path: Caminho para a imagem do CPF
        validate: Se True, valida os dados extraídos

    Returns:
        Dict com dados extraídos e validações
    """
    try:
        logger.info(f"Extraindo CPF: {image_path}")
        result = extractor.extract_cpf(image_path)

        if result["status"] == "error":
            return result

        # Validação opcional
        if validate and result.get("data"):
            data = result["data"]
            validations = {}

            # Valida CPF
            if data.get("numero_cpf"):
                validations["cpf"] = validator.validate_cpf(data["numero_cpf"])

            # Valida data de nascimento
            if data.get("data_nascimento"):
                validations["data_nascimento"] = validator.validate_date(data["data_nascimento"])

            result["validations"] = validations

        return result

    except Exception as e:
        logger.error(f"Erro ao extrair CPF: {e}")
        return {
            "status": "error",
            "message": f"Erro ao extrair CPF: {str(e)}"
        }


def extract_cnpj_document(image_path: str, validate: bool = True) -> Dict[str, Any]:
    """
    Extrai dados de um Cartão CNPJ.

    Args:
        image_path: Caminho para a imagem do CNPJ
        validate: Se True, valida os dados extraídos

    Returns:
        Dict com dados extraídos e validações
    """
    try:
        logger.info(f"Extraindo CNPJ: {image_path}")
        result = extractor.extract_cnpj(image_path)

        if result["status"] == "error":
            return result

        # Validação opcional
        if validate and result.get("data"):
            data = result["data"]
            validations = {}

            # Valida CNPJ
            if data.get("numero_cnpj"):
                validations["cnpj"] = validator.validate_cnpj(data["numero_cnpj"])

            # Valida data de abertura
            if data.get("data_abertura"):
                validations["data_abertura"] = validator.validate_date(data["data_abertura"])

            # Valida data de situação cadastral
            if data.get("data_situacao_cadastral"):
                validations["data_situacao_cadastral"] = validator.validate_date(data["data_situacao_cadastral"])

            result["validations"] = validations

        return result

    except Exception as e:
        logger.error(f"Erro ao extrair CNPJ: {e}")
        return {
            "status": "error",
            "message": f"Erro ao extrair CNPJ: {str(e)}"
        }


def extract_document_auto(image_path: str, validate: bool = True) -> Dict[str, Any]:
    """
    Detecta automaticamente o tipo de documento e extrai dados.

    Args:
        image_path: Caminho para a imagem do documento
        validate: Se True, valida os dados extraídos

    Returns:
        Dict com dados extraídos e validações
    """
    try:
        logger.info(f"Extraindo documento (auto-detect): {image_path}")
        result = extractor.extract_from_image(image_path, "auto")

        if result["status"] == "error":
            return result

        # Identifica tipo e executa validação apropriada
        if validate and result.get("data"):
            doc_type = result["data"].get("tipo_documento", "").upper()

            if doc_type == "RG":
                return extract_rg(image_path, validate=True)
            elif doc_type == "CNH":
                return extract_cnh(image_path, validate=True)
            elif doc_type == "CPF":
                return extract_cpf_document(image_path, validate=True)
            elif doc_type == "CNPJ":
                return extract_cnpj_document(image_path, validate=True)

        return result

    except Exception as e:
        logger.error(f"Erro ao extrair documento: {e}")
        return {
            "status": "error",
            "message": f"Erro ao extrair documento: {str(e)}"
        }


def list_images(directory: str = "data") -> Dict[str, Any]:
    """
    Lista imagens de documentos em um diretório.

    Args:
        directory: Diretório para listar imagens

    Returns:
        Dict com lista de imagens
    """
    try:
        logger.info(f"Listando imagens em: {directory}")
        path = Path(directory)

        if not path.exists():
            return {
                "status": "error",
                "message": f"Diretório não encontrado: {directory}"
            }

        # Busca imagens
        extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]
        images = []

        for ext in extensions:
            images.extend([str(f) for f in path.rglob(f"*{ext}")])

        return {
            "status": "success",
            "message": f"Encontradas {len(images)} imagens",
            "images": images,
            "count": len(images)
        }
    except Exception as e:
        logger.error(f"Erro ao listar imagens: {e}")
        return {
            "status": "error",
            "message": f"Erro ao listar imagens: {str(e)}"
        }


def save_extraction(data: Dict[str, Any], output_file: str) -> Dict[str, Any]:
    """
    Salva resultado de extração em arquivo JSON.

    Args:
        data: Dados extraídos
        output_file: Caminho do arquivo de saída

    Returns:
        Dict com status da operação
    """
    try:
        logger.info(f"Salvando extração em: {output_file}")
        import json

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {
            "status": "success",
            "message": f"Dados salvos em: {output_file}",
            "path": str(output_path)
        }
    except Exception as e:
        logger.error(f"Erro ao salvar extração: {e}")
        return {
            "status": "error",
            "message": f"Erro ao salvar extração: {str(e)}"
        }


def validate_cpf_number(cpf: str) -> Dict[str, Any]:
    """
    Valida um número de CPF.

    Args:
        cpf: Número do CPF (com ou sem formatação)

    Returns:
        Dict com resultado da validação
    """
    return validator.validate_cpf(cpf)


def validate_cnh_number(cnh: str) -> Dict[str, Any]:
    """
    Valida um número de CNH.

    Args:
        cnh: Número da CNH

    Returns:
        Dict com resultado da validação
    """
    return validator.validate_cnh(cnh)


def validate_cnpj_number(cnpj: str) -> Dict[str, Any]:
    """
    Valida um número de CNPJ.

    Args:
        cnpj: Número do CNPJ (com ou sem formatação)

    Returns:
        Dict com resultado da validação
    """
    return validator.validate_cnpj(cnpj)


# ==================== DEFINIÇÃO DO AGENTE ====================

from google.adk.agents import Agent

root_agent = Agent(
    name="extrator_agent",
    model="gemini-2.5-flash",
    description=(
        "Agente especializado em extração de documentos brasileiros "
        "(RG, CNH, CPF e CNPJ) usando OCR e IA. Extrai dados estruturados e valida informações."
    ),
    instruction=(
        "Você é um assistente especializado em EXTRAÇÃO DE DOCUMENTOS BRASILEIROS.\n\n"

        "🎯 **ESPECIALIDADE:** RG, CNH, CPF e CNPJ\n\n"

        "📸 **ANÁLISE MULTIMODAL:**\n\n"
        "Você tem capacidade NATIVA de analisar imagens enviadas no chat!\n"
        "- Quando o usuário enviar uma imagem de documento (RG, CNH, CPF, CNPJ), você PODE analisá-la DIRETAMENTE\n"
        "- Use suas capacidades de visão para extrair TODOS os dados visíveis\n"
        "- Identifique automaticamente o tipo de documento (RG, CNH, CPF ou CNPJ)\n"
        "- Após extrair os dados da imagem, USE AS FERRAMENTAS DE VALIDAÇÃO\n\n"

        "🔧 **FERRAMENTAS DISPONÍVEIS:**\n\n"

        "**1. EXTRAÇÃO DE ARQUIVOS LOCAIS:**\n"
        "- extract_rg(image_path, validate=True): Extrai dados de RG de arquivo\n"
        "- extract_cnh(image_path, validate=True): Extrai dados de CNH de arquivo\n"
        "- extract_cpf_document(image_path, validate=True): Extrai dados de CPF de arquivo\n"
        "- extract_cnpj_document(image_path, validate=True): Extrai dados de CNPJ de arquivo\n"
        "- extract_document_auto(image_path, validate=True): Auto-detecta tipo e extrai de arquivo\n"
        "- list_images(directory): Lista imagens disponíveis no sistema\n\n"

        "**2. VALIDAÇÃO DE DADOS:**\n"
        "- validate_cpf_number(cpf): Valida CPF (calcula dígitos verificadores)\n"
        "- validate_cnh_number(cnh): Valida CNH (verifica dígitos)\n"
        "- validate_cnpj_number(cnpj): Valida CNPJ (verifica dígitos verificadores)\n\n"

        "**3. GERENCIAMENTO:**\n"
        "- save_extraction(data, output_file): Salva resultados em JSON\n\n"

        "📋 **WORKFLOW PARA IMAGENS NO CHAT:**\n\n"
        "Quando o usuário enviar uma imagem de documento:\n\n"
        "1️⃣ Analise a imagem DIRETAMENTE com sua visão\n"
        "2️⃣ Identifique o tipo de documento (RG, CNH, CPF ou CNPJ)\n"
        "3️⃣ Extraia TODOS os campos visíveis (nome, números, datas, endereço, etc.)\n"
        "4️⃣ IMPORTANTE: Use as ferramentas de validação:\n"
        "   - validate_cpf_number() para validar CPF\n"
        "   - validate_cnh_number() para validar CNH\n"
        "   - validate_cnpj_number() para validar CNPJ\n"
        "5️⃣ Apresente os resultados formatados\n\n"

        "📋 **EXEMPLOS DE USO:**\n\n"
        "🖼️ IMAGEM NO CHAT:\n"
        "   Usuário: [envia imagem de CNH]\n"
        "   Você: Analisa a imagem → Extrai dados → validate_cnh_number() → Apresenta resultado\n\n"
        "   Usuário: [envia imagem de Cartão CNPJ]\n"
        "   Você: Analisa a imagem → Extrai dados → validate_cnpj_number() → Apresenta resultado\n\n"

        "📁 ARQUIVO LOCAL:\n"
        "   'extraia o RG data/rg.jpg' → extract_rg('data/rg.jpg')\n"
        "   'processe a CNH cnh_joao.png' → extract_cnh('data/cnh_joao.png')\n"
        "   'extraia o CNPJ data/cartao_cnpj.jpg' → extract_cnpj_document('data/cartao_cnpj.jpg')\n\n"

        "✅ VALIDAÇÃO:\n"
        "   'valide o CPF 123.456.789-09' → validate_cpf_number('123.456.789-09')\n"
        "   'valide o CNPJ 11.222.333/0001-81' → validate_cnpj_number('11.222.333/0001-81')\n\n"

        "⚙️ **COMPORTAMENTO:**\n\n"
        "- SEMPRE analise imagens enviadas diretamente no chat usando sua visão\n"
        "- SEMPRE valide CPF, CNH e CNPJ extraídos usando as ferramentas\n"
        "- Mostre dados extraídos E validações de forma clara\n"
        "- Se validação falhar, explique o erro\n"
        "- Para CNH, verifique se está vencida\n"
        "- Seja preciso com formatação (CPF: XXX.XXX.XXX-XX, CNPJ: XX.XXX.XXX/XXXX-XX)\n\n"

        "🎨 **FORMATO DE RESPOSTA:**\n\n"
        "✅ DADOS EXTRAÍDOS (CNH):\n"
        "- Tipo: CNH\n"
        "- Nome: João da Silva\n"
        "- CPF: 123.456.789-09\n"
        "- CNH: 12345678901\n"
        "- Categoria: AB\n"
        "- Validade: 01/01/2026\n\n"
        "🔍 VALIDAÇÕES:\n"
        "- CPF: ✅ Válido\n"
        "- CNH: ✅ Válida\n"
        "- Validade: ⚠️ Vence em 45 dias\n\n"

        "✅ DADOS EXTRAÍDOS (CNPJ):\n"
        "- Tipo: CNPJ\n"
        "- CNPJ: 11.222.333/0001-81\n"
        "- Razão Social: EMPRESA EXEMPLO LTDA\n"
        "- Nome Fantasia: EMPRESA EXEMPLO\n"
        "- Situação: ATIVA\n"
        "- Endereço: Rua Exemplo, 123 - Bairro - Cidade/UF\n\n"
        "🔍 VALIDAÇÕES:\n"
        "- CNPJ: ✅ Válido\n"
        "- Data Abertura: ✅ Válida\n\n"

        "Seja preciso, profissional e sempre valide os dados extraídos!\n"
    ),
    tools=[
        extract_rg,
        extract_cnh,
        extract_cpf_document,
        extract_cnpj_document,
        extract_document_auto,
        list_images,
        save_extraction,
        validate_cpf_number,
        validate_cnh_number,
        validate_cnpj_number,
    ],
)
