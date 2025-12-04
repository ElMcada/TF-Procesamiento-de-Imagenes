<table>
<tr>
<td style="vertical-align: top; width: 100px; padding-right: 15px; border: none;">
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ45DITH77up1n8tb7Bx2n7TO8tBq4I65ZIuw&s", align="left">
</td>
<td style="vertical-align: top; border: none;">
<h1>Universidad Peruana de Ciencias Aplicadas</h1>
<h2>1ACC0235 – Procesamiento de Imágenes</h2>
<p><strong>Sección:</strong> 12624</p>
<p><strong>Profesor:</strong> Peter Jonathan Montalvo Garcia</p>
</td>
</tr>
</table>

## Problematica escogida

   *Al plantearnos este proyecto, partimos de una observación muy sencilla: a los niños pequeños muchas veces les cuesta poner en palabras lo que sienten. Es difícil para ellos decir "me siento frustrado" o "estoy ansioso", pero hemos notado que entienden y usan los emojis con mucha naturalidad. Basándonos en esto, pensamos en crear una herramienta educativa donde el niño pudiera demostrar que entiende una emoción dibujándola. Sin embargo, al intentar llevar esta idea a la práctica, nos encontramos con un problema técnico bastante grande: hacer que una computadora entienda los dibujos de un niño es mucho más difícil de lo que parece.

2.  **🖼️ Integración de Pictogramas ARASAAC:**
    * Para mejorar la comprensión y accesibilidad, KIBO analiza cada respuesta con `spaCy` para extraer palabras clave (sustantivos, verbos, adjetivos).
    * Busca automáticamente pictogramas para estas palabras en la API de ARASAAC y los muestra junto al texto.
3.  **🌐 Interfaz Web Interactiva:**
    * Frontend desarrollado con HTML, CSS y JavaScript para una interacción fluida.
    * Utiliza Firebase Firestore 🗃️ para almacenar el historial de conversaciones.
