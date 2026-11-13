# Banner animado — d-ribeiro

## 1. Sobre o projeto

Criei um banner animado personalizado para representar minha identidade no GitHub, reunindo tecnologia, criatividade, inteligência artificial e programação.

O desenvolvimento aconteceu em duas etapas principais:

1. Criação da animação original com auxílio do Manus, seguindo um prompt elaborado por mim.
2. Personalização da animação utilizando Python, para substituir os textos e adaptar o GIF à identidade visual desejada.

O resultado é um banner personalizado, desenvolvido a partir da combinação de criação com IA e processamento de imagens por código.

## 2. Criação da animação com inteligência artificial

Utilizei o **Manus** para criar o GIF original a partir de um prompt que elaborei.

Nesse processo, defini a proposta visual e as características que desejava para o banner.

A ferramenta gerou a animação que serviu como ponto de partida para a etapa seguinte.

O arquivo original foi preservado sem alterações, permitindo manter uma cópia da criação inicial e utilizá-la novamente, caso necessário.

## 3. Personalização com Python

Depois de receber o GIF original, iniciei a etapa de personalização.

Utilizei Python 3 e bibliotecas de processamento de imagens para substituir os textos presentes na animação.

O objetivo era preservar os movimentos e a aparência original, sem colocar uma caixa sobre a imagem ou comprometer sua composição.

O script `editar_banner.py` automatiza esse processo, trabalhando quadro a quadro.

### Bibliotecas utilizadas

- **Pillow:** abertura, manipulação, desenho dos textos e gravação do GIF.
- **OpenCV:** identificação e remoção dos textos antigos por processamento de imagem.
- **NumPy:** manipulação das matrizes de pixels utilizadas pelo OpenCV.

### Identidade visual aplicada

Foram adicionados três textos:

- Em constante compilação.
- Estudos, desafios e aprendizados em programação, IA e automações.
- Aberto a pequenos projetos.

A tipografia utiliza uma fonte serifada, cor marfim e sombra discreta.

Também foi incluída a assinatura `d-ribeiro` no canto inferior direito.

A fonte preferencial configurada no script é Noto Serif Display, com alternativas previstas.

## 4. Arquivos do projeto

| Arquivo | Finalidade |
|---|---|
| `banner_github_animated.gif` | Animação original criada com auxílio do Manus |
| `editar_banner.py` | Script Python que realiza a personalização |
| `banner-d-ribeiro.gif` | GIF personalizado, resultado final |

### Características do GIF final

- Resolução: 1000 × 429 pixels.
- Quantidade: 41 quadros.
- Duração aproximada: 5,13 segundos.
- Reprodução em loop contínuo.

## 5. Como reproduzir a personalização

### Requisitos

- Python 3 instalado.
- GIF original `banner_github_animated.gif`.
- Script `editar_banner.py`.

O GIF original e o script precisam estar na mesma pasta.

### Instalação das bibliotecas

No terminal, execute:

```bash
python -m pip install Pillow numpy opencv-python-headless
```

### Executar o script

```bash
python editar_banner.py
```

Se tudo funcionar corretamente, será criado o arquivo `banner-d-ribeiro.gif` na mesma pasta.

O GIF original não deve ser alterado pelo processo.

## 6. Possíveis problemas e soluções

**Python não encontrado**

Verifique a instalação:

```bash
python --version
```

Se necessário, tente:

```bash
py --version
```

**Biblioteca não encontrada**

Instale novamente as dependências:

```bash
python -m pip install Pillow numpy opencv-python-headless
```

**GIF original não encontrado**

Confira se o arquivo `banner_github_animated.gif` está na mesma pasta do script e se o nome está correto.

**Fonte diferente da esperada**

Confira a instalação da Noto Serif Display e os caminhos definidos em `CAMINHOS_FONTE`.

**GIF final não foi criado**

Leia a mensagem de erro apresentada no terminal e confira se o script está completo, se as dependências estão instaladas e se a pasta permite gravação de arquivos.

## 7. Publicação no GitHub

Depois de gerar e conferir o GIF personalizado, enviei o arquivo `banner-d-ribeiro.gif` para o repositório do meu perfil.

Para exibi-lo no `README.md`, utilizei o caminho correspondente à localização do arquivo.

Se estiver na raiz:

```markdown
![Banner animado d-ribeiro](./banner-d-ribeiro.gif)
```

Se estiver dentro de `assets/`:

```markdown
![Banner animado d-ribeiro](./assets/banner-d-ribeiro.gif)
```

Após atualizar o README, salvei e publiquei as alterações com Git.

## 8. Ferramentas utilizadas

- Manus — criação da animação original a partir de um prompt.
- Python 3 — automação da personalização.
- Pillow — processamento e gravação de imagens.
- OpenCV — processamento dos quadros.
- NumPy — manipulação de pixels.
- Terminal — execução dos comandos.
- Git e GitHub — versionamento e publicação.

Não utilizei Canva nem Photoshop.

## 9. O que aprendi com este projeto

Neste projeto, explorei uma maneira de combinar inteligência artificial e programação para criar algo personalizado.

Aprendi sobre processamento de imagens, manipulação de quadros de GIF, utilização de bibliotecas Python e automação de tarefas visuais.

Também percebi como uma ideia pode passar por diferentes ferramentas até chegar ao resultado desejado.

Mais do que criar um banner, registrei um processo que posso consultar, reproduzir e aprimorar em projetos futuros.