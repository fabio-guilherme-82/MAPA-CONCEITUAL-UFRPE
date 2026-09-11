# Mapa Conceitual UFRPE

Mapa conceitual sobre **software livre**, **software proprietario** e **tipos de licenca**, desenvolvido para a UFRPE.

## Conteudo

O mapa apresenta:

- definicoes de software livre e proprietario;
- caracteristicas, vantagens e riscos de cada modelo;
- exemplos de softwares;
- licencas GPL, MIT/BSD e EULA.

## Requisitos

- Python 3.10 ou superior;
- pacote `pyvis`.

## Como executar

1. Instale a dependencia:

   ```bash
   pip install pyvis
   ```

2. Gere o mapa conceitual:

   ```bash
   python mapa01.py
   ```

   O arquivo `mapa_conceitual_software.html` sera criado ou atualizado na raiz do projeto.

3. Abra o arquivo HTML no navegador.

   Para executar um servidor local, use:

   ```bash
   python -m http.server 8765
   ```

   Depois acesse <http://127.0.0.1:8765/mapa_conceitual_software.html>.

## Estrutura

```text
.
├── mapa01.py
├── mapa_conceitual_software.html
└── lib/
    ├── bindings/
    ├── tom-select/
    └── vis-9.1.2/
```

## Tecnologias

- Python;
- PyVis;
- vis-network;
- HTML, CSS e JavaScript.

## Licenca

Projeto academico desenvolvido para fins educacionais.
