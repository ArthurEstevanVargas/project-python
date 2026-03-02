# Guia de Contribuição

Obrigado por considerar contribuir para este projeto!

## Como Contribuir

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Padrões de Código

- Use Python 3.10+
- Siga PEP 8 para estilo de código
- Adicione docstrings para funções públicas
- Mantenha funções auxiliares privadas com prefixo `__`

## Estrutura de Commits

Use mensagens de commit claras e descritivas:
- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para mudanças na documentação
- `refactor:` para refatorações de código

## Testando Localmente

```bash
# Instale em modo desenvolvimento
pip install -e .

# Teste o Git Review Agent
git-review

# Teste o CV Extractor
python cv_extractor/extractor.py
```

## Reportando Bugs

Ao reportar bugs, inclua:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Versão do Python e dependências
- Logs de erro, se aplicável
