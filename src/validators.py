"""
Validadores para documentos brasileiros (CPF, CNH, RG, datas)
"""
from datetime import datetime
from typing import Optional, Dict, Any
import re


class DocumentValidator:
    """Validador de documentos brasileiros"""

    @staticmethod
    def validate_cpf(cpf: str) -> Dict[str, Any]:
        """
        Valida CPF brasileiro.

        Args:
            cpf: CPF no formato XXX.XXX.XXX-XX ou apenas números

        Returns:
            Dict com status e CPF formatado
        """
        # Remove caracteres não numéricos
        cpf_numbers = re.sub(r'\D', '', cpf)

        if len(cpf_numbers) != 11:
            return {
                "valid": False,
                "error": "CPF deve ter 11 dígitos",
                "cpf": cpf
            }

        # Verifica se todos os dígitos são iguais
        if cpf_numbers == cpf_numbers[0] * 11:
            return {
                "valid": False,
                "error": "CPF inválido (dígitos repetidos)",
                "cpf": cpf
            }

        # Calcula primeiro dígito verificador
        soma = sum(int(cpf_numbers[i]) * (10 - i) for i in range(9))
        primeiro_digito = 11 - (soma % 11)
        if primeiro_digito >= 10:
            primeiro_digito = 0

        # Calcula segundo dígito verificador
        soma = sum(int(cpf_numbers[i]) * (11 - i) for i in range(10))
        segundo_digito = 11 - (soma % 11)
        if segundo_digito >= 10:
            segundo_digito = 0

        # Valida dígitos verificadores
        if int(cpf_numbers[9]) != primeiro_digito or int(cpf_numbers[10]) != segundo_digito:
            return {
                "valid": False,
                "error": "Dígitos verificadores inválidos",
                "cpf": cpf,
                "expected": f"{cpf_numbers[:9]}{primeiro_digito}{segundo_digito}"
            }

        # Formata CPF
        cpf_formatado = f"{cpf_numbers[:3]}.{cpf_numbers[3:6]}.{cpf_numbers[6:9]}-{cpf_numbers[9:]}"

        return {
            "valid": True,
            "cpf": cpf_numbers,
            "formatted": cpf_formatado
        }

    @staticmethod
    def validate_cnpj(cnpj: str) -> Dict[str, Any]:
        """
        Valida CNPJ brasileiro.

        Args:
            cnpj: CNPJ no formato XX.XXX.XXX/XXXX-XX ou apenas números

        Returns:
            Dict com status e CNPJ formatado
        """
        # Remove caracteres não numéricos
        cnpj_numbers = re.sub(r'\D', '', cnpj)

        if len(cnpj_numbers) != 14:
            return {
                "valid": False,
                "error": "CNPJ deve ter 14 dígitos",
                "cnpj": cnpj
            }

        # Verifica se todos os dígitos são iguais
        if cnpj_numbers == cnpj_numbers[0] * 14:
            return {
                "valid": False,
                "error": "CNPJ inválido (dígitos repetidos)",
                "cnpj": cnpj
            }

        # Calcula primeiro dígito verificador
        peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj_numbers[i]) * peso1[i] for i in range(12))
        resto = soma % 11
        primeiro_digito = 0 if resto < 2 else 11 - resto

        # Calcula segundo dígito verificador
        peso2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj_numbers[i]) * peso2[i] for i in range(13))
        resto = soma % 11
        segundo_digito = 0 if resto < 2 else 11 - resto

        # Valida dígitos verificadores
        if int(cnpj_numbers[12]) != primeiro_digito or int(cnpj_numbers[13]) != segundo_digito:
            return {
                "valid": False,
                "error": "Dígitos verificadores inválidos",
                "cnpj": cnpj,
                "expected": f"{cnpj_numbers[:12]}{primeiro_digito}{segundo_digito}"
            }

        # Formata CNPJ
        cnpj_formatado = f"{cnpj_numbers[:2]}.{cnpj_numbers[2:5]}.{cnpj_numbers[5:8]}/{cnpj_numbers[8:12]}-{cnpj_numbers[12:]}"

        return {
            "valid": True,
            "cnpj": cnpj_numbers,
            "formatted": cnpj_formatado
        }

    @staticmethod
    def validate_cnh(cnh: str) -> Dict[str, Any]:
        """
        Valida CNH brasileira.

        Args:
            cnh: CNH com 11 dígitos

        Returns:
            Dict com status e CNH validada
        """
        # Remove caracteres não numéricos
        cnh_numbers = re.sub(r'\D', '', cnh)

        if len(cnh_numbers) != 11:
            return {
                "valid": False,
                "error": "CNH deve ter 11 dígitos",
                "cnh": cnh
            }

        # Verifica se todos os dígitos são iguais
        if cnh_numbers == cnh_numbers[0] * 11:
            return {
                "valid": False,
                "error": "CNH inválida (dígitos repetidos)",
                "cnh": cnh
            }

        # Calcula primeiro dígito verificador
        dsc = 0
        v = 0
        for i in range(9):
            v += int(cnh_numbers[i]) * (9 - i)

        dsc = v % 11
        primeiro_digito = 0 if dsc >= 10 else dsc

        # Calcula segundo dígito verificador
        v = 0
        for i in range(9):
            v += int(cnh_numbers[i]) * (1 + i)

        dsc = v % 11
        segundo_digito = 0 if dsc >= 10 else dsc

        # Valida dígitos verificadores
        if int(cnh_numbers[9]) != primeiro_digito or int(cnh_numbers[10]) != segundo_digito:
            return {
                "valid": False,
                "error": "Dígitos verificadores inválidos",
                "cnh": cnh,
                "expected": f"{cnh_numbers[:9]}{primeiro_digito}{segundo_digito}"
            }

        return {
            "valid": True,
            "cnh": cnh_numbers
        }

    @staticmethod
    def validate_date(date_str: str, date_format: str = "%d/%m/%Y") -> Dict[str, Any]:
        """
        Valida e parseia uma data.

        Args:
            date_str: Data no formato string
            date_format: Formato esperado da data

        Returns:
            Dict com status e data parseada
        """
        if not date_str:
            return {
                "valid": False,
                "error": "Data não fornecida",
                "date": None
            }

        try:
            date_obj = datetime.strptime(date_str.strip(), date_format)

            # Verifica se a data não é futura (para nascimento/emissão)
            hoje = datetime.now()

            return {
                "valid": True,
                "date": date_obj.strftime("%Y-%m-%d"),
                "formatted": date_str,
                "is_future": date_obj > hoje,
                "age_years": (hoje - date_obj).days // 365 if date_obj < hoje else 0
            }

        except ValueError:
            return {
                "valid": False,
                "error": f"Data inválida ou formato incorreto. Esperado: {date_format}",
                "date": date_str
            }

    @staticmethod
    def validate_rg(rg: str, uf: Optional[str] = None) -> Dict[str, Any]:
        """
        Valida RG brasileiro (validação básica).

        Args:
            rg: Número do RG
            uf: UF de emissão (opcional)

        Returns:
            Dict com status do RG
        """
        # Remove caracteres não numéricos
        rg_numbers = re.sub(r'\D', '', rg)

        if len(rg_numbers) < 5 or len(rg_numbers) > 9:
            return {
                "valid": False,
                "error": "RG deve ter entre 5 e 9 dígitos",
                "rg": rg
            }

        # Validação básica (RG não tem algoritmo verificador universal no Brasil)
        return {
            "valid": True,
            "rg": rg_numbers,
            "uf": uf,
            "note": "Validação básica de formato. RG não possui dígito verificador universal."
        }

    @staticmethod
    def validate_cnh_expiration(emissao: str, validade: str) -> Dict[str, Any]:
        """
        Valida se a data de validade da CNH é coerente com a emissão.

        Args:
            emissao: Data de emissão
            validade: Data de validade

        Returns:
            Dict com análise das datas
        """
        emissao_result = DocumentValidator.validate_date(emissao)
        validade_result = DocumentValidator.validate_date(validade)

        if not emissao_result["valid"] or not validade_result["valid"]:
            return {
                "valid": False,
                "error": "Datas inválidas",
                "emissao": emissao_result,
                "validade": validade_result
            }

        emissao_date = datetime.strptime(emissao_result["date"], "%Y-%m-%d")
        validade_date = datetime.strptime(validade_result["date"], "%Y-%m-%d")

        if validade_date <= emissao_date:
            return {
                "valid": False,
                "error": "Data de validade deve ser posterior à emissão",
                "emissao": emissao_result,
                "validade": validade_result
            }

        # Verifica se está vencida
        hoje = datetime.now()
        dias_para_vencer = (validade_date - hoje).days

        return {
            "valid": True,
            "emissao": emissao_result,
            "validade": validade_result,
            "status": "vencida" if dias_para_vencer < 0 else "válida",
            "dias_para_vencer": dias_para_vencer if dias_para_vencer > 0 else 0,
            "vencida": dias_para_vencer < 0
        }
