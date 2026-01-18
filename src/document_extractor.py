"""
Extrator de Documentos Brasileiros usando Gemini Vision 2.0 Flash
Suporta: RG, CNH, CPF
"""
import os
import base64
from pathlib import Path
from typing import Dict, Any, Optional
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from loguru import logger

# Carrega variáveis de ambiente
load_dotenv()

# Configura Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")

genai.configure(api_key=GOOGLE_API_KEY)


class DocumentExtractor:
    """Extrator de documentos brasileiros usando Gemini Vision"""

    # Prompts especializados para cada tipo de documento
    PROMPTS = {
        "rg": """
Analise esta imagem de um RG (Registro Geral) brasileiro e extraia TODAS as informações visíveis.

Retorne um JSON com a seguinte estrutura (preencha apenas os campos visíveis):

{
  "tipo_documento": "RG",
  "numero_rg": "XX.XXX.XXX-X",
  "orgao_emissor": "SSP",
  "uf_emissor": "SP",
  "data_emissao": "DD/MM/AAAA",
  "nome_completo": "Nome completo",
  "data_nascimento": "DD/MM/AAAA",
  "filiacao_pai": "Nome do pai",
  "filiacao_mae": "Nome da mãe",
  "naturalidade": "Cidade - UF",
  "cpf": "XXX.XXX.XXX-XX",
  "observacoes": "Qualquer informação adicional"
}

INSTRUÇÕES:
- Extraia apenas texto visível e legível
- Mantenha formatação original (pontos, traços)
- Se um campo não estiver visível, use null
- Seja preciso com datas (formato DD/MM/AAAA)
- Retorne APENAS o JSON, sem explicações
""",

        "cnh": """
Analise esta imagem de uma CNH (Carteira Nacional de Habilitação) brasileira e extraia TODAS as informações visíveis.

Retorne um JSON com a seguinte estrutura:

{
  "tipo_documento": "CNH",
  "numero_registro": "XXXXXXXXXXX",
  "numero_espelho": "XXXXXXXXXXX",
  "nome_completo": "Nome completo",
  "data_nascimento": "DD/MM/AAAA",
  "cpf": "XXX.XXX.XXX-XX",
  "filiacao_pai": "Nome do pai",
  "filiacao_mae": "Nome da mãe",
  "data_primeira_habilitacao": "DD/MM/AAAA",
  "data_emissao": "DD/MM/AAAA",
  "data_validade": "DD/MM/AAAA",
  "categoria": "AB",
  "local_emissao": "Cidade - UF",
  "orgao_emissor": "DETRAN/XX",
  "numero_seguranca": "XXXXXXXXX",
  "observacoes": "Ex: EAR, OD, etc",
  "restricoes": "Restrições médicas ou de uso"
}

INSTRUÇÕES:
- Extraia apenas texto visível e legível
- A CNH tem informações frente e verso - extraia tudo que conseguir ver
- Mantenha formatação original de números
- Se um campo não estiver visível, use null
- Retorne APENAS o JSON, sem explicações
""",

        "cpf": """
Analise esta imagem de um CPF (Cadastro de Pessoa Física) brasileiro e extraia as informações.

Retorne um JSON com a seguinte estrutura:

{
  "tipo_documento": "CPF",
  "numero_cpf": "XXX.XXX.XXX-XX",
  "nome_completo": "Nome completo",
  "data_nascimento": "DD/MM/AAAA",
  "situacao_cadastral": "Regular/Pendente/Suspensa/Cancelada/Nula",
  "data_inscricao": "DD/MM/AAAA",
  "observacoes": "Informações adicionais"
}

INSTRUÇÕES:
- Extraia apenas texto visível e legível
- O CPF deve estar no formato XXX.XXX.XXX-XX
- Se um campo não estiver visível, use null
- Retorne APENAS o JSON, sem explicações
""",

        "auto": """
Analise esta imagem de um documento de identidade brasileiro e:

1. IDENTIFIQUE o tipo de documento (RG, CNH ou CPF)
2. EXTRAIA todas as informações visíveis

Retorne um JSON com a estrutura apropriada ao documento identificado.

Para RG, CNH ou CPF, use as estruturas de dados padrão de cada documento.

INSTRUÇÕES:
- Primeiro identifique qual tipo de documento é
- Extraia todos os campos visíveis
- Mantenha formatação original
- Use null para campos não visíveis
- Retorne APENAS o JSON, sem explicações
"""
    }

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Inicializa o extrator.

        Args:
            model_name: Nome do modelo Gemini a usar
        """
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"DocumentExtractor inicializado com modelo: {model_name}")

    def extract_from_image(
        self,
        image_path: str,
        document_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Extrai informações de uma imagem de documento.

        Args:
            image_path: Caminho para a imagem
            document_type: Tipo do documento ("rg", "cnh", "cpf", "auto")

        Returns:
            Dict com dados extraídos
        """
        try:
            # Valida caminho
            path = Path(image_path)
            if not path.exists():
                return {
                    "status": "error",
                    "message": f"Arquivo não encontrado: {image_path}"
                }

            # Abre imagem
            logger.info(f"Processando imagem: {image_path}")
            image = Image.open(path)

            # Seleciona prompt apropriado
            prompt = self.PROMPTS.get(document_type.lower(), self.PROMPTS["auto"])

            # Envia para Gemini Vision
            logger.info(f"Enviando para Gemini Vision (tipo: {document_type})")
            response = self.model.generate_content([prompt, image])

            # Extrai texto da resposta
            extracted_text = response.text.strip()

            # Tenta parsear como JSON
            import json

            # Remove markdown code blocks se existirem
            if extracted_text.startswith("```"):
                extracted_text = extracted_text.split("```")[1]
                if extracted_text.startswith("json"):
                    extracted_text = extracted_text[4:]
                extracted_text = extracted_text.strip()

            try:
                extracted_data = json.loads(extracted_text)
            except json.JSONDecodeError:
                # Se não conseguir parsear, retorna como texto
                extracted_data = {
                    "raw_text": extracted_text,
                    "note": "Resposta não estava em formato JSON válido"
                }

            logger.info(f"Extração concluída com sucesso")

            return {
                "status": "success",
                "message": "Documento processado com sucesso",
                "image_path": str(path),
                "document_type": document_type,
                "data": extracted_data,
                "raw_response": extracted_text
            }

        except Exception as e:
            logger.error(f"Erro ao extrair documento: {e}")
            return {
                "status": "error",
                "message": f"Erro ao processar documento: {str(e)}",
                "image_path": image_path
            }

    def extract_rg(self, image_path: str) -> Dict[str, Any]:
        """Extrai dados de um RG"""
        return self.extract_from_image(image_path, "rg")

    def extract_cnh(self, image_path: str) -> Dict[str, Any]:
        """Extrai dados de uma CNH"""
        return self.extract_from_image(image_path, "cnh")

    def extract_cpf(self, image_path: str) -> Dict[str, Any]:
        """Extrai dados de um CPF"""
        return self.extract_from_image(image_path, "cpf")

    def extract_batch(self, image_paths: list, document_type: str = "auto") -> Dict[str, Any]:
        """
        Processa múltiplas imagens em lote.

        Args:
            image_paths: Lista de caminhos de imagens
            document_type: Tipo do documento

        Returns:
            Dict com resultados de todos os documentos
        """
        results = []
        errors = []

        logger.info(f"Processando {len(image_paths)} documentos em lote")

        for image_path in image_paths:
            result = self.extract_from_image(image_path, document_type)

            if result["status"] == "success":
                results.append(result)
            else:
                errors.append(result)

        return {
            "status": "completed",
            "total": len(image_paths),
            "success": len(results),
            "errors": len(errors),
            "results": results,
            "error_details": errors
        }
