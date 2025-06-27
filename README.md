# 📚 Biblioteca Virtual IFPB - Campus Campina Grande

Sistema web para disponibilização de listas de exercícios, livros e outros materiais didáticos voltados aos alunos do ensino médio técnico do IFPB - Campus Campina Grande.

---

## 🎯 Objetivo

O projeto visa centralizar e organizar conteúdos pedagógicos de forma acessível e permanente, promovendo o apoio ao estudo autônomo dos estudantes dos cursos técnicos integrados.

---

## 🧩 Funcionalidades

- ✅ Navegação por curso, série e disciplina
- ✅ Separação entre núcleo comum e técnico
- ✅ Listas, livros e materiais extras
- ✅ Upload de arquivos por administradores
- ✅ Estrutura de busca por palavra-chave (em desenvolvimento)
- ✅ Acesso livre aos materiais (sem login)

---

## 🏫 Cursos Atendidos

- Informática  
- Química  
- Petróleo e Gás  
- Mineração  

---

## 🗂 Estrutura do Conteúdo

```text
Home
 └── Cursos
      └── [Curso]
           └── [Série]
                ├── Núcleo Comum
                │     └── [Disciplina]
                │           ├── Listas
                │           └── Livros
                └── Núcleo Técnico
                      └── [Disciplina Técnica]
                            ├── Listas
                            └── Livros
                            └── ...
