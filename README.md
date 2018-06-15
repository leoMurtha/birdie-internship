# birdie-internship

## Teste coleta e pré-processamento
  
Usando as técnicas que lhe forem mais familiares e amigáveis (linguagem, frameworks, arquitetura), faça um crawler para capturar os dados das categorias [Geladeira-Refrigeradores](https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/) e [Lavadora-Lava e Seca](https://www.magazineluiza.com.br/lavadora-de-roupas-lava-e-seca/eletrodomesticos/s/ed/ela1/) do site MagazineLuiza .

A partir dos dados capturados, exporte uma lista com todos os produtos vendidos por MagazineLuiza (descarte os produtos vendidos por lojas terceirizadas dentro do site) e destaque os atributos:
 - SKU (código do produto na loja)
 - Titulo
 - Marca
 - Modelo
 - Preço
 - Categoria
   
**Bibliotecas Utilizadas**
- Linguagens
  - [Python](https://www.python.org/)
- Bibliotecas para crawler
  - [Requests](http://docs.python-requests.org/en/master/) + [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
  
  Dados Exportados estão em **magazine_products.csv**
  
## Teste de aprendizado

A partir dos dados coletados, crie um modelo de classificação para predizer a categoria do produto dado seu título. Utilize 70% dos dados para treinar o modelo **(conjunto de treino)** e os 30% restantes para avaliar **(conjunto de teste)**

**Bibliotecas Utilizadas**
- Linguagens
  - [Python](https://www.python.org/)
- Bibliotecas para crawler
  - [TensorFlow](https://www.tensorflow.org/)
  - [NLTK](https://www.nltk.org/)
   
   
   

# Parte Teórica
Pense numa aplicação onde esse script de crawler deve ser executado semanalmente para capturar novos produtos e atualizações nos dados dos produtos já capturados:

### Como você organizaria a arquitetura da aplicação/dados?
   Definiria uma arquitetura em camadas onde teria duas camadas a primeira sendo a camada responsável pela 
   extração dados, a segunda seria responsável pela base de dados sendo suas funções o processamento dos dados, 
   a inserção de novos produtos e atualizações nos produtos existentes a partir dos dados coletados pela primeira camada.
      <img style="width: 50px;" src="https://github.com/leoMurtha/birdie-internship/blob/master/data/arquitetura.png ">
   
### O que deixaria automatizado/agendado?
   O crawler teria um processo rodando contando e monitorando se páginas ou produtos foram adicionados e por exemplo todo
   domingo às 00h ele rodaria a aplicação novamente.
  
### O que monitorar para acompanhar a saúde/qualidade da aplicação?
   Se os dados estão consistentes e não redundantes assim como também se o crawler está conseguindo acessar corretamente os
   links.
  
### Na sua opinião, quais são os principais riscos que podem causar erros na execução desse script?
   Como se trata de um crawler o risco mais preocupante é se o site da onde se está extraindo informações tomar um update que
   mude seu layout e seus HTML comprometendo o parsing e o regex feitos pelo crawler para extrair somente as informações
   requisitadas.
