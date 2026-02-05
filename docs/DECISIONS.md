> Documentação escrita em português para manter consistência com o briefing do case.

# Decisões técnicas

## Escolha do framework
Utilizei Flask por ser um framework simples e suficiente para o escopo do case. A ideia foi manter o foco na solução e não na complexidade do framework.

## Camada de serviço
As regras de filtro, ordenação e paginação foram isoladas em um módulo de serviço para manter o endpoint mais simples e facilitar a escrita de testes unitários sem dependência do Flask ou da API externa.

## Estratégia de cache
A SWAPI é uma dependência externa e pode apresentar lentidão ou indisponibilidade. Por isso, implementei um cache simples em memória com TTL, reduzindo chamadas repetidas e facilitando a observação do comportamento via header `X-Cache`.

## Limitações da solução
- Quando utilizado o parâmetro `search`, a SWAPI já retorna os dados paginados. As regras adicionais de filtro e ordenação são aplicadas apenas sobre essa página retornada.
- Os filtros são aplicados apenas em campos escalares. Não foi feita resolução de URLs relacionadas (como filmes ou planetas) para evitar múltiplas chamadas externas.

