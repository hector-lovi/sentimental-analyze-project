# Procesamiento natural del lenguaje focalizado en contenido audiovisual
Este repositorio tiene como objetivo la creación de un sistema de recomendación de series.  

Mediante una API construida en Python con Flask el usuario podrá almacenar contenido audiovisual (mediante un estilo similar al de un guión), pudiendo consultar dicho contenido, analizar su positividad / negatividad e incluso generar una recomendación.

# Documentación
Servicio de análisis de series, pudiendo extraer el sentimiento (por capítulos) de cualquier tipo de producto audiovisual, con el objetivo de recomendar las series en base a su similaridad entre el usuario y el contenido analizado.

- Index: @get("/help")
- User endpoints:
  - Create a new user: @post('/user/create')
  - Recommend a user to another user (based on nlp words similarity): @get("/user/<user_id>/recommend")

- Chat endpoints:
  - Create a new chat document: @post('/chat/create')
  - Extract sentiment from a certain chat: @get("/chat/<chat_id>/get_sentiment")
