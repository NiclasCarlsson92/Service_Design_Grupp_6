# Service Design - Grupp 6


Ni skall skapa en tjänst i form av ett API. Ni bestämmer själva vad ert API skall göra, men det måste uppfylla följande kriterier:

- Det skall följa god praxis och nå upp till nivå 3 i Richardson Maturity Model
- Det skall minst tillhandahålla metoderna för CRUD (CREATE/READ/UPDATE/DELETE)
- Projektet skall skapas och utvecklas med någon form av CI/CD struktur
- Datat skall hanteras av en databas
- Det skall finnas unit-test, gärna skrivna i PyTest
- Er kod skall ha en flerskiktsarkitektur som har minst tre väldefinierade områden och ni skall se till att koden inte utför uppgifter
  utanför sitt arkitektoniska ansvarsområde
- Ert API skall inte vara öppet, utan behöver skyddas med någon form av autentisering
- Access till ert API skall loggas i databasen. Ni skall alltså kunna se vem som använt API:et, när det skett och i vilket omfattning (exempelvis
  mängden data)
- Ert API skall ha en dokumentation, för detta kan ni exempelvis använda Swagger, men andra ramverk går också bra
