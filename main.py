from openai import OpenAI

# IMPORT de configurações do .env
from dotenv import load_dotenv

# IMPORT classes automática
from pydantic import BaseModel

# IMPORT de conversão
from typing import Optional
from typing import List

# IMPORT de conversão de image
import base64

# IMPORT de conversão de json
import json

"""
{
  "sdtPessoaCompleto": {
    "Pessoa": {
      "PesNome": "string",
      "PesDataNascimento": null,
      "PesGenero": "string",
      "PesCpf": "string",
      "PesEmail": "string",
      "PesDddCelular": 0,
      "PesCelular": 0,
      "PesSobre": "string",
      "PesProfissao": "string",
      "PesPossuiAcessibilidade": "string",
      "TipAdaAceId": 0
    },
    "Endereco": {
      "PesEndCep": "string",
      "PesEndComplemento": "string",
      "PesEndNumero": "string"
    },
    "Formacoes": [
      {
        "TipForId": 0,
        "PesForStatus": "string",
        "PesForCurso": "string",
        "PesForInstituicao": "string",
        "PesForDataConclusao": null
      }
    ],
    "Experiencias": [
      {
        "PesExpProCargo": "string",
        "PesExpProEmpresa": "string",
        "PesExpProDescricaoAtividades": "string",
        "PesExpProDataInicio": null,
        "PesExpProDataFim": null,
        "PesExpProEmpregoAtual": true
      }
    ],
    "Links": [
      {
        "TipLinId": 0,
        "PesLinLink": "string"
      }
    ]
  }
}
"""

# Classes baseadas no meu json acima
class Pessoa(BaseModel):
    PesNome: Optional[str] = None
    PesDataNascimento: Optional[str] = None
    PesGenero: Optional[str] = None
    PesCpf: Optional[str] = None
    PesEmail: Optional[str] = None
    PesDddCelular: Optional[int] = None
    PesCelular: Optional[int] = None
    PesSobre: Optional[str] = None
    PesProfissao: Optional[str] = None
    PesPossuiAcessibilidade: Optional[str] = None
    TipAdaAceId: Optional[int] = None

# class Endereco(BaseModel):
#     PesEndCep: str
#     PesEndComplemento: str
#     PesEndNumero: str

# class Formacao(BaseModel):
#     TipForId: int
#     PesForStatus: str
#     PesForCurso: str
#     PesForInstituicao: str
#     PesForDataConclusao: Optional[str] = None

# class Experiencia(BaseModel):
#     PesExpProCargo: str
#     PesExpProEmpresa: str
#     PesExpProDescricaoAtividades: str
#     PesExpProDataInicio: Optional[str] = None
#     PesExpProDataFim: Optional[str] = None
#     PesExpProEmpregoAtual: bool

# class Link(BaseModel):
#     TipLinId: int
#     PesLinLink: str

# # Classe do .Parse
# class Curriculo(BaseModel):
#     Pessoa: Pessoa
#     Endereco: Endereco
#     Formacoes: List[Formacao]
#     Experiencias: List[Experiencia]
#     Links: List[Link]

# EXTRACTION_PROMPT = """Você é um analista de currículo (RH) especializado em extração de dados.
# Analise esta imagem (currículo) e extraia os seguintes dados em formato JSON.
# Não invente dados. Se não encontrar algo, use null (ou lista vazia quando fizer sentido).
# """

MODEL = "gpt-4.1-mini-2025-04-14"

EXTRACTION_PROMPT = """Você é um analista de currículo (RH) especializado em extração de dados.
Analise esta imagem (currículo) e extraia os seguintes dados em formato JSON.

{
  "sdtPessoaCompleto": {
    "Pessoa": {
      "PesNome": "string | null",
      "PesDataNascimento": "YYYY-MM-DD | null",
      "PesGenero": "string | null",
      "PesCpf": "string | null",
      "PesEmail": "string | null",
      "PesDddCelular": number | null,
      "PesCelular": number | null,
      "PesSobre": "string | null",
      "PesProfissao": "string | null",
      "PesPossuiAcessibilidade": "string | null",
      "TipAdaAceId": number | null
    },
    "Endereco": {
      "PesEndCep": "string | null",
      "PesEndComplemento": "string | null",
      "PesEndNumero": "string | null"
    },
    "Formacoes": [
      {
        "TipForId": number | null,
        "PesForStatus": "string | null",
        "PesForCurso": "string | null",
        "PesForInstituicao": "string | null",
        "PesForDataConclusao": null
      }
    ],
    "Experiencias": [
      {
        "PesExpProCargo": "string | null",
        "PesExpProEmpresa": "string | null",
        "PesExpProDescricaoAtividades": "string | null",
        "PesExpProDataInicio": null,
        "PesExpProDataFim": null,
        "PesExpProEmpregoAtual": true
      }
    ],
    "Links": [
      {
        "TipLinId": number | null,
        "PesLinLink": "string | null"
      }
    ]
  }
}

Retorne APENAS o JSON, sem texto adicional. Se não conseguir extrair algum campo, use null.
"""

# with open("imagem.jpg", "rb") as f:
#     file_bytes = f.read()
    
with open("profile.pdf", "rb") as f:
    file_bytes = f.read()

# mime_type = "image/jpeg"
mime_type = "application/pdf"

b64 = base64.b64encode(file_bytes).decode("utf-8")

# Carrega variável da open ia do .env
load_dotenv()

client = OpenAI()

response = client.responses.create(
    model=MODEL,
    input=[
      {
        "role": "system", 
        "content": EXTRACTION_PROMPT
      },
      {
        "role": "user",
        "content": 
        [
          # {"type": "input_text", "text": EXTRACTION_PROMPT},
          # {
          #   "type": "input_image",
          #   "image_url": f"data:{mime_type};base64,{b64}",
          # }
          {
              "type": "input_file",
              "filename": "profile.pdf",
              "file_data": f"data:{mime_type};base64,{b64}",
          }
        ],
      },  
    ],
    # text_format=Pessoa,
    temperature=0.1,
    max_output_tokens=2048,
)

# event = response.output_parsed

def __parse_json_response(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
    return json.loads(text.strip())

raw_text = response.output_text
data = json.dumps(__parse_json_response(raw_text), indent=2, ensure_ascii=False)

# print(event.model_dump_json(indent=2, ensure_ascii=False))

RULES_PROMPT = """
Sua tarefa é DEVOLVER O MESMO JSON, porém aplicando as regras:

REGRA FORMAÇÃO ACADÊMICA (TipForId)
Fundamental=1, Médio=2, Técnico=3, Superior=4, Pós=5, Mestrado=6, Doutorado=7, Não identificável=0

REGRA LINKS (TipLinId)
GitHub=1, LinkedIn=2, Portfólio=3

Instruções:
- Retorne APENAS o JSON (sem markdown, sem explicações).
- Não invente dados fora do que estiver no JSON de entrada.
- Se der para inferir TipLinId pelo link (ex: contém "linkedin.com"), preencha.
- Se não der para inferir TipForId com segurança, use 0.
"""

response = client.responses.create(
    model=MODEL,
    input=[
      {
        "role": "system", 
        "content": RULES_PROMPT
      },
      {
        "role": "user", 
        "content": data
      } 
    ],
    temperature=0.3,
    max_output_tokens=2048,
)

print(response.output_text)