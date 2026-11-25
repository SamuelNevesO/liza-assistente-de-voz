# Guia de Contribuição — LIZA

## Git Flow do Projeto

1. **`main`**: código estável em produção (e site em `docs/index.html`). Nunca faça commits diretos na `main`.
2. **`develop`**: branch de integração das novas funcionalidades e correções.
3. **Branches de trabalho** (sempre criadas a partir de `develop`):
   - `feature/<nome-da-feature>` para novas funcionalidades
   - `fix/<nome-da-correcao>` para correções de bugs
   - `refactor/<nome>` para melhorias estruturais
   - `docs/<nome>` para documentação

### Passo a passo para contribuir

```powershell
git checkout develop
git pull liza-novo develop
git checkout -b feature/minha-melhoria

# Após implementar e validar:
pytest --cov=src/config --cov=src/core --cov=src/domain --cov=src/services --cov-report=term-missing -v
python -m scripts.self_test

git add -A
git commit -m "feat: descreva sua alteração de forma objetiva"
git push -u liza-novo feature/minha-melhoria
```

Em seguida, abra um **Pull Request** para `develop` usando o template padrão.
