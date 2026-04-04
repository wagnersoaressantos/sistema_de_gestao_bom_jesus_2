# 🏥 Sistema de Gestão de Encaminhamentos em Saúde

## 🧠 Contexto
Este projeto está sendo desenvolvido com base em problemas reais observados na Atenção Primária à Saúde, especialmente no fluxo de encaminhamentos para especialidades médicas.

A proposta é digitalizar, organizar e otimizar a gestão da fila de espera, trazendo mais eficiência, transparência e suporte à tomada de decisão.

---

## 🎯 Problema

Em muitas unidades de saúde, o processo de encaminhamento ainda apresenta falhas críticas:

- Uso de papel ou planilhas desorganizadas
- Falta de controle da fila de espera
- Dificuldade para identificar:
  - Pacientes aguardando há mais tempo
  - Especialidades mais demandadas
- Risco de perda de informações
- Falta de rastreabilidade (não se sabe quem alterou o quê)
- Ocorrência de encaminhamentos duplicados
- Demora no atendimento por falta de organização

👉 **Resultado:**
Sistema ineficiente, retrabalho e prejuízo direto ao paciente.

---

## 💡 Solução

O sistema propõe uma gestão digital inteligente dos encaminhamentos, permitindo:

- Organização automatizada da fila
- Priorização por critérios clínicos e tempo de espera
- Controle de duplicidade
- Monitoramento em tempo real
- Geração de indicadores para gestão

---

## 🚧 Status do Projeto

🚧 Em desenvolvimento ativo

### ✅ Funcionalidades já implementadas

#### 📌 Organização
- Cadastro estruturado de encaminhamentos
- Fila automática baseada em prioridade e data

#### 🧠 Inteligência
- Cálculo de tempo de espera
- Identificação de tempo máximo de espera
- Análise de demanda por especialidade

#### 🔐 Segurança e controle
- Bloqueio de encaminhamentos duplicados
- Registro de tentativas inválidas (auditoria)

#### 📊 Gestão
- Dashboard com indicadores
- Visão geral da fila de espera

#### 🔍 Rastreabilidade
- Histórico de alterações
- Log de ações dos usuários

---

### 🔜 Funcionalidades em desenvolvimento

- Interface frontend (Flutter ou React)
- Melhorias no dashboard analítico
- Integração com sistemas externos
- Deploy em ambiente de produção (PostgreSQL)

---

## 🏗️ Arquitetura

O sistema segue uma organização modular, separando responsabilidades para facilitar manutenção e escalabilidade.

- **Backend:** Django
- **API:** Django REST Framework (DRF)
- **Banco de dados:** SQLite (dev) → PostgreSQL (produção)

### 🔧 Padrões e técnicas utilizadas

- ORM do Django
- Aggregations (Avg, Max, Count)
- Annotations (cálculo de tempo de espera)
- Signals (auditoria automática)
- Camada de Services (separação da lógica de negócio)

---

## 🛠️ Tecnologias

- Python
- Django
- Django REST Framework
- SQLite
- (Planejado) PostgreSQL
- (Planejado) Flutter ou React

---

## 👥 Público-alvo

### 👩‍⚕️ Profissionais de saúde
- Médicos e enfermeiros, podem consultar o sistema, não interfere no uso do sistema da unidade de saúde que é o E-SUS APS 
- Registro de encaminhamentos e visualizar o status das pastas

### 🧾 Recepção / Administrativo
- Registro de encaminhamentos e visualizar o status das pastas
- Organização da fila
- Atualização de status
- Consulta de pacientes

### 🧑‍⚕️ Agente Comunitário de Saúde (ACS)
- Acompanhamento de pacientes
- Identificação de demandas
- Redução de retrabalho

### 📊 Gestão
- Visualização de indicadores
- Apoio à tomada de decisão
- Identificação de gargalos (ex: especialidades sobrecarregadas)

---

## 📊 Impacto Esperado

- Redução de erros e retrabalho
- Maior transparência no processo
- Melhoria no tempo de atendimento
- Apoio à gestão baseada em dados
- Melhor acompanhamento dos pacientes

---

## 📷 Demonstração

> Em breve (prints da interface e do sistema em funcionamento)

---

## ⚙️ Como rodar o projeto

```bash
# Clone o repositório
git clone https://github.com/wagnersoaressantos/gestao-encaminhamentos-saude

# Acesse a pasta
cd gestao-encaminhamentos-saude

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Rode as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver

```
# 📚 Aprendizados

## Durante o desenvolvimento deste projeto, foram trabalhados:

* Modelagem de sistemas baseados em problemas reais
* Organização de código com Django
* Criação de APIs REST
* Uso de agregações e cálculos no banco de dados
* Implementação de auditoria automática
* Separação de regras de negócio (services)

# 🔮 Próximos passos
* Implementação do frontend (Flutter ou React)
* Deploy em produção
* Implementação de autenticação e permissões mais robustas
* Criação de relatórios avançados
* Escalabilidade para múltiplas unidades de saúde

# 🤝 Contribuição

* Sinta-se à vontade para contribuir com sugestões ou melhorias.

# 📬 Contato
GitHub: https://github.com/wagnersoaressantos

LinkedIn: www.linkedin.com/in/wagner-soaressantos
