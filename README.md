# PowerOfData 

API desenvolvida como parte do desafio técnico para a vaga de Desenvolvedor Back-end Python na POWER DATA TECNOLOGIA ANALITICA LTDA .
O objetivo da aplicação é fornecer uma interface para consulta de dados da saga Star Wars, utilizando a SWAPI como fonte externa, com suporte a filtros, ordenação, paginação e cache.

---

## Tecnologias usadas
- Python 3.8
- Flask
- Pytest
- SWAPI (https://swapi.dev)

---

## Como rodar o projeto localmente
### 1. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

### 2. Instalar dependências
pip install -r requirements.txt

### 3. Executar a aplicação
FLASK_APP=src.app flask run --port 8080

# API ficará disponível em:
http://127.0.0.1:8080

# Endpoints disponíveis
Health check
GET /health

# Consulta de dados da SWAPI
GET /v1/swapi

#Parâmetros suportados

resource (obrigatório): people, planets, films, starships, species, vehicles
q: termo de busca
sort: campo para ordenação
order: asc | desc
page: número da página
page_size: quantidade de itens por página
Filtros adicionais via query params (ex: gender=male)

# Exemplos de uso
/v1/swapi?resource=people&q=luke
/v1/swapi?resource=people&q=a&gender=male
/v1/swapi?resource=planets&q=a&sort=name&order=asc&page_size=5

# Cache
As chamadas à SWAPI utilizam um cache simples em memória com TTL de 5 minutos.
O comportamento do cache pode ser observado através do header de resposta:
X-Cache: MISS | HIT

# Testes
Os testes unitários cobrem as regras de filtro, ordenação e paginação.

Para executá-los:
pytest

### Observações
As decisões técnicas e limitações conhecidas estão documentadas em docs/DECISIONS.md.

## Autenticação (API Key)

O endpoint `/v1/swapi` possui um controle simples de acesso baseado em API Key.
Copie o arquivo `.env.example` para `.env` e configure sua chave.


### Como configurar

Defina a variável de ambiente antes de iniciar a aplicação:

## Linux / Mac:
export API_KEY="minha-chave-local"
FLASK_APP=src.app flask run --port 8080

### Windows (PowerShell)

```powershell
$env:API_KEY="minha-chave-local"
flask run --port 8080
```

---

## Considerações para ambiente de produção
---

## Considerações para ambiente de produção

### Cache

Atualmente o cache é mantido em memória da aplicação.  
Em um ambiente com múltiplas instâncias isso não seria compartilhado.

Uma evolução natural seria utilizar:

- Redis
- Memcached
- Azure Cache for Redis
- AWS ElastiCache

---

### Deploy

A aplicação poderia ser executada em:

- Containers Docker

Ou utilizando serviços gerenciados como:

- AWS ECS / Fargate
- Azure App Service
- Render / Railway / Fly.io

---

### Escalabilidade

Uma separação futura possível seria dividir a aplicação em:

- API
- Cache distribuído
- Gateway / camada de autenticação
