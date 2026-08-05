# 🌿 Fluxo de Trabalho git/github

## 1. Atualize a `master`

```bash
git switch master
git pull origin master
```

## 2. Atualize sua branch

```bash
git switch <sua_branch>
git merge master
```

## 3. Desenvolva a funcionalidade

Faça as alterações na **sua branch**.

## 4. Salve as alterações

```bash
git add .
git commit -m "Descrição do que foi feito"
git push origin <sua_branch>
```

## 5. Abra um Pull Request

No GitHub, crie um **Pull Request** da sua branch para a `master`.

## 6. Review e Merge

* O outro integrante revisa o código.
* Se necessário, faça novos `commit` + `push`.
* Após a aprovação, realize o **Merge**.

---

## ✅ Boas práticas

Boa prática: sempre que for começar uma nova funcionalidade, primeiro atualize sua master com git pull origin master e depois atualize sua branch com git merge master. Assim você trabalha sempre com a versão mais recente do projeto e reduz a chance de conflitos.
