O projeto da disciplina consiste na implementação de uma rede distribuída, onde os elementos comunicam-se entre si utilizando uma topologia em anel. A comunicação direta entre os nós é restrita aos seus pares adjacentes, enquanto todos os nós podem trocar mensagens diretamente com a Autoridade Certificadora.

O projeto é dividido em quatro etapas principais:

Topologia e Comunicação entre Elementos:

Os nós da rede são representados como processos em máquinas locais, utilizando sockets distintos na abordagem convencional. Com Docker, cada nó é representado por um contêiner independente. A comunicação entre os nós é restrita aos vizinhos, e todos os nós podem se comunicar diretamente com a Autoridade Certificadora.

Autoridade Certificadora:

Cada nó, ao ser instanciado, deve se registrar na Autoridade Certificadora, que gera um par de chaves assimétricas (pública e privada). A chave privada é enviada para o nó, enquanto a chave pública é armazenada na Autoridade Certificadora. As sinalizações de solicitação e troca de chaves devem ser seguras, e a criptografia simétrica é obrigatória para garantir a confidencialidade na transmissão de informações.

Aplicação:

A aplicação final é desenvolvida utilizando o protocolo UDP e consiste em um chat seguro. Todos os nós devem conversar entre si trocando mensagens simultâneas, seguidas por uma mensagem de broadcast. As mensagens devem ser protegidas por criptografia e/ou assinatura digital para garantir a segurança da informação.

Roteamento:

É necessário implementar um mecanismo de roteamento para direcionar solicitações de serviço entre os nós. Com Docker, diferentes redes são criadas para realizar o roteamento entre os contêineres. Sem Docker, uma classe em Python (ou na linguagem escolhida) é criada para realizar o roteamento entre os nós, incluindo a implementação de tabelas de roteamento e um mecanismo de encaminhamento de pacotes.
