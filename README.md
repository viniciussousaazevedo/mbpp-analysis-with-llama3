# Mbpp Script for LLM analysis

## O que foi feito?
Basicamente, utilizei o dataset do [mbpp](https://huggingface.co/datasets/google-research-datasets/mbpp), que contém descrições de problemas de programação juntamente com solução e testes da solução, para observar como o Llama 3.1 70B cria sua própria suíte de testes por meio de uma integração com RAG simples. O que fiz foi criar uma cópia de cada problema removendo a suíte de testes e solicitando para a LLM criar a sua própria. Uma vez isso feito, comparei o quão bem sucedida a LLM se saiu principalmente em comparação com os testes do próprio dataset que apontam sucesso nos seus códigos de resolução de problemas.

## Como rodar?
Para rodar o script, basta executar esse comando `pip` para instalar as dependências:
```bash
pip install llama-index-core llama-index-llms-ollama llama-index-embeddings-huggingface llama-index-llms-groq llama-index-readers-json
```
Uma vez instalado, basta executar no root do projeto o comando: 
```bash
python ./mbpp_script.py
```
Os resultados estarão presentes nos arquivos locais `error_logs.txt` e `prompt history.txt`

## Interpretações de "erros na geração de teste"
- Em momentos de teste e análise do conteúdo "errado" da LLM, encontrei pérolas como `ERROR IN LLM TEST EXECUTION: assert is_not_prime(1) == True (question id: 3)`🤦‍♂️
- De quem é a culpa? Bem, no fim das contas, devemos analisar tudo como "pode haver problema com":
  - LLM
  - Código da solução
  - Descrições de problemas (potenciais "US's")
  - Prompt Engineer
  - Eu mesmo que posso ter feito o script com algum defeito rs (ninguém é perfeito)
- Gostaria de ter removido todos os outros possíveis causadores de problema da jogada para analisar apenas o desempenho da LLM, mas é um dataset imenso para análise manual...
- Acredito que uma boa prática é analisar sempre os logs e o contexto antes de apontar o dedo para um desses cinco
- O arquivo `error_logs.txt` citado anteriormente guarda todos os erros logados do script

## Melhorias em prompt
- o arquivo `prompt_history.txt`, citado anteriormente, guarda todo o histórico de prompts que utilizei quando o script estava finalizado, juntamente com alguns dados estatísticos referentes a aquela execução em específico. De modo geral, houve uma melhora significativa com adição de elementos de engenharia de prompt, como few-shot prompting, esclarecimento de output e afins. Questões mais complexas foram mais difíceis de fazer a LLM passar, naturalmente.

## Resultados finais
Foram gerados X casos de teste para Y problemas. De modo geral, os resultados obtidos com LLM foram:
- Testes compilados com sucesso: %
- Testes que aprovaram o código gerado: %
- Problemas que passaram em todos os testes: %
> P.S.: Não houveram erros em testes do próprio dataset

## Conclusões: Como isso pode contribuir para nosso projeto?
Brincar com esse dataset me ajudou a ter um pouco mais de noção em uso e consumo de RAG, que muito provavelmente vamos usar no contexto do projeto, vale a pena com certeza dar uma olhada... Além disso, esses resultados me mostraram um pouco mais sobre a importância de prompt engineering e que nem sempre o culpado vai ser a LLM que fez seu trabalho muitas vezes até bem feito!

## Contribuindo com o script...
Minhas maiores indagações em como melhorar esse script consistem em:
- Adaptar o código para utilizar apenas a descrição (acredito ser o mais urgente, por hora)
- Como identificar falsos positivos e falsos negativos no script?
- Como acertar qual é o culpado do teste falho de forma automatizada?