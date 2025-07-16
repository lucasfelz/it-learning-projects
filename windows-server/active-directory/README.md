# Construindo um Home Lab Active Directory: Do Zero à Administração Completa

## Introdução

Este Home Lab é fruto da minha motivação em aprendizado contínuo e prático. Os meus objetivos são a criação de um domínio completo com uma máquina Windows Server e uma máquina Windows 10 com vários usuários, a fim de construir um sistema funcional com a possibilidade de praticar:

- Administração de domínio Windows por meio do Active Directory;
- Configuração de rede com DHCP e DNS;
- Gerenciamento de usuários e permissões.

Após a construção da infraestrutura, o objetivo é utilizar o ambiente também para praticar a exploração de vulnerabilidades associadas ao Active Directory.

## Objetivos do Projeto

- Implementar um ambiente Active Directory funcional  
- Configurar políticas de grupo (GPOs)  
- Gerenciar usuários e permissões  
- Implementar backup e recuperação  
- Explorar vulnerabilidades associadas ao Active Directory  

---

## Planejamento da Infraestrutura

### Especificações do Hardware / Virtualização

- Hypervisor utilizado: **VirtualBox 7.1**
- Recursos disponíveis:
  - RAM: 8 GB
  - Armazenamento: 512 GB
  - Processador: Intel Pentium G4560

---

## Arquitetura Proposta

O projeto foi estruturado com:

- Uma máquina **Windows Server 2019** (Server19) como Domain Controller (DC), DHCP e DNS;
- Uma máquina **Windows 10** como cliente do domínio (Client1);
- Duas redes: NAT (para internet) e Rede Interna (comunicação entre as VMs).

![Arquitetura de rede do projeto](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/ARQUITETURA%20PROJETO%20AD.png)

---

## Planejamento de Rede

- **Domínio:** lab.ad.felz  
- **Faixa de IP:** 172.16.0.0/24  
- **DNS:** 172.16.0.1  
- **DHCP:** 172.16.0.100 – 172.16.0.200  

---

## Fase 1: Preparação do Ambiente

### Instalação do VirtualBox

Foi realizada a instalação do software VirtualBox versão 7.1 diretamente pelo site oficial: [https://www.virtualbox.org](https://www.virtualbox.org). A instalação ocorreu sem problemas, bastando seguir as configurações padrão.

---

## Fase 2: Instalação do Windows Server

### Versão Escolhida

- **Sistema Operacional:** Windows Server 2019  
- **Tipo de Instalação:** Standard - Desktop Experience

### Processo de Instalação

1. Inserção da ISO e início da instalação no VirtualBox;
2. Configuração inicial de idioma e layout;
3. Instalação da edição Desktop Experience;
4. Criação da senha do administrador;
5. Alocação de 50 GB de armazenamento virtual para o disco da máquina.

#### Capturas do processo:

![Configurações básicas](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(2).png)

![Disco de 50 GB alocado](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(3).png)


### Configuração da Rede Virtual

Para este projeto, foram criadas duas redes virtuais diferentes no VirtualBox:

#### 1. Rede NAT (para acesso à internet)
- **Objetivo:** Permitir que o Domain Controller (Server19) tenha acesso à internet por meio do roteador doméstico.
- **Configuração:**
  - Interface de rede 1 configurada como “Adaptador NAT” (nome da rede: `INTERNET`)
  - IP atribuído automaticamente via DHCP pelo roteador
  - Usada para atualizações do sistema e download de ferramentas

#### 2. Rede Interna (comunicação entre VMs)
- **Objetivo:** Criar uma rede local isolada entre o servidor e o cliente.
- **Configuração:**
  - Interface de rede 2 configurada como “Rede Interna” (nome da rede: `X_Internal_X`)
  - **Server19 (DC):** IP estático `172.16.0.1`, máscara `255.255.255.0`, DNS `127.0.0.1`
  - **Client1:** IP obtido via DHCP fornecido pelo próprio Server19

- **Configuração do escopo DHCP no Server19:**
  - Faixa: `172.16.0.100 – 172.16.0.200`
  - Gateway: `172.168.0.1` (definido manualmente)
  - DNS: `172.16.0.1` (o próprio DC)

---

### Tabela Resumo da Topologia

| VM            | NIC 1 (NAT)     | NIC 2 (Interna) | IP Interno   | Papel               |
| ------------- | --------------- | --------------- | ------------ | ------------------- |
| Server19 (DC) | INTERNET (NAT)  | X_Internal_X    | 172.16.0.1   | DC, DHCP, DNS, AD   |
| Client1       | --              | X_Internal_X    | Dinâmico     | Cliente do domínio  |

---

### Capturas de Tela

#### Rede NAT configurada:
![Rede NAT](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(19).png)

#### Rede Interna configurada no Windows Server:
![Rede Interna](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(20).png)

#### Visualização geral das redes:
![Duas redes](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(24).png)

#### IP recebido pelo roteador doméstico (rede NAT):
![IP NAT](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(22).png)

#### Configuração de IP estático no Server19:
![IP Fixo](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(25).png)

#### Endereços de referência adicionados:
![Referências IP](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(26).png)

#### Alteração do nome da Máquina (Passo a passo):
![caminhoNomePC1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(27).png)
![caminhoNomePC2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(28).png)
![caminhoNomePC3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(29).png)
![caminhoNomePC4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(30).png)

## Fase 3: Implementação do Active Directory
###  Instalação do AD DS (Active Directory Domain Services)
### Método utilizado: [Server Manager]

#### Passo a passo:

1. [Instalação da função AD DS]

![AD1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(31).png)
![AD2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(32).png)
![AD3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(33).png)
![AD4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(34).png)
![AD5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(35).png)

2. [Promoção do servidor a Domain Controller]
![AD6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(36).png)

3. [Configuração da floresta/domínio]
![AD7](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(38).png)
![AD8](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(39).png)
![AD9](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(40).png)
![AD10](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(41).png)
![AD11](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(42).png)
4. [Reinicialização do Seervidor para conclusão das configurações]
![AD12](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(43).png)

#### Configurações do domínio:

1. Nome do domínio: [exemplo.local]

![domain1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(44).png)
![domain2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(45).png)
![domain3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(46).png)
![domain4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(47).png)

2. Criação de Usuário adm [membro do Domain Admins]
![DA1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(48).png)
![DA2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(49).png)
![DA3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(50).png)
![DA4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(51).png)
![DA5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(52).png)
![DA6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(53).png)

3. Testando Usuário Criado e suas permissões:
![DA7](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(55).png)
![DA8](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(56).png)
![DA9](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(57).png)


## Fase 4: Implementação do Remote Access:
1. Passo a passo para configuração do Remote Access

![RA0](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(58).png)
![RA1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(59).png)
![RA2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(60).png)
![RA3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(61).png)
![RA4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(62).png)
![RA5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(63).png)
![RA6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(64).png)
![RA7](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(65).png)
![RA8](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(66).png)
![RA9](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(67).png)

#### * Nesse ponto a opção necessária não aparece, então é necessário fechar tudo e abrir de novo conforme descrito nos passos anteriores e a opção é carregada normalmente
![RA10](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(68).png)
![RA11](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(69).png)
![RA12](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(70).png)

### Configuração do DHCP
1. Passo a Passo:
![DHCP0](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(71).png)
![DHCP1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(72).png)
![DHCP3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(73).png)
![DHCP4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(74).png)

### *** Nesse passo eu cometi um erro. Após instalar o DHCP eu não configurei o post deployment do DHCP o que me gerou um erro futuro. Eu deveria ter ido até essa opção (vou mostrar ao final como resolver o problema que eu tive):
![DHCP5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(125).png)

### Só então eu deveria ter seguido com essa opção:
![DHCP6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(75).png)
![DHCP7](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(76).png)
![DHCP8](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(77).png)

#### Faixa de IPs: [início - fim]
#### Máscara de sub-rede: [máscara]
![DHCP9](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(78).png)
#### Só seguir Next
![DHCP10](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(80).png)

#### Na opção a seguir recomenda-se deixar 8h por ser um ambiente de testes, mas em produção é recomendado deixar com cerca de 2h para alteração automática de IP
![DHCP11](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(81).png)
![DHCP12](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(82).png)

#### Configurando o Gateway:
![DHCP13](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(83).png)

#### Domanin Name e DNS Server (O próprio Domain Controler)
![DMC1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(84).png)
![DMC2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(85).png)
![DMC3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(86).png)


## Fase 5: Estruturação Organizacional
### Criação de Unidades Organizacionais (OUs)
#### Após a configuração do DNS server, desliguei a "IE enhanced security configuration" que vem ativada por padrão para proteger o Windows Server de acessar scripts e portanto, impedir o acesso a malwares etc. Precisei desligdar para pegar um script de criação de usuários no gitHub.

![IE0](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(88).png)
![IE1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(89).png)
![IE2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(90).png)

#### O script se encontra no endereço - https://github.com/joshmadakor1/AD_PS/master.zip
![IE3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(91).png)

#### O script é:
```
﻿# ----- Edit these Variables for your own Use Case ----- #
$PASSWORD_FOR_USERS   = "Password1"
$USER_FIRST_LAST_LIST = Get-Content .\names.txt
# ------------------------------------------------------ #

$password = ConvertTo-SecureString $PASSWORD_FOR_USERS -AsPlainText -Force
New-ADOrganizationalUnit -Name _USERS -ProtectedFromAccidentalDeletion $false

foreach ($n in $USER_FIRST_LAST_LIST) {
    $first = $n.Split(" ")[0].ToLower()
    $last = $n.Split(" ")[1].ToLower()
    $username = "$($first.Substring(0,1))$($last)".ToLower()
    Write-Host "Creating user: $($username)" -BackgroundColor Black -ForegroundColor Cyan
    
    New-AdUser -AccountPassword $password `
               -GivenName $first `
               -Surname $last `
               -DisplayName $username `
               -Name $username `
               -EmployeeID $username `
               -PasswordNeverExpires $true `
               -Path "ou=_USERS,$(([ADSI]`"").distinguishedName)" `
               -Enabled $true
}
```


#### Seguindo para o passo a passo de como utilizar o script (a lista de nomes usada no script está no link do github acima):

![IE4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(92).png)

#### Adicionei meu nome no início da lista:
![IE5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(93).png)


#### Em seguida iniciei o powerShell para dar início a criação de usuários
![IE6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(94).png)
![IE7](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(95).png)
![IE8](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(97).png)
#### Alterei a política de segurança do powershell conforme mostrado abaixo para rodar o script:
![IE9](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(98).png)
![IE10](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(99).png)
![IE11](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(100).png)

#### Inicio da execução do script:
![PS0](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(102).png)

#### Refresh no AD para verificar o resultado:
![PS1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(103).png)
![PS2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(104).png)
![PS3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(105).png)
![PS4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(106).png)
![PS5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(107).png)
![PS6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(108).png)


### Estrutura criada das Unidades Organizacionais:
```
[Domínio]
 ├── Usuários
 │   ├── Administradores
 │   ├── Vendas
 │   └── TI
 ├── Computadores
 │   ├── Servidores
 │   ├── Desktops
 │   └── Laptops
 └── Grupos
     ├── Grupos de Segurança
     └── Grupos de Distribuição
```

*** POSTAR COMO FICOU ***



## Fase 6: Implementação da máquina windows10 para configurá-la na rede interna e testar o DHCP e DNS:
### Configurações iniciais no VirtualBox:
![PS7](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(109).png)
#### Configuração do adaptador de rede para - rede interna
![PS8](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(110).png)

#### Instalação do Win10:
![Win10-0](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(111).png)
![Win10-1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(112).png)
![Win10-2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(113).png)
![Win10-3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(114).png)
![Win10-4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(115).png)
![Win10-5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(116).png)

### Aqui foi onde eu reparei o erro que listei antes no DHCP: como eu tinha esquecido de de iniciar o DHCP conforme listado no início do presente projeto, o Windows10 instalado não recebeu IP automaticamente e portanto não tinha conexão com a internet.
![Win10-6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(119).png)

#### Correção: finalizando a config do DHCP e reiniciando o mesmo e o ifconfig:
![ip0](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(118).png)
![ip1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(120).png)
![ip2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(121).png)
![ip3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(122).png)
![ip4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(123).png)
![ip5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(124).png)
![ip6](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(128).png)

#### Deu certo!
![ip7](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(129).png)

![ip8](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(130).png)

#### Confirmando que os usuários foram criados com sucesso a tem permissão de acesso via Windows10 provando estarem conectados ao DC:
![PRV0](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(131).png)
![PRV1](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(132).png)
![PRV2](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(133).png)
![PRV3](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(134).png)
![PRV4](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(135).png)
![PRV5](https://github.com/lucasfelz/cybersecurity/blob/main/PersonalProjects/Project-Active-Directory-ADM%26vulnsExploitation/ScreenShoots-ProjectAD/Captura%20de%20Tela%20(136).png)





---





