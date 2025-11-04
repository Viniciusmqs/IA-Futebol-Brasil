# 📘 Dicionário de Dados — IA Futebol Brasil

## Tabela: Brasileirão Série A (`brasileirao_serie_a_clean.csv`)
Contém informações das partidas do Campeonato Brasileiro Série A de 2003 a 2024.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| ano_campeonato | int | Ano da edição do campeonato |
| data | date | Data de realização da partida |
| rodada | int | Número da rodada |
| estadio | string | Nome do estádio onde ocorreu o jogo |
| arbitro | string | Nome do árbitro principal |
| publico | float | Público pagante |
| publico_max | float | Capacidade máxima declarada do estádio |
| time_mandante | string | Nome do time mandante |
| time_visitante | string | Nome do time visitante |
| tecnico_mandante | string | Técnico do time mandante |
| tecnico_visitante | string | Técnico do time visitante |
| colocacao_mandante | float | Colocação do mandante antes da partida |
| colocacao_visitante | float | Colocação do visitante antes da partida |
| valor_equipe_titular_mandante | float | Valor de mercado do time titular mandante |
| valor_equipe_titular_visitante | float | Valor de mercado do time titular visitante |
| idade_media_titular_mandante | float | Idade média dos titulares mandantes |
| idade_media_titular_visitante | float | Idade média dos titulares visitantes |
| gols_mandante | int | Gols marcados pelo mandante |
| gols_visitante | int | Gols marcados pelo visitante |
| gols_1_tempo_mandante | int | Gols do mandante no primeiro tempo |
| gols_1_tempo_visitante | int | Gols do visitante no primeiro tempo |
| escanteios_mandante | float | Escanteios do mandante |
| escanteios_visitante | float | Escanteios do visitante |
| faltas_mandante | float | Faltas do mandante |
| faltas_visitante | float | Faltas do visitante |
| chutes_bola_parada_mandante | float | Chutes de bola parada do mandante |
| chutes_bola_parada_visitante | float | Chutes de bola parada do visitante |
| defesas_mandante | float | Defesas do goleiro mandante |
| defesas_visitante | float | Defesas do goleiro visitante |
| impedimentos_mandante | float | Impedimentos do mandante |
| impedimentos_visitante | float | Impedimentos do visitante |
| chutes_mandante | float | Total de chutes do mandante |
| chutes_visitante | float | Total de chutes do visitante |
| chutes_fora_mandante | float | Chutes para fora do mandante |
| chutes_fora_visitante | float | Chutes para fora do visitante |
| resultado | string | Resultado da partida (mandante, visitante, empate) |
| pontos_mandante | int | Pontos obtidos pelo mandante |
| pontos_visitante | int | Pontos obtidos pelo visitante |
| mandante_venceu | bool | Indicador se o mandante venceu |
| visitante_venceu | bool | Indicador se o visitante venceu |
| empate_flag | bool | Indicador se houve empate |

---

## Tabela: Copa do Brasil (`copa_brasil_clean.csv`)
Contém informações das partidas da Copa do Brasil entre 2020 e 2024.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| ano_campeonato | int | Ano da edição |
| data | date | Data de realização da partida |
| horario | string | Horário do jogo |
| fase | string | Nome da fase |
| tipo_fase | string | Tipo de fase (ida, volta, jogo único) |
| estadio | string | Estádio |
| arbitro | string | Nome do árbitro |
| publico | float | Público pagante |
| publico_max | float | Capacidade máxima declarada |
| time_mandante | string | Time mandante |
| time_visitante | string | Time visitante |
| tecnico_mandante | string | Técnico mandante |
| tecnico_visitante | string | Técnico visitante |
| valor_equipe_titular_mandante | float | Valor de mercado do time titular mandante |
| valor_equipe_titular_visitante | float | Valor de mercado do time titular visitante |
| idade_media_titular_mandante | float | Idade média dos titulares mandantes |
| idade_media_titular_visitante | float | Idade média dos titulares visitantes |
| gols_mandante | int | Gols marcados pelo mandante |
| gols_visitante | int | Gols marcados pelo visitante |
| gols_1_tempo_mandante | int | Gols do mandante no primeiro tempo |
| gols_1_tempo_visitante | int | Gols do visitante no primeiro tempo |
| penalti | bool | Indicador se houve pênaltis |
| gols_penalti_mandante | int | Gols de pênalti do mandante |
| gols_penalti_visitante | int | Gols de pênalti do visitante |
| escanteios_mandante | float | Escanteios do mandante |
| escanteios_visitante | float | Escanteios do visitante |
| faltas_mandante | float | Faltas do mandante |
| faltas_visitante | float | Faltas do visitante |
| chutes_bola_parada_mandante | float | Chutes de bola parada do mandante |
| chutes_bola_parada_visitante | float | Chutes de bola parada do visitante |
| defesas_mandante | float | Defesas do goleiro mandante |
| defesas_visitante | float | Defesas do goleiro visitante |
| impedimentos_mandante | float | Impedimentos do mandante |
| impedimentos_visitante | float | Impedimentos do visitante |
| chutes_mandante | float | Chutes totais do mandante |
| chutes_visitante | float | Chutes totais do visitante |
| chutes_fora_mandante | float | Chutes para fora do mandante |
| chutes_fora_visitante | float | Chutes para fora do visitante |
| resultado | string | Resultado da partida |
| pontos_mandante | int | Pontos obtidos pelo mandante |
| pontos_visitante | int | Pontos obtidos pelo visitante |
| mandante_venceu | bool | Indicador se o mandante venceu |
| visitante_venceu | bool | Indicador se o visitante venceu |
| empate_flag | bool | Indicador se houve empate |
