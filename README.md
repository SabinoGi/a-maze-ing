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

* Nunca trabalhe diretamente na `master`.
* Sempre atualize a `master` antes de iniciar uma nova tarefa.
* Faça commits pequenos e descritivos.
* Sempre utilize **Pull Request** antes do **Merge**.

