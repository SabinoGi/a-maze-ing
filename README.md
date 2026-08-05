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


# Amazing - Estrutura minima do fluxo

## Objetivo

Gerar um labirinto a partir de um arquivo de configuração, exportá-lo e renderizá-lo.

---

# Fluxo Geral

```text
Config (.txt)
      │
      ▼
 ConfigParser
      │
      ▼
MazeGenerator
      │
      ▼
     Maze
      │
      ▼
MazeRenderer
      │
      ▼
ASCII / MLX
```

---

# Estrutura do Projeto

```text
amazeg/

├── main.py
├── models/
│   ├── cell.py
│   └── maze.py
├── generator/
│   └── maze_generator.py
├── parser/
│   └── config_parser.py
└── renderer/
    └── maze_renderer.py
```

---

# Responsabilidade de Cada Classe

## Cell

Representa uma única célula.

* posição
* paredes (N, E, S, W)
* visitada

---

## Maze

Representa o labirinto.

* largura
* altura
* matriz de Cells
* entrada
* saída

---

## MazeGenerator

Responsável por gerar o labirinto.

Entrada:

* width
* height
* seed
* perfect

Saída:

* Maze

---

## ConfigParser

Responsável por:

* ler o arquivo
* validar dados
* criar a configuração

---

## MazeRenderer

Responsável por:

* desenhar
* exportar
* interação do usuário

---

# Divisão da Dupla

## Pessoa A

* Cell
* Maze
* MazeGenerator
* Algoritmo de geração

## Pessoa B

* ConfigParser
* MazeRenderer
* Exportação
* Interface
* Interações

---

# Ordem de Desenvolvimento

* [ ] Criar Cell
* [ ] Criar Maze
* [ ] Criar MazeGenerator
* [ ] Implementar Backtracking
* [ ] Gerar Perfect Maze
* [ ] Adicionar Loops
* [ ] Parser
* [ ] Renderer
* [ ] Testes

---

# Main

```text
main()

↓

parser.parse()

↓

MazeGenerator(config)

↓

maze.generate()

↓

renderer.export()

↓

renderer.render()

↓

renderer.interaction()
```

---

# Objetivo do Gerador

```text
Criar Maze

↓

Criar Cells

↓

Aplicar algoritmo

↓

Retornar Maze
```

---

# Objetivo Final

```text
Arquivo (.txt)

↓

Config

↓

Maze

↓
Labirinto Renderizado
```
