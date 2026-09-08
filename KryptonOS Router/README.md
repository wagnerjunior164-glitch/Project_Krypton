# KryptonOS Router

## Objetivo

O **KryptonOS Router** é uma futura variante especializada do ecossistema KryptonOS destinada a roteadores, access points e outros appliances de rede compatíveis.

Ele não substituirá a versão de uso geral do KryptonOS. Será uma edição própria, otimizada para funções de rede, segurança, conectividade e integração com o ProjectKrypton.

## Direção tecnológica inicial

A direção registrada para estudo é utilizar o **OpenWrt como base tecnológica**, aproveitando sua infraestrutura Linux, suporte a hardware de rede, drivers, firewall, routing, Wi-Fi, DHCP, DNS, VPN, VLAN e gerenciamento de pacotes.

Sobre essa base poderão ser desenvolvidos componentes próprios do ecossistema Krypton, sem a necessidade de reinventar toda a infraestrutura de baixo nível de um sistema operacional de roteador.

## Arquitetura conceitual

```text
KryptonOS Router
│
├── Base OpenWrt / Linux
│   ├── Kernel
│   ├── Drivers
│   ├── Ethernet / Wi-Fi
│   ├── Routing
│   ├── Firewall
│   ├── DHCP / DNS
│   ├── VLAN
│   └── VPN
│
└── Camada Krypton
    ├── Krypton Core
    ├── Krypton Network
    ├── Krypton IoT
    ├── Krypton Center Agent
    └── Interface Web Krypton
```

## Integração com o ProjectKrypton

A variante deverá funcionar como um nó especializado do ecossistema:

```text
PROJECTKRYPTON
│
├── KryptonOS — uso geral
├── KryptonOS Router — rede / appliances
├── KryptonPlay — mídia
├── Krypton IoT — automação
└── Krypton Center — gerenciamento do ecossistema
```

O futuro Krypton Center poderá administrar e monitorar dispositivos que executarem o KryptonOS Router por meio de uma interface/API apropriada.

## Estado

🟡 **Planejamento futuro.** Nenhuma instalação de firmware, substituição de sistema ou alteração de hardware está autorizada neste estágio.

## Regra de segurança

Nenhum firmware experimental deverá ser instalado em hardware real sem que o modelo, revisão de hardware, imagem, bootloader e método de recuperação tenham sido previamente identificados e validados.
