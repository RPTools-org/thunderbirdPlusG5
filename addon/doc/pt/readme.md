# Thunderbird+G5 para Thunderbird >= 115

* Autores: Pierre-Louis Renaud (Do Thunderbird 78 ao 115) & Cyrille Bougot (TB 102), Daniel Poiraud (Do TB 78 ao 91), Yannick (TB 45 ao 60);
* URL: [página inicial dos extras do Thunderbird+ G5 e G4][4] ;
  [Histórico de alterações em RPTools.org][5] ;
  [Contato em francês ou inglês][6] ;
* Baixe [versão estável] [1]
* Baixe [versão mais recente em RPTools.org][3];
* Compatibilidade com NVDA: 2021.1 e posterior;
* [Código fonte no gitHub][2]

## Introdução
O Thunderbird+G5 é um extra para o NVDA que aumenta significativamente a eficiência e o conforto de uso do cliente de e-mail Thunderbird 115.

Melhora a sua produtividade fornecendo comandos que não existem, nativamente, no Thunderbird:

* atalhos de teclado para acesso direto à árvore de pastas, lista de mensagens e painel de visualização.
* Navegação perfeita entre os painéis da janela principal usando as teclas Tab e Escape.
* Atalhos para ver e copiar campos da lista de mensagens e cabeçalhos de mensagens sem alterar o foco.
* Acesso direto aos anexos.
* Atalhos para consulta e acesso direto aos campos de endereçamento da janela Escrever.
* Melhora significativamente o uso da caixa de diálogo de verificação ortográfica.
* Gestão mais fácil de livros de endereços e listas de discussão (v.2402.14.00).
* Menu de atualização de extras (v.2402.14.00)
* E muitos mais...

Esta página documenta os atalhos de teclado oferecidos pelo Thunderbird+G5.

A maioria desses atalhos de teclado são configuráveis através da categoria Menu NVDA / Preferências / definir comandos / Thunderbird+G5 (TB >= 115).

## Navegação na janela principal

Nota: A tecla nomeada como (tecla acima de Tab) no restante desta página designa a tecla localizada abaixo de Escape, acima de Tab e à esquerda do número 1. O seu nome varia dependendo do idioma do teclado.

### Atalhos gerais
*/*
* (tecla acima de Tab): mostra o menu de vários comandos do extra, incluindo atualização do extra.
* Shift+(tecla acima de Tab): mostra o menu de opções do extra.
* Control+F1: mostra a página atual. Para alguns esclarecimentos, pode [visitar a documentação da versão 4][7]
* F8 para mostrar ou ocultar o painel de visualização: este comando é duplicado pelo extra.

### Navegar entre os painéis da janela principal
Estes atalhos aplicam-se na árvore de pastas, lista de mensagens e painel de visualização de mensagens.

* control+(tecla acima de Tab): Um pressionamento coloca o foco na lista de mensagens, dois pressionamentos colocam o foco na lista de mensagens e selecionam a última mensagem.
* Alt+c: mostra o menu de contas e depois o menu de pastas da conta escolhida. Desde a versão 2312.14, suporta o modo "pastas unificadas" da árvore de pastas.
* Control+Alt+c: mostra o menu de contas e depois o menu de pastas não lidas da conta escolhida. (2023.11.15)<br>
Nota: estes dois últimos atalhos podem ser modificados através da caixa de diálogo Definir comandos.
* alt+Home: um pressionamento seleciona a pasta atual na árvore de pastas, dois pressionamentos mostram um menu que permite escolher a conta de e-mail a ser acedida na árvore.
* Control+Alt+Home: O mesmo, mas para pastas com mensagens não lidas. (2023.10.31)
* Tab: vai imediatamente para o próximo painel.
* Escape: retorna ao painel anterior, sem desvio.
Escape também permite alternar entre a árvore de pastas e a lista de mensagens.
* Shift+Tab: O seu comportamento nativo foi preservado nesta versão.

### Navegar pelos separadores da janela principal

* Control+Tab com ou sem a tecla shift e control+1 a 9: O extra intercepta as mudanças de separadores para anunciar o número do pedido e o número total de separadores.<br>
Além disso, o extra dá foco ao conteúdo do separador quando é ativado pela primeira vez. Para o primeiro separador, o foco pode ser colocado na última mensagem da lista de mensagens ou na primeira mensagem não lida. Através do menu de opções / Opções da janela principal, pode marcar a opção intitulada: Aceda à primeira mensagem não lida quando o primeiro separador for ativado pela primeira vez, caso contrário, a última mensagem (v.2402.14.00));
* Control+a primeira tecla localizada à esquerda do retrocesso: mostra um menu com a lista de separadores existentes. Pressione Enter num item de menu para ativar o separador correspondente.
* Alt+a primeira tecla à esquerda do retrocesso: mostra o menu de contexto do separador. Este menu é nativo do Thunderbird.

Nota: A etiqueta da primeira tecla à esquerda do retrocesso varia dependendo do idioma do teclado.

## Lista de mensagens

<!-- início 2023.11.10 -->

### Vocalização personalizada de linhas (2023.11.10)

Este modo personalizado, desabilitado por padrão, permite ouvir com mais conforto as linhas da lista de mensagens.

No entanto, tem algumas desvantagens:

* Não é compatível com a visualização do cartão da lista de mensagens. Para retornar à visualização de tabela, vá até a lista de mensagens, pressione Shift+Tab até o botão "Opções da lista de mensagens", pressione Enter e no menu de contexto marque "Visualização de tabela".
* Em PCs mais lentos, pode causar uma lentidão perceptível na navegação com as setas na lista de mensagens.
* Se pressionar a seta para baixo, na última linha, não será anunciado.

Pode ativar este modo pressionando a tecla shift+ acima de Tab e selecionando o item "Opções da janela principal" no menu e marcando a opção "Lista de mensagens: vocalização personalizada de linhas".

Este submenu também contém outras opções de personalização que só funcionam se a vocalização personalizada estiver habilitada.
<br>
Observação:

Alguns utyilizadores estão a enfrentar problemas com linhas em branco no modo normal. Se estiver neste caso, ative a opção “Lista de mensagens: forçar preenchimento de linhas se sempre em branco”.

Mas o ideal é que esse problema seja resolvido com a criação de um novo perfil de utilizador no Thunderbird, o que envolve a reconfiguração de contas de e-mail.

#### Dica para vocalização personalizada de linhas

Pode usar as duas colunas "Status de leitura" e "Status" juntas para combinar as suas respectivas vantagens:

* A coluna "Status de leitura" anuncia "não lido" quando pressiona a letra m para reverter o status de leitura.
* A coluna “Status” anuncia os status “Novo”, “Respondido” e “Transferido”.
* O extra garantirá que “Não lido” seja anunciado apenas uma vez e que “Lido” nunca seja anunciado.

<br>
leia também a seção [Escolha e ordem das colunas](#cols)

### Atalhos da lista de mensagens

<!-- final 2023.10.31 -->

* Escape na lista de mensagens: se um filtro estiver ativo, ele é desativado e a lista de mensagens permanece selecionada. Caso contrário, este atalho dá foco à árvore de pastas.
* NVDA+seta para cima ou NVDA+l (laptop) na lista de mensagens:<br>
Um pressionamento: anuncia a linha atual da lista de mensagens. O atalho NVDA+Tab produz o mesmo resultado, mas sem usar este extra.<br>
Dois pressionamentos: mostra os detalhes da linha numa janela de texto que permite a análise da linha através do teclado.
* Control+seta para direita em mensagens agrupadas por conversa: seleciona a última mensagem da conversa. Este é primeiro expandido se estiver recolhido. (2312.14.00)
* Control+seta para esquerda em mensagens agrupadas por conversas: seleciona a primeira mensagem da conversa. Ele será expandido primeiro se estiver recolhido.<br>Esses dois últimos atalhos precisam da coluna "Total" para funcionar.
* Barra de espaço, F4 ou Alt+seta para baixo: lê uma versão limpa ou traduzida da mensagem no painel de visualização, sem sair da lista de mensagens.<br>
Nota: Se uma mensagem contiver mais de 75 elementos HTML, um bipe será emitido para cada elemento de texto recuperado. Com um pressionamento rápido na tecla Control, pode começar imediatamente a ler a mensagem incompleta. (2401.09.0)
* Bloqueio de rolagem. : ativa ou desativa o modo de tradução de mensagens para leitura de mensagens com Espaço, F4 ou Alt+seta para baixo. Observe que o extra Instant Translate deve estar instalado e ativado. (2401.02.0)
* Shift + Scroll Lock: ativa ou desativa a visualização da tradução numa janela de texto navegável. Este modo permite que toda a mensagem seja lida em Braille. (2401.02.0) <br>
Nota: A tradução de mensagens também está disponível em janelas e separadores que mostram uma mensagem.
* Alt+seta para cima: coloca a mensagem no navegador virtual de citações/citações;
* Windows+setas para baixo ou para cima: lê a citação seguinte ou anterior. Se o modo Tradução estiver ativo, a cotação será traduzida (2401.02.0.

Nota: Este navegador de citações/citações pode ser usado na lista de mensagens, na mensagem da janela de leitura separada, na janela de composição e na caixa de diálogo de verificação ortográfica.

### Anunciar, soletrar e copiar campos da lista de mensagens

Cada linha da lista é dividida em vários campos correspondentes às colunas. Pode comparar um campo a uma célula numa folha do Excel.

Os atalhos abaixo podem ser executados sem alterar o foco:

* número 1 a 9 da linha acima das letras: com o número correspondente à linha da coluna da lista de mensagens, estão disponíveis as seguintes ações:<br>
Um pressionamento: anuncia o valor do campo. Por exemplo, dependendo da ordem das suas colunas, 1 anuncia o remetente e 2 anuncia o assunto.<br>
Dois pressionamentos: soletra o valor do campo.<br>
Três pressionamentos: copia o valor do campo para a área de transferência.

Dica: Se usar várias pastas, aplique a mesma ordem de colunas a todas elas, para que um número sempre corresponda à mesma coluna.

### Anunciar e copiar cabeçalhos do painel de visualização ou janela de leitura separada

* Alt+1 a Alt+6 da lista e da janela de leitura separada:<br>
Um pressionamento: anuncia o valor do cabeçalho,<br>
Dois pressionamentos: abre uma caixa de edição contendo o valor do cabeçalho. Ao fechar esta caixa de diálogo com Enter, este valor é copiado para a área de transferência, o que é muito prático para recuperar o endereço de e-mail de um correspondente. <br>
Três pressionamentos: abre o menu de contexto do cabeçalho relevante. Este é um menu nativo do Thunderbird.

### Painel de anexos na janela principal e janela de leitura separada
Os atalhos a seguir permitem anunciar anexos ou selecionar um na lista.

* Alt+9 ou Alt+Page Down:<br>
Um pressionamento: anuncia o número de anexos e os nomes de todos os anexos.<br>Se o Thunderbird não mostrar automaticamente o painel de anexos, o extra fazê-lo-á e o Thunderbird selecionará o primeiro anexo.<br>
Dois pressionamentos:<br>
Se houver apenas um anexo, move o foco para ele e mostra o seu menu de contexto. (2312.18.00)<br>
Se houver vários anexos, seleciona o primeiro anexo da lista. (2312.18.00)

### Gestão de etiquetas da lista de mensagens
Os atalhos abaixo permitem a gestão vocal de etiquetas sem a necessidade de navegar pelo menu de contexto do Thunderbird.

* Shift+1 a Shift+9: Adiciona ou remove uma etiqueta, com vocalização.
* Shift+0: Remove todas as etiquetas da mensagem selecionada.
* alt+0: Anuncia todas as etiquetas da mensagem.

### Vocalização dos atalhos a, c, j e m da lista de mensagens
A partir da versão 2023.11.10, estes atalhos de marcação não são mais vocalizados pelo extra. O NVDA anuncia imediatamente a mudança no conteúdo da linha em questão.

### Filtragem rápida de mensagens (2023.11.10)

letra f: alternativa ergonômica ao Control+Shift+k para mostrar ou aceder à barra de filtro rápido. Este atalho é configurável na caixa de diálogo definir comandos.
<br>Nota: O foco deve estar numa lista de mensagens não vazia. Pressione Escape para desativar o filtro ativo.

Para aceder diretamente aos resultados da filtragem no campo de entrada de palavras-chave, pressione a seta para baixo.

Quando um filtro está ativo, um som semelhante a um assobio é reproduzido sempre que a lista de mensagens ganha foco. Isto é especialmente útil quando alterna janelas ou guias e retorna à lista de mensagens posteriormente.

Se esse som o incomoda, tem duas opções:

1. Abra o menu Shift+(tecla acima de Tab) e no submenu Desativações marque a opção:<br>
Lista de Mensagens: não reproduz nenhum som quando a lista é filtrada e ganha foco.
2. Abra o menu Shift+ (tecla acima de Tab) e pressione Enter no item: Abrir pasta de sons.
<br>Esta pasta será aberta no Explorador de ficheiros,
<br>Lá, encontrará o ficheiro filter.wav.
<br> Pode substituir este ficheiro por outro desde que o seu ficheiro tenha o mesmo nome: filter.wav.
<br>Quando terminar, reinicie o NVDA.
<!-- final 2023.10.31 -->

### Anúncio da barra de status e informações de filtro rápido

* Alt+end ou Alt+(segunda tecla do retrocesso esquerdo):
Da lista de mensagens ou barra de filtro rápido: anuncia o número total ou filtrado de mensagens, o número de mensagens selecionadas se houver mais de uma e a expressão do filtro se um filtro tiver sido definido. Essas informações vêm da barra de filtro rápido e não mais da barra de status.<br>
De outro separador ou janela: anuncia a barra de status.
* Quando a lista de mensagens recebe o foco, um som sibilante é ouvido quando a filtragem rápida está ativa.

### Resposta inteligente: responda a listas de discussão com control+R
Para responder a determinadas listas de discussão, é necessário pressionar Control+Shift+L. Para evitar responder ao destinatário errado, pressione Control+R para responder à lista e Control+r duas vezes para responder em particular ao remetente da mensagem.

Nota: groups.io não é afetado por este recurso.

<!-- Não remova nem traduza a seguinte tag --><a name="cols">

<!-- início 31/10/2023 -->

### Escolha e ordem das colunas (31.10.2023)

Este procedimento é nativo do Thunderbird 115, mas é explicado aqui porque está mal documentado.

* Pressione Shift+tab na lista de mensagens para ir para a lista de cabeçalhos de coluna.
* Use as setas esquerda e direita para selecionar uma coluna.
* Quando chegar à coluna especial "Escolher colunas para mostrar", pressione Enter nela.
* No menu, marque ou desmarque as colunas e pressione Escape para fechar este menu. Como lembrete, é recomendável desmarcar a coluna “Status de leitura” e marcar a coluna “Status”.
* De volta à lista de cabeçalhos de coluna, pressione a seta para a esquerda para mover uma coluna.
* Em seguida, pressione Alt+seta para esquerda ou direita para colocá-la no local desejado. Isso será vocalizado corretamente.
* Repita estas operações para mover outras colunas.
* Quando a organização das colunas estiver concluída, pressione Tab para retornar à lista de mensagens.

<!-- início 31/10/2023 -->

## árvore de pastas: navegação rápida (2023.10.31)

Alguns comandos mostram um menu contendo pastas na estrutura em árvore para permitir a navegação pelas letras iniciais. Por motivos de desempenho, o script não mostra subpastas de ramificações recolhidas.

Além disso, se o nome de uma conta ou pasta terminar com um hífen, não será incluído no menu de pastas não lidas.

Portanto, é aconselhável excluir contas e pastas fechando contas pouco utilizadas ou renomeando contas para não adicionar um hífen no final do nome.

<br>
Desde a versão 2312.14.00, o modo "Pastas Unificadas" é suportado. Neste modo, todos os nomes de contas devem conter o caractere @. Para renomear uma conta, selecione-a na árvore, pressione a tecla Aplicativos e pressione Configurações no menu de contexto. Em seguida, vá para o campo "Nome da conta".

### Atalhos da árvore de pastas

* NVDA+seta para cima ou NVDA+l (laptop): anuncia o nome da pasta selecionada. O NVDA não faz mais isto sozinho.
* Espaço na pasta não lida: define o foco para a  primeira mensagem não lida na lista de mensagens.
* Enter ou Alt+seta para cima: mostra um menu de todas as pastas da conta à qual a pasta selecionada pertence.
* Control+Enter ou Alt+seta para baixo: mostra um menu de pastas não lidas para a conta à qual a pasta selecionada pertence.
<br>Em ambos os casos, o último item do menu mostra o menu de contas. Pode pressionar a barra de espaço para escolher uma conta.
* Shift+Enter: mostra um menu contendo todas as contas e pastas da árvore.
* Shift+Control+Enter: mostra um menu contendo todas as contas e pastas não lidas na árvore.

Observações:

Para estes dois últimos comandos, levará algum tempo até que o menu seja mostrado, pois o script deve percorrer toda a árvore para construir o menu.

Em vez disso, use uma destas duas pequenas dicas:

1. Pressione Alt+Home duas vezes rapidamente para mostrar o menu de contas,
<br>Escolha uma conta e pressione Enter.<br>Um novo menu contendo as pastas desta conta será aberto e poderá usar uma letra para ativar uma.
2. Pressione Control+Alt+Home duas vezes rapidamente para mostrar o menu de contas com pastas não lidas,
<br>Escolha uma conta e pressione Enter.
<br>Um novo menu contendo as pastas não lidas desta conta será aberto e poderá usar uma letra para ativar uma.

<!-- final 2023.10.31 -->

## Fechar janelas e separadores

* A tecla Escape fecha a janela separada de leitura de mensagens e a janela de composição. Veja as opções relevantes.
* Control+retrocesso: também usado para fechar separadores e janelas. Ao editar texto, este atalho exclui a palavra anterior.

## Janela de composição
Os atalhos nesta janela dizem respeito aos campos de endereçamento e ao painel de anexos.

* Alt+1 a Alt+8:<br>
Um pressionamento: anuncia o valor do campo de endereçamento ou do painel de anexos,<br>
Dois pressionamentos: coloca o foco no campo de endereçamento ou no painel de anexos.
* Alt+pageDown: O mesmo que Alt+3 para o painel de anexos.
* Notas:<br>
o anúncio do painel de anexos com Alt+3 da uma lista numerada de nomes de ficheiros e seu tamanho total,<br>
Quando o foco está na lista de anexos, a tecla de escape retorna ao corpo da mensagem.
* Alt+seta para cima: coloca a mensagem que está sendo escrita no navegador virtual de citações/citações;
* Windows+setas verticais: anuncia a linha seguinte ou anterior no navegador de citações; Isto permite que ouça a mensagem que está respondendo sem alterar as janelas.
* Windows+seta horizontal: vai para a citação seguinte ou anterior sem alterar as janelas.<br>

## Caixa de diálogo de verificação ortográfica
Na abertura deste diálogo, o extra anuncia automaticamente as palavras e sua ortografia. Isso pode ser desativado nas opções da janela de composição.

Os seguintes atalhos estão disponíveis na área de edição de palavras de substituição:

* Alt+seta para cima: soletra a palavra com erro ortográfico e a sugestão de substituição.
* Alt+seta para cima quando pressionado duas vezes: anuncia a frase em que se encontra a palavra com erro ortográfico, graças ao navegador virtual de citações que inicializa automaticamente neste contexto.
*Enter: pressiona o botão “Substituir”, sem sair da área de edição.
* Shift+enter: pressiona o botão "Substituir tudo".
* Control+Enter: Pressiona o botão "Ignorar".
* Shift+control+Enter: pressiona o botão "Ignorar tudo".
* Alt+Enter: adiciona a palavra declarada como incorreta ao dicionário.

## livro de endereços, gestão mais fácil (v.2024.02.07)
O extra melhora os anúncios do livro de endereços e fornece comandos de teclado que permitem organizar livros de endereços e listas de e-mail por meio de arrastar e soltar virtual.

### Anúncios aprimorados

* Árvore de livros de endereços e listas de discussão: o extra também anuncia o tipo de um elemento: livro de endereços ou lista do livro de endereços pai,
* lista de contatos: o add-on também anuncia o endereço de e-mail do contato selecionado.

### Resumo do comando

* Tecla Tab do campo de pesquisa: vai diretamente para a tabela de contatos ignorando o botão "Listar opções de visualização". Este botão permanece acessível com shift+Tab na tabela de contatos;.
* tecla de escape:

* Na árvore do livro de endereços, traz o foco para o campo de pesquisa;
* No campo de pesquisa, traz o foco para a árvore do livro de endereços;
* Na tabela de contatos, traz o foco para o campo de pesquisa;

* Control + tecla de Aplicações ou tecla acima de tab: abre um menu de contexto que inclui: Ir para a árvore de livros de endereços e listas de e-mail, Acessar a tabela de contatos, Novo livro de endereços, Novo contato, Nova lista, Importar. Além dos dois primeiros, esses itens vêm da barra de ferramentas do livro de endereços.
* letra "a" da tabela de contatos: arrasta e solta os contatos selecionados na lista de discussão ou no livro de endereços definido como destino. Na primeira vez que pressiona esta tecla, o destino é solicitado através de um menu. Então, o destino não será solicitado novamente até que altere a lista de fontes ou o livro de endereços.
* letra “d” da tabela de contatos: mostra o menu de listas e destinos dos livros de endereços.

### Exemplo 1: Criando uma lista de e-mails no livro de Endereços Pessoal
* Vá para a árvore do livro de endereços e selecione "Endereços pessoais". Uma nova lista é criada apenas no livro de endereços selecionado, não é possível em "Todos os livros de endereços";
* Pressione Control+tecla de Aplicações ou a tecla acima de Tab e no menu pressione Enter em: Nova lista;
* Na caixa de diálogo que se abre, digite o nome da lista, por exemplo: Minha família,<br> pode adicionar contatos através desta caixa de diálogo, mas por exemplo, feche esta caixa de diálogo através do botão OK;
* De volta aos livros de endereços e à árvore de listas, percebe um novo elemento chamado: Minha família, lista de endereços pessoais,<br>
Selecione “Endereços pessoais”;
* Pressione Tab para inserir uma palavra-chave de pesquisa ou Tab na tabela de Contatos ou use o menu Control+te de Aplicações ou a tecla acima de Tab;
* Na tabela de contatos, selecione um ou mais contatos através do método padrão Control+barra de espaço, Control+seta para baixo, Control+barra de espaço, etc;
* Pressione a letra a para arrastá-los e soltá-los na lista de discussão. Na primeira vez, será mostrado o menu de destinos possíveis. Selecione o item "Novo nome da lista" e pressione Enter. Na próxima vez que pressionar a letra a, o mesmo destino será usado sem mostrar este menu.
* No final da operação de arrastar e soltar, um bipe será emitido e o foco será colocado na caixa de pesquisa.
* Digite uma nova palavra, pressione Tab, selecione os contatos e pressione a letra a novamente para adicioná-los à lista "Novo nome da lista";

### Mover contatos de endereços coletados para livros de endereços diferentes

1. Vá até a árvore do livro de endereços e selecione “Endereços coletados”;
2. Aceda à tabela de contatos;
3. Selecione um ou mais contatos;
4. Opcionalmente pressione a letra “d” para pré-selecionar um novo destino;
5. De volta à tabela de contatos, pressione a letra “a” para arrastar e soltar os contatos selecionados no livro de endereços de destino;
6. Feito isto, o foco é colocado no campo de busca. Opcionalmente, insira um nome e repita as operações 2 a 5.

## Menu de atualização de extras (v.2402.14.00)

Para aceder a este menu, pode pressionar AltGr+Shift+tecla acima da tecla Tab ou fazer o seguinte:

* Vá para a janela principal do Thunderbird,
* Pressione a tecla acima da tecla Tab,
* No menu de contexto, pressione a seta para cima para selecionar o item Atualizar e pressione Enter,
* Um novo menu de contexto oferece a escolha entre: Verificar atualizações, ativar ou desativar atualizações automáticas e Instalar versão AAAMM.DD, onde AAAMM.DD é a versão disponível para download. Este último pode ser mais recente que o disponível na atualização automática.

## extras externos

### extra Iniciar com caixa de entrada para Thunderbird 115 (2023.10.31)1

Quando o Thunderbird é iniciado, este extra seleciona automaticamente:

* a pasta “Caixa de entrada” da conta de sua escolha na árvore de pastas.
* A última mensagem na pasta de entrada de mensagens da conta escolhida.
* A primeira mensagem não lida na pasta de entrada de mensagens da conta escolhida.

Instalação:

* no Thunderbird, abra o menu “Ferramentas” e valide em: extras e temas;
* Na página gestor de Módulos, coloque-se na caixa de pesquisa. No modo de navegação, pode pressionar a letra "e" para acessá-lo rapidamente;
* escreva: comece com Caixa de entrada e pressione Enter;
* selecione manualmente o separador "Iniciar com caixa de entrada:: Pesquisar:: Módulos para Thunderbird", por exemplo. em seguida, pressione a tecla 3 ou aspas até chegar ao título do nível 3 intitulado pelo nome do módulo que você buscou;
* Com a seta para baixo, role para baixo até o link "Adicionar ao Thunderbird" e pressione Enter nele;
* Siga o procedimento e reinicie o Thunderbird;
* Se tudo correr bem, o Thunderbird abrirá no separador principal e colocará o foco na lista de mensagens;


Definir as opções de Iniciar com Caixa de entrada:

* Retorne ao separador "gestor de extras";
* Se necessário, saia do campo de pesquisa para se colocar no modo de navegação;
* Pressione a tecla 3 quantas vezes forem necessárias para atingir o cabeçalho do nível 3 intitulado “Iniciar com caixa de entrada na lista de módulos instalados;
* Em seguida valide no botão: Opções do módulo. Isto abre um novo separador intitulada: Comece com Caixa de entrada, Configurações;
* Defina as opções e reinicie o Thunderbird.


[1]: https://github.com/RPTools-org/thunderbirdPlusG5/releases/download/v2403.27.00/thunderbirdPlusG5-2403.27.00.nvda-addon

[2]: https://github.com/RPTools-org/thunderbirdPlusG5/

[3]: https://www.rptools.org/?p=9514

[4]: https://www.rptools.org/NVDA-Thunderbird/index.html

[5]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=changes&v=G5&lang=en

[6]: https://www.rptools.org/NVDA-Thunderbird/toContact.html

[7]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=manual&lang=en